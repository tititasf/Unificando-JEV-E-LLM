"""
E020 - leitura robusta da variavel oculta: escolha da regra pelo residuo de fechamento (N2, 10 sementes).

Redes: as do E019 (importadas; so ponteiro, sem dicas, sem valor), sementes novas. Familias: SP e WP (controle).
Leitura (nenhuma verdade entra):
  - para cada forma R (18): 3 reinicios da leitura linear z = h.a + b0 + coeficientes pelo residuo de fechamento
    normalizado (e019.ajusta_leitura); fica o reinicio de menor residuo; normaliza e arredonda (e019.normaliza);
  - ESCOLHA NOVA: a forma cuja regra ARREDONDADA tem o menor residuo de fechamento normalizado na propria leitura
    normalizada z'' (transicoes de n = 16 e 32); empate -> menor soma |coef|;
    inicio: o que deixa o programa (64 passos, n = 32, fonte 0) mais perto da leitura final z''(h^32) da rede;
    ponteiro: concordancia com os ponteiros da rede (18 formas);
  - ESCOLHA ANTIGA (E019, ablacao pareada): e019.melhor_programa nos mesmos candidatos (concordancia de ponteiro).
Diagnostico pos-escolha: Pearson(leitura escolhida, variavel verdadeira) nos nos nao-fonte (n = 32).
Reconhecimento (SP): e019.reconhece_sp. Programas executados em Python puro em n = 16, 64, 256.
A sintese direta (5/5 no E018 e no E019) nao roda aqui, por custo (declarado).
Uso: python3 e020.py [--quick] [--procs=4]
"""
import json
import os
import random
import sys
import time
from multiprocessing import Pool

import torch

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E018_extracao"))
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E019_variavel_oculta"))
import e018 as M  # noqa: E402
import e019 as E19  # noqa: E402
from lab import estat, sementes  # noqa: E402
from lab import tarefas_clrs as C  # noqa: E402

QUICK = "--quick" in sys.argv
SEMENTES = [2090, 2091] if QUICK else list(range(2000, 2010))
FAMILIAS = ("SP", "WP")
REINICIOS = 3
NS_REDE = (16, 32, 64)
NS_PROG = (16, 64, 256)
N_TESTE = 16 if QUICK else 64
N_PROG = 4 if QUICK else 20
SUF = "_smoke" if QUICK else ""
E19.PASSOS = 300 if QUICK else 4000
E19.PASSOS_LEITURA = 60 if QUICK else 300


def residuo(regra, th, ler, trans):
    with torch.no_grad():
        num, zs = 0.0, []
        t = torch.tensor(th, dtype=torch.float)
        for h0, h1, W, A0, S in trans:
            m = S == 0
            z0, z1 = ler(h0), ler(h1)
            num += float(((z1 - M.aplica(regra, t, z0, W, A0))[m] ** 2).mean())
            zs.append(z1[m])
        return num / len(trans) / (float(torch.cat(zs).var()) + 1e-9)


def escolha_nova(cands, leituras, trans, hs_fim, W, A0, S, pr):
    melhor = None
    for regra, th in cands:
        e = residuo(regra, th, leituras[regra], trans)
        k = (round(e, 6), sum(abs(v) for v in th))
        if melhor is None or k < melhor[0]:
            melhor = (k, regra, th, e)
    _, regra, th, e = melhor
    with torch.no_grad():
        alvo = leituras[regra](hs_fim)
    m = S == 0
    best_ini = None
    for i, ini in enumerate(M.INICIOS):
        x0 = torch.where(S > 0, torch.zeros_like(S), torch.full_like(S, ini))
        x = M.executar(regra, torch.tensor(th, dtype=torch.float), x0, S, W, A0, 64)
        d = float((x - alvo)[m].abs().clamp(max=10).mean())
        if best_ini is None or (round(d, 6), i) < best_ini[0]:
            best_ini = ((round(d, 6), i), ini, x)
    _, ini, x = best_ini
    best_p = None
    for fp in M.PONTEIROS:
        c = round((E19.ptr_de(x, fp, W, A0, S) == pr).float().mean().item(), 6)
        if best_p is None or c > best_p[0]:
            best_p = (c, fp[0], fp[1], fp[2])
    prog = {"regra": regra, "th": [float(v) for v in th], "ini": ini, "fonte": 0.0}
    return prog, best_p, e


def uma(arg):
    seed, fam, sem_teste = arg
    torch.set_num_threads(1)
    t0 = time.time()
    fi = FAMILIAS.index(fam)
    r = {"seed": seed, "fam": fam}
    net = E19.treinar_ptr(fam, seed * 10 + fi)
    trng = random.Random(sem_teste * 10 + fi)
    with torch.no_grad():
        for n in NS_REDE:
            W, A, S, Y, V, _ = M.lote(fam, N_TESTE, n, trng)
            lg, _, _ = net(W, A, S, n)
            r[f"rede|{n}|ptr"] = M.acuracia_ptr(lg.argmax(-1), V)
    xrng = random.Random(sem_teste * 10 + 5 + fi)
    trans = []
    for n in (16, 32):
        W, A, S, Y, V, _ = M.lote(fam, 8, n, xrng)
        hs = E19.trilha(net, W, A, S, 16)
        A0 = A - torch.eye(n)
        for t in range(1, len(hs) - 1):
            trans.append((hs[t], hs[t + 1], W, A0, S))
    gen = torch.Generator().manual_seed(seed * 10 + fi)
    cands, leituras = [], {}
    for regra in M.REGRAS:
        melhor = None
        for _ in range(REINICIOS):
            a, b0, res = E19.ajusta_leitura(regra, trans, gen)
            if melhor is None or res < melhor[0]:
                melhor = (res, a, b0)
        th, ler = E19.normaliza(regra, melhor[1], melhor[2], trans)
        cands.append((regra, th))
        leituras[regra] = ler
    W, A, S, Y, V, _ = M.lote(fam, 8, 32, xrng)
    A0 = A - torch.eye(32)
    with torch.no_grad():
        lg, _, _ = net(W, A, S, 32)
    pr = lg.argmax(-1)
    hs = E19.trilha(net, W, A, S, 32)
    prog_n, ptr_n, res_n = escolha_nova(cands, leituras, trans, hs[-1], W, A0, S, pr)
    prog_a, ptr_a, _ = E19.melhor_programa(cands, (0.0,), W, A0, S, lambda p: (p == pr).float().mean().item())
    m = S == 0
    with torch.no_grad():
        r["corr_nova"] = E19.pearson(leituras[prog_n["regra"]](hs[-1])[m], Y[m])
        r["corr_antiga"] = E19.pearson(leituras[prog_a["regra"]](hs[-1])[m], Y[m])
        r["corr_max_18"] = max(abs(E19.pearson(leituras[rg](hs[-1])[m], Y[m])) for rg in M.REGRAS)
    r["residuo_nova"] = res_n
    for nome, prog, ptr in (("nova", prog_n, ptr_n), ("antiga", prog_a, ptr_a)):
        r[f"{nome}|prog"] = [list(prog["regra"]), prog["th"], prog["ini"], prog["fonte"]]
        r[f"{nome}|ptr"] = [ptr[0], ptr[1], ptr[2], list(ptr[3])]
        r[f"{nome}|reconhece"] = E19.reconhece_sp(prog, ptr) if fam == "SP" else None
        prng = random.Random(sem_teste * 10 + 7 + fi)
        for n in NS_PROG:
            accs = []
            for _ in range(N_PROG):
                adj = C.grafo_er(n, 0.5, prng, pesos=True)
                s = prng.randrange(n)
                _, val = M.verdade(fam, adj, s)
                _, pi = M.programa(prog, ptr, adj, s)
                accs.append(sum(pi[v] in val[v] for v in range(n)) / n)
            r[f"{nome}|{n}|ptr"] = sum(accs) / len(accs)
    r["cpu_s"] = time.time() - t0
    print(f"{fam} semente {seed} ok ({r['cpu_s']:.0f}s)", flush=True)
    return r


def main():
    procs = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--procs=")), 4)
    teste = [2095, 2096] if QUICK else sementes.derivar(sementes.base_teste(__file__), len(SEMENTES))
    jobs = [(sd, fam, st) for sd, st in zip(SEMENTES, teste) for fam in FAMILIAS]
    with Pool(procs) as pool:
        res = pool.map(uma, jobs)
    json.dump(res, open(os.path.join(AQUI, f"resultados{SUF}.json"), "w"), indent=1, sort_keys=True)
    k = len(SEMENTES)
    sp = [x for x in res if x["fam"] == "SP"]
    wp = [x for x in res if x["fam"] == "WP"]
    L = [f"# E020 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{k} sementes por familia; redes so com ponteiro; rede: {N_TESTE} grafos por n; programa: {N_PROG} grafos por n.", "",
         "| família | quem | n | ponteiro IQM [IC95%] |", "|---|---|---|---|"]

    def linha(fam, quem, n, a):
        lo, hi = estat.bootstrap_ic(a, estat.iqm)
        L.append(f"| {fam} | {quem} | {n} | {estat.iqm(a):.3f} [{lo:.3f},{hi:.3f}] |")
    for fam, rf in (("SP", sp), ("WP", wp)):
        for n in NS_REDE:
            linha(fam, "rede (só ponteiro)", n, [x[f"rede|{n}|ptr"] for x in rf])
        for nome in ("nova", "antiga"):
            for n in NS_PROG:
                linha(fam, f"programa (escolha {nome})", n, [x[f"{nome}|{n}|ptr"] for x in rf])
    L += ["", "| família | semente | escolha nova | ponteiro | r nova | escolha antiga | r antiga | máx \\|r\\| 18 |",
          "|---|---|---|---|---|---|---|---|"]
    for x in res:
        L.append(f"| {x['fam']} | {x['seed']} | {x['nova|prog']} | {x['nova|ptr']} | {x['corr_nova']:.3f} | "
                 f"{x['antiga|prog']} {x['antiga|ptr']} | {x['corr_antiga']:.3f} | {x['corr_max_18']:.3f} |")
    L += ["", "## Checagem das previsões (PREVISOES.md, commitadas antes de qualquer piloto)", ""]

    def chk(nome, ok, txt):
        L.append(f"- {nome} {'OK' if ok else 'FALHOU'}: {txt}")
    rn = sum(x["nova|reconhece"] for x in sp)
    ra = sum(x["antiga|reconhece"] for x in sp)
    chk("P1", rn >= 8, f"SP escolha nova reconhecida em >= 8/10: {rn}/{k}")
    cn = sum(abs(x["corr_nova"]) >= 0.9 for x in sp)
    chk("P2", cn >= 8, f"SP |r(leitura, distância)| >= 0,9 em >= 8/10: {cn}/{k} {[round(x['corr_nova'], 3) for x in sp]}")
    cw = sum(abs(x["corr_nova"]) < 0.5 for x in wp)
    chk("P3", cw >= 8, f"WP |r(leitura, largura)| < 0,5 em >= 8/10: {cw}/{k} {[round(x['corr_nova'], 3) for x in wp]}")
    chk("P4", rn >= 7, f"SP escolha nova reconhecida em >= 7/10 (regra de parada): {rn}/{k}")
    chk("P5", rn >= ra + 2, f"escolha nova >= antiga + 2 nas mesmas redes: {rn} contra {ra}")
    rec = [x[f"{nm}|256|ptr"] for x in sp for nm in ("nova", "antiga") if x[f"{nm}|reconhece"]]
    chk("P6", bool(rec) and min(rec) == 1.0, f"todo programa reconhecido acerta 1,000 em n=256: min {min(rec) if rec else '-'} ({len(rec)})")
    a64 = estat.iqm([x["rede|64|ptr"] for x in sp])
    chk("P7", a64 >= 0.75, f"rede SP só com ponteiro em n=64 >= 0,75: {a64:.3f}")
    so_n = sum(x["nova|reconhece"] and not x["antiga|reconhece"] for x in sp)
    so_a = sum(x["antiga|reconhece"] and not x["nova|reconhece"] for x in sp)
    L.append(f"- Pareado (discordantes): só a nova {so_n}, só a antiga {so_a}; "
             f"Fisher nova×antiga p = {estat.fisher_exato(rn, k, ra, k):.3f}; IC95% da taxa nova {estat.ic_proporcao(rn, k)}")
    L.append(f"- CPU total: {sum(x['cpu_s'] for x in res):.0f}s")
    txt = "\n".join(L)
    open(os.path.join(AQUI, f"resultados{SUF}.md"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
