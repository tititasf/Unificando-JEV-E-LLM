"""
E018 - G1: rede generica sem dicas -> regra extraida automaticamente -> programa correto para todo n.

Familias (duas algebras diferentes):
  SP  caminho minimo      (min, +):   verdade d_v = min sobre caminhos da soma dos pesos; d_s = 0
  WP  caminho mais largo  (max, min): verdade c_v = max sobre caminhos do menor peso;   c_s = 1 (pesos em (0,1))
Grafos Erdos-Renyi p = 0,5, pesos U(0,1), nao direcionados (lab/tarefas_clrs.grafo_er).

Rede (identica nas duas familias; nada do algoritmo e dado):
  h0 = Linear(is_fonte); T passos de  m_v = max_u MLP([h_v, h_u, w_uv]);  h_v = MLP([h_v, m_v])
  saidas: valor por no (Linear(h)) e ponteiro (softmax sobre vizinhos e o proprio no de MLP([h_v,h_u,w])).
  Treino so com entrada -> saida (valor + ponteiro), SEM dicas (sem trajetoria do algoritmo);
  n = 16, T ~ U{8..24}, Adam 5e-4, corte de gradiente 1,0, 4000 passos, lote 32 (100 lotes fixos).

Extracao automatica (sem olhar a familia):
  1. sonda: o valor decodificado do estado a cada passo, x^t = Linear(h^t), vira o estado simbolico;
  2. linguagem de regras: x_v' = OUT( x_v, AGG_u f(x_u, w_uv) ), OUT/AGG em {min, max, media},
     f em {a*x_u + b*w + c, min(a*x_u, b*w) + c, max(a*x_u, b*w) + c}  -> 18 formas, 3 coeficientes;
  3. ajuste dos coeficientes nas transicoes observadas da rede (n = 16 e 32);
  4. arredondamento de Occam: coeficientes para o multiplo de 1/2 mais proximo;
  5. escolha em CIRCUITO FECHADO: cada regra arredondada e executada a partir do estado inicial exato
     (fonte = x_fonte decodificado, demais = valor decodificado de h0) por n passos em grafos novos; vence o
     menor erro contra a saida final da propria rede. (A verdade do algoritmo NAO entra na escolha.)
  6. ponteiro extraido: argmin/argmax_u g(x_u, w) com g na mesma linguagem, escolhido pela concordancia com
     os ponteiros da rede.
Programa extraido = (inicio, regra, ponteiro). Avaliado contra o resolvedor exato em n = 16, 64, 256.
"Prova para todo n": se a regra arredondada e SINTATICAMENTE a relaxacao do semianel da familia
((min,+) ou (max,min)) com inicio correto, vale o teorema classico (Bellman-Ford generalizado em semianel);
o reconhecimento e automatico (comparacao de forma e coeficientes exatos). Isto e prova por reducao a
teorema conhecido, nao prova formal em assistente de provas (declarado).
Uso: python3 e018.py [--quick] [--procs=4]
"""
import itertools
import json
import os
import random
import sys
import time
from multiprocessing import Pool

import torch
import torch.nn as nn

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, RAIZ)
from lab import estat, sementes  # noqa: E402
from lab import tarefas_clrs as C  # noqa: E402

QUICK = "--quick" in sys.argv
SEMENTES = [1890, 1891] if QUICK else list(range(1800, 1805))
FAMILIAS = ("SP", "WP")
PASSOS = 300 if QUICK else 4000
NS_REDE = (16, 32, 64)
NS_PROG = (16, 64, 256)
N_TESTE = 16 if QUICK else 64  # grafos por n para a rede
N_PROG = 4 if QUICK else 20    # grafos por n para o programa extraido
SUF = "_smoke" if QUICK else ""
H = 32
INF = 1e9


# ------------------------------------------------------------ verdade
def verdade(fam, adj, s):
    n = len(adj)
    if fam == "SP":
        d, pi = C.bellman_ford(adj, s)
        return [x if x < INF else 0.0 for x in d], [[p] for p in pi]
    c = [0.0] * n  # caminho mais largo: Dijkstra de gargalo (max-min)
    c[s] = 1.0
    feito = [False] * n
    for _ in range(n):
        v = max((i for i in range(n) if not feito[i]), key=lambda i: c[i])
        feito[v] = True
        for u, w in adj[v]:
            if not feito[u] and min(c[v], w) > c[u]:
                c[u] = min(c[v], w)
    validos = []
    for v in range(n):
        if v == s or c[v] == 0.0:
            validos.append([v])
        else:
            validos.append([u for u, w in adj[v] if abs(min(c[u], w) - c[v]) < 1e-12])
    return c, validos


def lote(fam, B, n, rng):
    W = torch.zeros(B, n, n)
    A = torch.zeros(B, n, n)
    S = torch.zeros(B, n)
    Y = torch.zeros(B, n)
    V = torch.zeros(B, n, n)  # pais validos
    adjs = []
    for b in range(B):
        adj = C.grafo_er(n, 0.5, rng, pesos=True)
        s = rng.randrange(n)
        y, val = verdade(fam, adj, s)
        for v in range(n):
            for u, w in adj[v]:
                W[b, v, u] = w
                A[b, v, u] = 1
            for u in val[v]:
                V[b, v, u] = 1
        S[b, s] = 1
        Y[b] = torch.tensor(y)
        adjs.append((adj, s))
    return W, A + torch.eye(n), S, Y, V, adjs


# ------------------------------------------------------------ rede generica
def mlp(i, o):
    return nn.Sequential(nn.Linear(i, H), nn.ReLU(), nn.Linear(H, o))


class Rede(nn.Module):
    def __init__(self):
        super().__init__()
        self.enc = nn.Linear(1, H)
        self.msg = mlp(2 * H + 1, H)
        self.upd = mlp(2 * H, H)
        self.ptr = mlp(2 * H + 1, 1)
        self.val = nn.Linear(H, 1)

    def passo(self, h, W, A):
        B, n, _ = W.shape
        hv = h.unsqueeze(2).expand(B, n, n, H)
        hu = h.unsqueeze(1).expand(B, n, n, H)
        m = self.msg(torch.cat([hv, hu, W.unsqueeze(-1)], -1)).masked_fill(A.unsqueeze(-1) == 0, -INF).max(2).values
        return self.upd(torch.cat([h, m], -1))

    def forward(self, W, A, S, T, trilha=False):
        h = self.enc(S.unsqueeze(-1))
        xs = [self.val(h).squeeze(-1)]
        for _ in range(T):
            h = self.passo(h, W, A)
            if trilha:
                xs.append(self.val(h).squeeze(-1))
        B, n, _ = W.shape
        hv = h.unsqueeze(2).expand(B, n, n, H)
        hu = h.unsqueeze(1).expand(B, n, n, H)
        lg = self.ptr(torch.cat([hv, hu, W.unsqueeze(-1)], -1)).squeeze(-1).masked_fill(A == 0, -INF)
        return lg, self.val(h).squeeze(-1), xs


def treinar(fam, seed):
    torch.manual_seed(seed)
    rng = random.Random(seed)
    net = Rede()
    opt = torch.optim.Adam(net.parameters(), 5e-4)
    dados = [lote(fam, 32, C.N_TREINO, rng) for _ in range(100)]
    for it in range(PASSOS):
        W, A, S, Y, V, _ = dados[it % len(dados)]
        lg, y, _ = net(W, A, S, rng.randint(8, 24))
        lp = torch.log_softmax(lg, -1)
        perda_ptr = -torch.logsumexp(lp.masked_fill(V == 0, -INF), -1).mean()
        perda = perda_ptr + ((y - Y) ** 2).mean()
        opt.zero_grad()
        perda.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
        opt.step()
    return net


def acuracia_ptr(pred, V):
    return V.gather(-1, pred.unsqueeze(-1)).squeeze(-1).mean().item()


# ------------------------------------------------------------ linguagem de regras
FORMAS = list(itertools.product(("min", "max", "media"), ("lin", "minf", "maxf")))
FORMAS = [(o, f) for o, f in FORMAS]  # OUT = AGG (mesmo agregador dentro e fora): 9 formas x com/sem manter = 18
REGRAS = [(o, f, k) for (o, f) in FORMAS for k in (True, False)]


def termo(f, th, xu, Wm):
    a, b, c = th
    if f == "lin":
        return a * xu + b * Wm + c
    if f == "minf":
        return torch.minimum(a * xu, b * Wm) + c
    return torch.maximum(a * xu, b * Wm) + c


def aplica(regra, th, x, W, A0):
    o, f, k = regra
    t = termo(f, th, x.unsqueeze(1).expand_as(W), W)
    if o == "min":
        r = t.masked_fill(A0 == 0, INF).min(2).values
        return torch.minimum(r, x) if k else r
    if o == "max":
        r = t.masked_fill(A0 == 0, -INF).max(2).values
        return torch.maximum(r, x) if k else r
    r = (t * A0).sum(2) / A0.sum(2).clamp(min=1)
    return (r + x) / 2 if k else r


def executar(regra, th, x0, S, W, A0, T):
    x = x0.clone()
    for _ in range(T):
        x = torch.where(S > 0, x0, aplica(regra, th, x, W, A0))
    return x


def extrair(net, fam, rng):
    trans = []
    with torch.no_grad():
        for n in (16, 32):
            W, A, S, Y, V, _ = lote(fam, 16, n, rng)
            _, _, xs = net(W, A, S, n, trilha=True)
            A0 = A - torch.eye(n)
            for t in range(1, len(xs) - 1):
                trans.append((xs[t], xs[t + 1], W, A0, S))

    def mse(regra, th):
        e, k = 0.0, 0
        for x, xn, W, A0, S in trans:
            m = S == 0
            e = e + ((aplica(regra, th, x, W, A0) - xn)[m] ** 2).sum()
            k += int(m.sum())
        return e / k

    cands = []
    for regra in REGRAS:
        th = torch.tensor([1.0, 1.0, 0.0], requires_grad=True)
        opt = torch.optim.Adam([th], 0.02)
        for _ in range(150):
            l = mse(regra, th)
            opt.zero_grad()
            l.backward()
            opt.step()
        arred = [round(float(v) * 2) / 2 for v in th.detach()]
        cands.append((regra, arred))
    # escolha em circuito fechado contra a saida final da rede (grafos novos, n = 32)
    with torch.no_grad():
        W, A, S, Y, V, _ = lote(fam, 16, 32, rng)
        _, yfin, xs = net(W, A, S, 32, trilha=True)
        x0 = torch.where(S > 0, xs[0], xs[0][S == 0].mean())
        A0 = A - torch.eye(32)
        placar = []
        for regra, th in cands:
            e = ((executar(regra, torch.tensor(th), x0, S, W, A0, 32) - yfin) ** 2).mean().item()
            placar.append((e, regra, th))
        placar.sort(key=lambda z: z[0])
        # ponteiro: argmin/argmax de g(x_u, w) concordando com a rede
        lg, _, _ = net(W, A, S, 32)
        pr = lg.argmax(-1)
        melhor_p = None
        for sel, f in itertools.product(("argmin", "argmax"), ("lin", "minf", "maxf")):
            for a, b in ((1.0, 1.0), (1.0, 0.0), (0.0, 1.0)):
                g = termo(f, (a, b, 0.0), yfin.unsqueeze(1).expand_as(W), W)
                g = g.masked_fill(A == 0, INF if sel == "argmin" else -INF)
                p = g.argmin(-1) if sel == "argmin" else g.argmax(-1)
                conc = (p == pr).float().mean().item()
                if melhor_p is None or conc > melhor_p[0]:
                    melhor_p = (conc, sel, f, (a, b))
    x0val = float(xs[0][S == 0].mean())
    xs_fonte = float(xs[0][S > 0].mean())
    return placar, melhor_p, x0val, xs_fonte


def reconhece(fam, regra, th, ptr):
    """Reconhecimento automatico da relaxacao do semianel da familia (coeficientes exatos)."""
    if fam == "SP":
        ok_r = regra == ("min", "lin", True) and th == [1.0, 1.0, 0.0]
        ok_p = ptr[1:] == ("argmin", "lin", (1.0, 1.0))
    else:
        ok_r = regra == ("max", "minf", True) and th == [1.0, 1.0, 0.0]
        ok_p = ptr[1:] == ("argmax", "minf", (1.0, 1.0))
    return ok_r, ok_p


def programa(regra, th, ptr, x0val, xfonte, adj, s):
    """Executa o programa extraido em Python puro (sem a rede) ate o ponto fixo."""
    n = len(adj)
    o, f, k = regra
    x = [x0val] * n
    x[s] = xfonte  # valor da fonte decodificado da rede e arredondado (Occam), nao dado pela familia
    a, b, c = th

    def t(xu, w):
        return a * xu + b * w + c if f == "lin" else (min(a * xu, b * w) + c if f == "minf" else max(a * xu, b * w) + c)
    for _ in range(4 * n):
        nx = list(x)
        for v in range(n):
            if v == s or not adj[v]:
                continue
            ts = [t(x[u], w) for u, w in adj[v]]
            r = min(ts) if o == "min" else (max(ts) if o == "max" else sum(ts) / len(ts))
            nx[v] = (min(r, x[v]) if o == "min" else max(r, x[v]) if o == "max" else (r + x[v]) / 2) if k else r
        if max(abs(p - q) for p, q in zip(nx, x)) < 1e-12:
            break
        x = nx
    _, sel, fp, (pa, pb) = ptr
    pi = list(range(n))
    for v in range(n):
        if v == s or not adj[v]:
            continue
        sc = [(t2 if True else 0, u) for u, t2 in ((u, (pa * x[u] + pb * w) if fp == "lin" else
                                                     (min(pa * x[u], pb * w) if fp == "minf" else max(pa * x[u], pb * w)))
                                                    for u, w in adj[v])]
        pi[v] = (min(sc) if sel == "argmin" else max(sc, key=lambda z: (z[0], -z[1])))[1]
    return x, pi


def uma(arg):
    seed, sem_teste = arg
    torch.set_num_threads(1)
    t0 = time.time()
    r = {"seed": seed}
    for fam in FAMILIAS:
        net = treinar(fam, seed * 10 + FAMILIAS.index(fam))
        trng = random.Random(sem_teste * 10 + FAMILIAS.index(fam))
        with torch.no_grad():
            for n in NS_REDE:
                W, A, S, Y, V, _ = lote(fam, N_TESTE, n, trng)
                lg, y, _ = net(W, A, S, n)
                r[f"{fam}|rede|{n}|ptr"] = acuracia_ptr(lg.argmax(-1), V)
                r[f"{fam}|rede|{n}|erro_val"] = (y - Y).abs().mean().item()
        placar, ptr, x0val, xf = extrair(net, fam, random.Random(sem_teste * 10 + 5 + FAMILIAS.index(fam)))
        e, regra, th = placar[0]
        ok_r, ok_p = reconhece(fam, regra, th, ptr)
        r[f"{fam}|regra"] = [list(regra), th, e]
        r[f"{fam}|segunda"] = [list(placar[1][1]), placar[1][2], placar[1][0]]
        r[f"{fam}|ptr_extraido"] = [ptr[0], ptr[1], ptr[2], list(ptr[3])]
        r[f"{fam}|reconhece_regra"] = ok_r
        r[f"{fam}|reconhece_ptr"] = ok_p
        r[f"{fam}|inicio"] = [x0val, xf]
        for n in NS_PROG:
            accs = []
            for _ in range(N_PROG):
                adj = C.grafo_er(n, 0.5, trng, pesos=True)
                s = trng.randrange(n)
                y, val = verdade(fam, adj, s)
                _, pi = programa(regra, th, ptr, x0val, round(xf * 2) / 2, adj, s)
                accs.append(sum(pi[v] in val[v] for v in range(n)) / n)
            r[f"{fam}|prog|{n}|ptr"] = sum(accs) / len(accs)
    r["cpu_s"] = time.time() - t0
    print(f"semente {seed} ok ({r['cpu_s']:.0f}s)", flush=True)
    return r


def main():
    procs = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--procs=")), 4)
    teste = [1895, 1896] if QUICK else sementes.derivar(sementes.base_teste(__file__), len(SEMENTES))
    with Pool(procs) as pool:
        res = pool.map(uma, list(zip(SEMENTES, teste)))
    json.dump(res, open(os.path.join(AQUI, f"resultados{SUF}.json"), "w"), indent=1, sort_keys=True)

    def col(c):
        return [x[c] for x in res]
    L = [f"# E018 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{len(SEMENTES)} sementes; rede: {N_TESTE} grafos por n; programa: {N_PROG} grafos por n.", "",
         "| família | quem | n | ponteiro IQM [IC95%] |", "|---|---|---|---|"]
    for fam in FAMILIAS:
        for n in NS_REDE:
            a = col(f"{fam}|rede|{n}|ptr")
            lo, hi = estat.bootstrap_ic(a, estat.iqm)
            L.append(f"| {fam} | rede | {n} | {estat.iqm(a):.3f} [{lo:.3f},{hi:.3f}] |")
        for n in NS_PROG:
            a = col(f"{fam}|prog|{n}|ptr")
            lo, hi = estat.bootstrap_ic(a, estat.iqm)
            L.append(f"| {fam} | programa extraído | {n} | {estat.iqm(a):.3f} [{lo:.3f},{hi:.3f}] |")
    L.append("")
    for fam in FAMILIAS:
        for x in res:
            L.append(f"- {fam} semente {x['seed']}: regra {x[f'{fam}|regra']} | 2a {x[f'{fam}|segunda']} | "
                     f"ponteiro {x[f'{fam}|ptr_extraido']} | reconhece regra {x[f'{fam}|reconhece_regra']} ptr {x[f'{fam}|reconhece_ptr']}")
    L += ["", "## Checagem das previsões", ""]
    k = len(SEMENTES)
    rec = {fam: sum(x[f"{fam}|reconhece_regra"] and x[f"{fam}|reconhece_ptr"] for x in res) for fam in FAMILIAS}
    for fam in FAMILIAS:
        L.append(f"- P1 {fam} {'OK' if rec[fam] >= 0.8 * k else 'FALHOU'}: regra e ponteiro reconhecidos como a relaxação do semianel em >= 80% das sementes: {rec[fam]}/{k}")
    for fam in FAMILIAS:
        prog = [x[f"{fam}|prog|256|ptr"] for x in res if x[f"{fam}|reconhece_regra"] and x[f"{fam}|reconhece_ptr"]]
        ok = bool(prog) and min(prog) == 1.0
        L.append(f"- P2 {fam} {'OK' if ok else 'FALHOU'}: programa reconhecido acerta 1,000 em n=256 em toda semente reconhecida: {prog}")
    for fam in FAMILIAS:
        a64 = estat.iqm(col(f"{fam}|rede|64|ptr"))
        L.append(f"- P3 {fam} {'OK' if a64 < 0.99 else 'FALHOU'}: a própria rede fica < 0,99 em n=64 (o programa extraído supera a rede): {a64:.3f}")
    sp_ok = estat.iqm(col("SP|rede|64|ptr"))
    L.append(f"- P4 {'OK' if sp_ok >= 0.75 else 'FALHOU'}: rede SP em n=64 >= 0,75 (a rede genérica aprendeu algo extrapolável): {sp_ok:.3f}")
    L.append(f"- CPU total: {sum(col('cpu_s')):.0f}s")
    txt = "\n".join(L)
    open(os.path.join(AQUI, f"resultados{SUF}.md"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
