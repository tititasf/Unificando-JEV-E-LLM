"""
E012 - JEV (TypeSafe System One) como S1 externo real em T1 (raiz) e T2 (k saltos).

Bracos:
  UMA      JEV em uma passada (uma pergunta Choice com o problema inteiro)
  REPETIR  a mesma pergunta de UMA, de novo (consistencia; so T2, k em {1, 2})
  ITER     T2: o controlador (S2) chama o JEV k vezes, um salto por chamada
  ITER_PF  T1: o controlador chama o JEV um salto por vez e para no ponto fixo
           (resposta == no atual: a checagem do S3), orcamento de 12 chamadas
  ACASO, UM_SALTO: linhas de base exatas, sem chamadas

Modos:
  python3 e012.py --coletar [--quick]   chama o JEV e grava respostas_jev.jsonl (retomavel)
  python3 e012.py [--quick]             so analisa as respostas gravadas (deterministico)

As instancias e a verdade sao regeneradas aqui a partir das sementes; do arquivo so se
le a escolha do JEV. A metrica nunca vem do JEV (regra 12).
"""
import json
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..", "..")
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(AQUI, "..", "E005_t2_salto"))
sys.path.insert(0, os.path.join(AQUI, "..", "E001_mlu"))
_argv = sys.argv
sys.argv = [sys.argv[0]]
import mlu  # noqa: E402
import tarefa_t2 as T2  # noqa: E402
sys.argv = _argv
from lab import estat, sementes  # noqa: E402

QUICK = "--quick" in sys.argv
COLETAR = "--coletar" in sys.argv
NS = (8, 32, 64)
KS = (1, 2, 4, 8)
DS = (1, 3, 5)
N_SEM = 2 if QUICK else 10
POR_CEL = 1 if QUICK else 3
ORC_PF = 12
MODELO = "jev-latest"
SUF = "_smoke" if QUICK else ""
ARQ = os.path.join(AQUI, f"respostas_jev{SUF}.jsonl")

INSTR = "Comece no no 'inicio' e siga 'ponteiros' exatamente k vezes. Em que no voce termina?"
INSTR_T1 = ("Comece no no 'inicio' e siga 'pai' ate chegar a um no que e pai de si mesmo (a raiz). "
            "Qual e essa raiz?")


def sementes_teste():
    if QUICK:
        return [1290, 1291]
    return sementes.derivar(sementes.base_teste(__file__), N_SEM)


def instancias():
    """Lista de (id, tarefa, N, param, dados, verdade, um_salto)."""
    out = []
    for i, sem in enumerate(sementes_teste()):
        rng = random.Random(sem)
        for N in NS:
            for k in KS:
                for j in range(POR_CEL):
                    pi, s, _, alvo = T2.exemplo(N, k, rng)
                    out.append((f"T2|{N}|{k}|{i}|{j}", "T2", N, k, (pi, s), alvo, pi[s]))
            for d in DS:
                for j in range(POR_CEL):
                    par, s, raiz = mlu.make_example(N, d, rng)
                    out.append((f"T1|{N}|{d}|{i}|{j}", "T1", N, d, (par, s), raiz, par[s]))
    return out


# ------------------------------------------------------------ coleta
_local = threading.local()


def _cli():
    if not hasattr(_local, "c"):
        from lab import jev
        jev.credencial()
        from typesafe_sdk import TypeSafeClient
        _local.c = TypeSafeClient()
    return _local.c


def _pergunta(estado, instr, N):
    from typesafe_sdk import Choice
    t0 = time.time()
    try:
        r = _cli().system_one(state=estado, model=MODELO,
                              questions={"q": Choice(instructions=instr, criteria={str(i): None for i in range(N)})})
    except Exception as e:  # registrado como erro; conta como errado na analise
        return dict(erro=type(e).__name__ + ": " + str(e)[:200], dt=time.time() - t0)
    a = r.choices["q"]
    return dict(escolha=a.choice, conf=a.confidence, probs=dict(a.probabilities), modelo=r.model,
                tin=r.usage.input_tokens, tout=r.usage.output_tokens, dt=time.time() - t0)


def _um_salto(ponteiros, x):
    return _pergunta({"ponteiros": {str(i): p for i, p in enumerate(ponteiros)}, "inicio": x, "k": 1},
                     INSTR, len(ponteiros))


def _tarefas_de(inst):
    iid, tarefa, N, p, (g, s), _, _ = inst
    tarefas = []
    if tarefa == "T2":
        tarefas.append((iid, "UMA", lambda: [_pergunta({"ponteiros": {str(i): v for i, v in enumerate(g)},
                                                        "inicio": s, "k": p}, INSTR, N)]))
        if p in (1, 2):
            tarefas.append((iid, "REPETIR", lambda: [_pergunta({"ponteiros": {str(i): v for i, v in enumerate(g)},
                                                                "inicio": s, "k": p}, INSTR, N)]))

        def iterar():
            passos, x = [], s
            for _ in range(p):
                r = _um_salto(g, x)
                r["x"] = x
                passos.append(r)
                if "erro" in r:
                    break
                x = int(r["escolha"])
            return passos
        tarefas.append((iid, "ITER", iterar))
    else:
        tarefas.append((iid, "UMA", lambda: [_pergunta({"pai": {str(i): v for i, v in enumerate(g)},
                                                        "inicio": s}, INSTR_T1, N)]))

        def iterar_pf():
            passos, x = [], s
            for _ in range(ORC_PF):
                r = _um_salto(g, x)
                r["x"] = x
                passos.append(r)
                if "erro" in r:
                    break
                y = int(r["escolha"])
                if y == x:
                    break
                x = y
            return passos
        tarefas.append((iid, "ITER_PF", iterar_pf))
    return tarefas


def coletar():
    feitos = set()
    if os.path.exists(ARQ):
        for linha in open(ARQ):
            r = json.loads(linha)
            feitos.add((r["id"], r["braco"]))
    fila = [t for inst in instancias() for t in _tarefas_de(inst) if (t[0], t[1]) not in feitos]
    print(f"coleta: {len(fila)} (instancia, braco) a fazer; {len(feitos)} ja gravados", flush=True)
    trava = threading.Lock()
    cont = [0]

    def rodar(t):
        iid, braco, fn = t
        passos = fn()
        with trava, open(ARQ, "a") as fh:
            fh.write(json.dumps({"id": iid, "braco": braco, "passos": passos}) + "\n")
            cont[0] += 1
            if cont[0] % 100 == 0:
                print(f"  {cont[0]}/{len(fila)}", flush=True)
    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(rodar, fila))


# ------------------------------------------------------------ analise
def resposta_final(braco, passos):
    """No escolhido pelo braco (ou None: erro ou orcamento esgotado sem ponto fixo)."""
    if not passos or any("erro" in q for q in passos):
        return None
    if braco == "ITER_PF":
        ult = passos[-1]
        return int(ult["escolha"]) if int(ult["escolha"]) == ult["x"] else None
    return int(passos[-1]["escolha"])


def analisar():
    insts = {i[0]: i for i in instancias()}
    reg = {}
    for linha in open(ARQ):
        r = json.loads(linha)
        if r["id"] not in insts:
            raise RuntimeError(f"registro de instancia desconhecida: {r['id']}")
        reg[(r["id"], r["braco"])] = r["passos"]
    # coerencia: o primeiro passo dos bracos iterados parte do inicio verdadeiro, e cada passo
    # parte da escolha anterior (o arquivo nao pode ter sido montado a mao)
    for (iid, braco), passos in reg.items():
        if braco in ("ITER", "ITER_PF") and passos and "erro" not in passos[0]:
            s = insts[iid][4][1]
            assert passos[0]["x"] == s, iid
            for a, b in zip(passos, passos[1:]):
                assert b["x"] == int(a["escolha"]), iid
    esperado = [(iid, b) for iid, inst in insts.items() for (_, b, _) in _tarefas_de(inst)]
    faltando = [e for e in esperado if e not in reg]
    chamadas = [q for p in reg.values() for q in p]
    erros = sum(1 for q in chamadas if "erro" in q)
    modelos = sorted({q.get("modelo") for q in chamadas if "modelo" in q})
    res = {"n_registros": len(reg), "faltando": len(faltando), "chamadas": len(chamadas), "erros": erros,
           "modelos": modelos, "tokens_in": sum(q.get("tin") or 0 for q in chamadas),
           "tokens_out": sum(q.get("tout") or 0 for q in chamadas), "celulas": {}}

    def celula(tarefa, N, p, braco):
        por_sem = {}
        acertos, confs, corr, atalho_err, n_err, cham = 0, [], [], 0, 0, []
        for iid, inst in insts.items():
            _, t, n_, p_, (g, s), verdade, um = inst
            if (t, n_, p_) != (tarefa, N, p):
                continue
            i = int(iid.split("|")[3])
            if braco == "ACASO":
                ok = 1.0 / N
            elif braco == "UM_SALTO":
                ok = 1.0 if um == verdade else 0.0
            else:
                passos = reg.get((iid, braco))
                if passos is None:
                    continue
                y = resposta_final(braco, passos)
                ok = 1.0 if y == verdade else 0.0
                cham.append(len(passos))
                if braco in ("UMA", "REPETIR") and "erro" not in passos[0]:
                    pc = passos[0]["probs"].get(passos[0]["escolha"], 0.0)
                    confs.append(pc)
                    corr.append(ok == 1.0)
                    if ok == 0.0:
                        n_err += 1
                        atalho_err += (y == um)
            por_sem.setdefault(i, []).append(ok)
            acertos += ok
        sem = [estat.media(v) for _, v in sorted(por_sem.items())]
        n = sum(len(v) for v in por_sem.values())
        return {"n": n, "acertos": acertos, "acc": acertos / n if n else None, "iqm": estat.iqm(sem) if sem else None,
                "ic": list(estat.bootstrap_ic(sem, estat.iqm)) if len(sem) > 1 else None,
                "chamadas_media": estat.media(cham) if cham else 0.0, "confs": confs, "corretos": corr,
                "erros_atalho": atalho_err, "n_erros": n_err}

    for N in NS:
        for k in KS:
            for b in ("UMA", "REPETIR", "ITER", "ACASO", "UM_SALTO"):
                if b == "REPETIR" and k not in (1, 2):
                    continue
                res["celulas"][f"T2|{N}|{k}|{b}"] = celula("T2", N, k, b)
        for d in DS:
            for b in ("UMA", "ITER_PF", "ACASO", "UM_SALTO"):
                res["celulas"][f"T1|{N}|{d}|{b}"] = celula("T1", N, d, b)
    # consistencia UMA x REPETIR (mesma pergunta duas vezes)
    concord = {}
    for k in (1, 2):
        iguais, tot = 0, 0
        for iid, inst in insts.items():
            if inst[1] == "T2" and inst[3] == k:
                a, b = reg.get((iid, "UMA")), reg.get((iid, "REPETIR"))
                if a and b and "erro" not in a[0] and "erro" not in b[0]:
                    tot += 1
                    iguais += a[0]["escolha"] == b[0]["escolha"]
        concord[k] = (iguais, tot)
    res["concordancia"] = {str(k): v for k, v in concord.items()}
    # acuracia por salto (cada chamada de um salto e verificavel: escolha == ponteiro[x])
    passo = {}
    for (iid, braco), passos in reg.items():
        if braco not in ("ITER", "ITER_PF"):
            continue
        g = insts[iid][4][0]
        chave = f"{insts[iid][1]}|{insts[iid][2]}"
        ok, n = passo.get(chave, (0, 0))
        for q in passos:
            if "erro" not in q:
                ok += int(q["escolha"]) == g[q["x"]]
                n += 1
        passo[chave] = (ok, n)
    res["passo"] = passo
    return res


def checar_previsoes(res):
    C = res["celulas"]
    L = []

    def acc(chave):
        return C[chave]["acc"]
    # P1
    p1 = {N: acc(f"T2|{N}|1|UMA") for N in NS}
    L.append(("P1", all(v >= 0.80 for v in p1.values()),
              "UMA T2 k=1 >= 0,80 em todo N: " + ", ".join(f"N={N}: {v:.2f}" for N, v in p1.items())))
    # P2
    p2 = {(N, k): acc(f"T2|{N}|{k}|UMA") for N in (32, 64) for k in (2, 4, 8)}
    L.append(("P2", all(v <= 0.25 for v in p2.values()),
              "UMA T2 k>=2 <= 0,25 em N=32,64: max = " + f"{max(p2.values()):.2f}"))
    # P3
    ea = sum(C[f"T2|{N}|{k}|UMA"]["erros_atalho"] for N in NS for k in (2, 4, 8))
    ne = sum(C[f"T2|{N}|{k}|UMA"]["n_erros"] for N in NS for k in (2, 4, 8))
    L.append(("P3", ne > 0 and ea / ne >= 0.40, f"erros de UMA (k>=2) iguais ao atalho pi(s): {ea}/{ne} = {ea / max(ne, 1):.2f}"))
    # P4
    ai = sum(C[f"T2|{N}|4|ITER"]["acertos"] for N in NS)
    au = sum(C[f"T2|{N}|4|UMA"]["acertos"] for N in NS)
    n4 = sum(C[f"T2|{N}|4|ITER"]["n"] for N in NS)
    n4u = sum(C[f"T2|{N}|4|UMA"]["n"] for N in NS)
    pf = estat.fisher_exato(int(ai), n4, int(au), n4u)
    L.append(("P4", ai / n4 > au / n4u and pf < 0.01, f"k=4 ITER {ai:.0f}/{n4} vs UMA {au:.0f}/{n4u}, Fisher p = {pf:.2g}"))
    # P5
    dentro, tot, det = 0, 0, []
    for N in NS:
        ok, n = res["passo"][f"T2|{N}"]
        base = ok / n
        for k in (2, 4, 8):
            prev, obs = base ** k, acc(f"T2|{N}|{k}|ITER")
            tot += 1
            dentro += abs(obs - prev) <= 0.15
            det.append(f"N={N},k={k}: {obs:.2f} vs {prev:.2f}")
    L.append(("P5", dentro >= 7, f"lei multiplicativa acc(k) ~ q^k (q = acerto por salto) dentro de 0,15 em {dentro}/{tot} celulas ({'; '.join(det)})"))
    # P6
    ai = sum(C[f"T1|{N}|{d}|ITER_PF"]["acertos"] for N in NS for d in DS)
    au = sum(C[f"T1|{N}|{d}|UMA"]["acertos"] for N in NS for d in DS)
    ni = sum(C[f"T1|{N}|{d}|ITER_PF"]["n"] for N in NS for d in DS)
    nu = sum(C[f"T1|{N}|{d}|UMA"]["n"] for N in NS for d in DS)
    pf = estat.fisher_exato(int(ai), ni, int(au), nu)
    L.append(("P6", ai / ni > au / nu and pf < 0.01, f"T1 ITER_PF {ai:.0f}/{ni} vs UMA {au:.0f}/{nu}, Fisher p = {pf:.2g}"))
    # P7, P8 (calibracao do JEV em uma passada, T2)
    confs, corr = [], []
    for N in NS:
        for k in KS:
            confs += C[f"T2|{N}|{k}|UMA"]["confs"]
            corr += C[f"T2|{N}|{k}|UMA"]["corretos"]
    cc = [c for c, o in zip(confs, corr) if o]
    ce = [c for c, o in zip(confs, corr) if not o]
    pp = estat.teste_permutacao(cc, ce) if cc and ce else 1.0
    L.append(("P7", bool(cc and ce) and estat.media(cc) > estat.media(ce) and pp < 0.01,
              f"p(escolha) certo {estat.media(cc) if cc else 0:.2f} vs errado {estat.media(ce) if ce else 0:.2f}, perm p = {pp:.2g}; "
              f"ECE = {estat.ece(confs, corr):.3f}"))
    ctot, cerr = [], 0
    for chave, c in C.items():
        if chave.endswith("|UMA"):
            for pc, o in zip(c["confs"], c["corretos"]):
                if not o:
                    ctot.append(pc)
                    cerr += pc >= 0.9
    L.append(("P8", len(ctot) > 0 and cerr / len(ctot) <= 0.05, f"erros confiantes (p >= 0,9) em UMA T1+T2: {cerr}/{len(ctot)}"))
    # P9
    ig, tot = res["concordancia"]["1"]
    L.append(("P9", tot > 0 and ig / tot >= 0.80, f"UMA x REPETIR concordam em T2 k=1: {ig}/{tot}"))
    return L


def main():
    if COLETAR:
        coletar()
    res = analisar()
    L = [f"# E012 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"Modelos: {res['modelos']}; chamadas {res['chamadas']}; erros {res['erros']}; faltando {res['faltando']}; "
         f"tokens in/out {res['tokens_in']}/{res['tokens_out']}", "",
         "| tarefa | N | k ou d | braço | acerto (n) | IQM entre sementes [IC95%] | chamadas/inst |", "|---|---|---|---|---|---|---|"]
    for chave, c in res["celulas"].items():
        t, N, p, b = chave.split("|")
        ic = f"[{c['ic'][0]:.2f},{c['ic'][1]:.2f}]" if c["ic"] else "-"
        acc_s = f"{c['acc']:.2f}" if c["acc"] is not None else "-"
        iqm_s = f"{c['iqm']:.2f}" if c["iqm"] is not None else "-"
        L.append(f"| {t} | {N} | {p} | {b} | {acc_s} ({c['n']}) | {iqm_s} {ic} | {c['chamadas_media']:.1f} |")
    L += ["", "Acurácia por salto (chamadas de um salto): " + ", ".join(
        f"{k}: {ok}/{n} = {ok / n:.3f}" for k, (ok, n) in sorted(res["passo"].items()) if n), "",
        "Concordância UMA x REPETIR: " + ", ".join(f"k={k}: {a}/{b}" for k, (a, b) in res["concordancia"].items())]
    L += ["", "## Checagem das previsões", ""]
    for pid, ok, txt in checar_previsoes(res):
        L.append(f"- {pid} {'OK' if ok else 'FALHOU'}: {txt}")
    open(os.path.join(AQUI, f"resultados{SUF}.md"), "w").write("\n".join(L) + "\n")
    enxuto = {k: v for k, v in res.items() if k != "celulas"}
    enxuto["celulas"] = {k: {kk: vv for kk, vv in v.items() if kk not in ("confs", "corretos")}
                         for k, v in res["celulas"].items()}
    json.dump(enxuto, open(os.path.join(AQUI, f"resultados{SUF}.json"), "w"), indent=1, sort_keys=True)
    print("\n".join(L[-12:]))


if __name__ == "__main__":
    main()
