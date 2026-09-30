"""
E019 - a rede generica treinada so com o ponteiro inventa a distancia? Leitura nao supervisionada da variavel oculta.

Protocolo CLRS: a saida e so o ponteiro pi (pais validos); a distancia NAO e dada (nem como saida, nem como dica).
Familias: SP (caminho minimo; o ponteiro exige a distancia oculta) e WP (caminho mais largo; controle negativo:
o ponteiro e trivial, a aresta mais pesada, e a rede nao precisa de estado oculto).

Rede: a do E018 (importada), treinada so com a perda de ponteiro. 4000 passos, n = 16.

Rota mecanistica (nenhuma verdade entra):
  1. trajetorias h^t da rede em grafos novos (n = 16 e 32);
  2. para cada uma das 18 formas R da linguagem do E018: ajusta uma leitura linear z = h.a + b0 e os coeficientes de R
     minimizando o residuo de fechamento  mean (z^t+1 - R(z^t))^2 / var(z)  nos nos nao-fonte;
  3. normaliza: z' = (z - z_fonte) / escala (escala = coeficiente do peso, se |.| > 0,05; senao desvio de z),
     reajusta os coeficientes em z' e arredonda a 1/2 (Occam);
  4. programa = (forma, coeficientes, inicio em {-inf, +inf, 0, 1}, fonte 0) executado 64 passos em n = 32;
     ponteiro = argmin/argmax_u g(x_u, w) (18 formas); escolha pela concordancia com os ponteiros DA REDE.
Sintese direta (atalho nao neural, sem rede): enumeracao conjunta de forma x grade x inicio x fonte {0, 1} x ponteiro,
escolha pela validade contra os ponteiros VERDADEIROS.
Diagnostico pos-escolha (nao entra na escolha): correlacao de Pearson entre a leitura z' (passo final) e a variavel
verdadeira (distancia no SP, largura no WP).
Reconhecimento (SP): regra min(x_v, min_u x_u + w) (ou sem manter), coef [1,1,0], inicio +inf, ponteiro argmin x_u + w.
A relaxacao min-plus e invariante a deslocamento, entao o valor da fonte e livre; pelo teorema de Bellman-Ford o programa
reconhecido e correto para todo grafo com pesos positivos (prova por reducao; nao e assistente de provas).
Uso: python3 e019.py [--quick] [--procs=4]
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
import e018 as M  # noqa: E402
from lab import estat, sementes  # noqa: E402
from lab import tarefas_clrs as C  # noqa: E402

QUICK = "--quick" in sys.argv
SEMENTES = [1990, 1991] if QUICK else list(range(1900, 1905))
FAMILIAS = ("SP", "WP")
PASSOS = 300 if QUICK else 4000
PASSOS_LEITURA = 60 if QUICK else 300
NS_REDE = (16, 32, 64)
NS_PROG = (16, 64, 256)
N_TESTE = 16 if QUICK else 64
N_PROG = 4 if QUICK else 20
SUF = "_smoke" if QUICK else ""


def treinar_ptr(fam, seed):
    torch.manual_seed(seed)
    rng = random.Random(seed)
    net = M.Rede()
    opt = torch.optim.Adam(net.parameters(), 5e-4)
    dados = [M.lote(fam, 32, C.N_TREINO, rng) for _ in range(100)]
    for it in range(PASSOS):
        W, A, S, Y, V, _ = dados[it % len(dados)]
        lg, _, _ = net(W, A, S, rng.randint(8, 24))
        lp = torch.log_softmax(lg, -1)
        perda = -torch.logsumexp(lp.masked_fill(V == 0, -M.INF), -1).mean()  # so o ponteiro
        opt.zero_grad()
        perda.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
        opt.step()
    return net


def trilha(net, W, A, S, T):
    with torch.no_grad():
        h = net.enc(S.unsqueeze(-1))
        hs = [h]
        for _ in range(T):
            h = net.passo(h, W, A)
            hs.append(h)
    return hs


def ajusta_leitura(regra, trans, gen):
    """Leitura z = h.a + b0 e coeficientes de R pelo residuo de fechamento normalizado (sem verdade)."""
    a = (torch.randn(M.H, generator=gen) * 0.1).requires_grad_(True)
    b0 = torch.zeros(1, requires_grad=True)
    th = torch.tensor([1.0, 1.0, 0.0], requires_grad=True)
    opt = torch.optim.Adam([a, b0, th], 0.01)
    for _ in range(PASSOS_LEITURA):
        num, zs = 0.0, []
        for h0, h1, W, A0, S in trans:
            z0 = h0 @ a + b0
            z1 = h1 @ a + b0
            m = S == 0
            num = num + ((z1 - M.aplica(regra, th, z0, W, A0))[m] ** 2).mean()
            zs.append(z1[m])
        var = torch.cat(zs).var() + 1e-6
        perda = num / len(trans) / var
        opt.zero_grad()
        perda.backward()
        opt.step()
    return a.detach(), b0.detach(), float(perda)


def normaliza(regra, a, b0, trans):
    """z' = (z - z_fonte) / escala; reajusta os coeficientes em z' e arredonda."""
    with torch.no_grad():
        zf = torch.cat([(h1 @ a + b0)[S > 0] for _, h1, _, _, S in trans]).mean()
        zall = torch.cat([(h1 @ a + b0).flatten() for _, h1, _, _, _ in trans])
    th = torch.tensor([1.0, 1.0, 0.0], requires_grad=True)
    opt = torch.optim.Adam([th], 0.02)
    escala = float(zall.std()) + 1e-6

    def zz(h):
        return (h @ a + b0 - zf) / escala
    for _ in range(PASSOS_LEITURA // 2):
        e = 0.0
        for h0, h1, W, A0, S in trans:
            m = S == 0
            e = e + ((zz(h1) - M.aplica(regra, th, zz(h0), W, A0))[m] ** 2).mean()
        opt.zero_grad()
        e.backward()
        opt.step()
    al, be, ce = [float(v) for v in th.detach()]
    if abs(be) > 0.05:  # reescala para que o coeficiente do peso seja a unidade do peso: z'' = z'/be
        escala = escala * be
        ce = ce / be
        be = 1.0
    th2 = [M.snap(al), M.snap(be), M.snap(ce)]
    return th2, (lambda h: (h @ a + b0 - zf) / escala)


def ptr_de(x, fp, W, A0, S):
    sel, f, (pa, pb) = fp
    g = M.termo(f, (pa, pb, 0.0), x.unsqueeze(1).expand_as(W), W)
    g = g.masked_fill(A0 == 0, M.INF if sel == "argmin" else -M.INF)
    p = g.argmin(-1) if sel == "argmin" else g.argmax(-1)
    return torch.where(S > 0, torch.arange(W.shape[1]).expand_as(S), p)


def melhor_programa(cands, fontes, W, A0, S, bom):
    """Circuito fechado: programa x ponteiro; escolha por bom(ponteiro) (maior), empate: inicio, fonte, soma |coef|."""
    melhor, avaliados = None, 0
    for regra, th in cands:
        for fonte in fontes:
            for i, ini in enumerate(M.INICIOS):
                x0 = torch.where(S > 0, torch.full_like(S, fonte), torch.full_like(S, ini))
                x = M.executar(regra, torch.tensor(th, dtype=torch.float), x0, S, W, A0, 64)
                avaliados += 1
                for fp in M.PONTEIROS:
                    c = round(bom(ptr_de(x, fp, W, A0, S)), 6)
                    k = (-c, i, fontes.index(fonte), sum(abs(v) for v in th))
                    if melhor is None or k < melhor[0]:
                        melhor = (k, {"regra": regra, "th": [float(v) for v in th], "ini": ini, "fonte": fonte},
                                  (c, fp[0], fp[1], fp[2]))
    return melhor[1], melhor[2], avaliados


def reconhece_sp(prog, ptr):
    ok_r = tuple(prog["regra"][:2]) == ("min", "lin") and prog["th"] == [1.0, 1.0, 0.0] and prog["ini"] == M.BIG
    ok_p = tuple(ptr[1:3]) == ("argmin", "lin") and tuple(ptr[3]) == (1.0, 1.0)
    return bool(ok_r and ok_p)


def pearson(a, b):
    a = a - a.mean()
    b = b - b.mean()
    return float((a * b).sum() / (a.norm() * b.norm() + 1e-12))


def uma(arg):
    seed, fam, sem_teste = arg
    torch.set_num_threads(1)
    t0 = time.time()
    fi = FAMILIAS.index(fam)
    r = {"seed": seed, "fam": fam}
    net = treinar_ptr(fam, seed * 10 + fi)
    trng = random.Random(sem_teste * 10 + fi)
    with torch.no_grad():
        for n in NS_REDE:
            W, A, S, Y, V, _ = M.lote(fam, N_TESTE, n, trng)
            lg, _, _ = net(W, A, S, n)
            r[f"rede|{n}|ptr"] = M.acuracia_ptr(lg.argmax(-1), V)
    # ---- rota mecanistica (sem verdade)
    xrng = random.Random(sem_teste * 10 + 5 + fi)
    trans = []
    for n in (16, 32):
        W, A, S, Y, V, _ = M.lote(fam, 8, n, xrng)
        hs = trilha(net, W, A, S, 16)
        A0 = A - torch.eye(n)
        for t in range(1, len(hs) - 1):
            trans.append((hs[t], hs[t + 1], W, A0, S))
    gen = torch.Generator().manual_seed(seed * 10 + fi)
    cands, leituras, residuos = [], {}, {}
    for regra in M.REGRAS:
        a, b0, res = ajusta_leitura(regra, trans, gen)
        th, ler = normaliza(regra, a, b0, trans)
        cands.append((regra, th))
        leituras[regra] = ler
        residuos[regra] = res
    W, A, S, Y, V, _ = M.lote(fam, 8, 32, xrng)  # lote de escolha, n = 32
    A0 = A - torch.eye(32)
    with torch.no_grad():
        lg, _, _ = net(W, A, S, 32)
    pr = lg.argmax(-1)
    prog_m, ptr_m, av_m = melhor_programa(cands, (0.0,), W, A0, S, lambda p: (p == pr).float().mean().item())
    # diagnostico pos-escolha: a leitura da regra escolhida contra a variavel verdadeira
    hs = trilha(net, W, A, S, 32)
    with torch.no_grad():
        z = leituras[tuple(prog_m["regra"])](hs[-1])
    m = S == 0
    r["corr_leitura_verdade"] = pearson(z[m], Y[m])
    r["corr_max_18_formas"] = max(abs(pearson(leituras[rg](hs[-1]).detach()[m], Y[m])) for rg in M.REGRAS)
    r["residuo_escolhida"] = residuos[tuple(prog_m["regra"])]
    # ---- sintese direta (sem rede) contra os ponteiros verdadeiros
    todos = [(rg, list(g)) for rg in M.REGRAS for g in M.GRADE]
    prog_s, ptr_s, av_s = melhor_programa(todos, (0.0, 1.0), W, A0, S, lambda p: M.acuracia_ptr(p, V))
    r["avaliados"] = {"mecanistica": av_m, "sintese": av_s}
    for nome, prog, ptr in (("mecanistica", prog_m, ptr_m), ("sintese", prog_s, ptr_s)):
        r[f"{nome}|prog"] = [list(prog["regra"]), prog["th"], prog["ini"], prog["fonte"]]
        r[f"{nome}|ptr"] = [ptr[0], ptr[1], ptr[2], list(ptr[3])]
        r[f"{nome}|reconhece"] = reconhece_sp(prog, ptr) if fam == "SP" else None
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
    teste = [1995, 1996] if QUICK else sementes.derivar(sementes.base_teste(__file__), len(SEMENTES))
    jobs = [(sd, fam, st) for sd, st in zip(SEMENTES, teste) for fam in FAMILIAS]
    with Pool(procs) as pool:
        res = pool.map(uma, jobs)
    json.dump(res, open(os.path.join(AQUI, f"resultados{SUF}.json"), "w"), indent=1, sort_keys=True)
    k = len(SEMENTES)
    L = [f"# E019 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{k} sementes por familia; rede so com ponteiro; rede: {N_TESTE} grafos por n; programa: {N_PROG} grafos por n.", "",
         "| família | quem | n | ponteiro IQM [IC95%] |", "|---|---|---|---|"]

    def linha(fam, quem, n, a):
        lo, hi = estat.bootstrap_ic(a, estat.iqm)
        L.append(f"| {fam} | {quem} | {n} | {estat.iqm(a):.3f} [{lo:.3f},{hi:.3f}] |")
    for fam in FAMILIAS:
        rf = [x for x in res if x["fam"] == fam]
        for n in NS_REDE:
            linha(fam, "rede (só ponteiro)", n, [x[f"rede|{n}|ptr"] for x in rf])
        for nome in ("mecanistica", "sintese"):
            for n in NS_PROG:
                linha(fam, f"programa ({nome})", n, [x[f"{nome}|{n}|ptr"] for x in rf])
    L += ["", "| família | semente | regra mecanística | ponteiro | r(leitura, verdade) | max \\|r\\| nas 18 | síntese | avaliados (mec / sín) |",
          "|---|---|---|---|---|---|---|---|"]
    for x in res:
        L.append(f"| {x['fam']} | {x['seed']} | {x['mecanistica|prog']} | {x['mecanistica|ptr']} | {x['corr_leitura_verdade']:.3f} | "
                 f"{x['corr_max_18_formas']:.3f} | {x['sintese|prog']} {x['sintese|ptr']} | {x['avaliados']['mecanistica']} / {x['avaliados']['sintese']} |")
    sp = [x for x in res if x["fam"] == "SP"]
    wp = [x for x in res if x["fam"] == "WP"]
    L += ["", "## Checagem das previsões (PREVISOES.md, commitadas antes de qualquer piloto)", ""]

    def chk(nome, ok, txt):
        L.append(f"- {nome} {'OK' if ok else 'FALHOU'}: {txt}")
    a64 = estat.iqm([x["rede|64|ptr"] for x in sp])
    chk("P1", a64 >= 0.75, f"rede SP só com ponteiro em n=64 >= 0,75: {a64:.3f}")
    rm = sum(x["mecanistica|reconhece"] for x in sp)
    chk("P2", rm >= 0.8 * k, f"SP mecanística reconhecida em >= 4/5: {rm}/{k}")
    rc = sum(abs(x["corr_leitura_verdade"]) >= 0.9 for x in sp)
    chk("P3", rc >= 0.8 * k, f"SP |r(leitura, distância)| >= 0,9 em >= 4/5: {rc}/{k} ({[round(x['corr_leitura_verdade'], 3) for x in sp]})")
    wc = sum(abs(x["corr_leitura_verdade"]) < 0.5 for x in wp)
    chk("P4", wc >= 0.8 * k, f"WP (controle) |r(leitura, largura)| < 0,5 em >= 4/5: {wc}/{k} ({[round(x['corr_leitura_verdade'], 3) for x in wp]})")
    rs = sum(x["sintese|reconhece"] for x in sp)
    chk("P5", rs >= 0.8 * k, f"SP síntese direta (ponteiros verdadeiros) reconhecida em >= 4/5: {rs}/{k}")
    rec = [x[f"{nm}|256|ptr"] for x in sp for nm in ("mecanistica", "sintese") if x[f"{nm}|reconhece"]]
    chk("P6", bool(rec) and min(rec) == 1.0, f"todo programa reconhecido acerta 1,000 em n=256: min {min(rec) if rec else '-'} ({len(rec)})")
    L.append(f"- Fisher (reconhecimento SP, síntese × mecanística): p = {estat.fisher_exato(rs, k, rm, k):.3f}")
    L.append(f"- CPU total: {sum(x['cpu_s'] for x in res):.0f}s")
    txt = "\n".join(L)
    open(os.path.join(AQUI, f"resultados{SUF}.md"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
