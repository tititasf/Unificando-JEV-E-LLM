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

Tres rotas de extracao, mesma linguagem de regras x_v' = OUT(x_v, AGG_u f(x_u, w_uv)) (18 formas; OUT/AGG em
{min, max, media}; f em {a*x_u + b*w + c, min(a*x_u, b*w) + c, max(a*x_u, b*w) + c}; com/sem manter x_v), inicio
x_fonte = saida arredondada a 1/2, demais em {-inf, +inf, 0, 1}, escolha em circuito fechado (64 passos, n = 32):
  mecanistica:    coeficientes ajustados nas transicoes x^t -> x^t+1 decodificadas da rede (x^t = Linear(h^t)),
                  arredondados a 1/2 (Occam); vence o menor erro contra a saida final da rede;
  comportamental: grade de coeficientes {0,.5,1,1.5,2}^2 x {-.5,0,.5}; alvo = saida final da rede;
  sintese direta: a mesma grade, alvo = a VERDADE (sem rede) -- o atalho trivial que um revisor proporia.
Empate: inicio que nada supoe (+-inf) primeiro, depois menor soma |coef|.
Ponteiro: argmin/argmax_u g(x_u, w) na mesma linguagem, pela concordancia com a rede (ou com os pais validos, na sintese).
Programa = (inicio, regra, ponteiro), executado em Python puro contra o resolvedor exato em n = 16, 64, 256.
"Prova para todo n": se o programa e SINTATICAMENTE a relaxacao do semianel da familia com inicio correto
(SP: fonte 0, demais +inf; WP: fonte 1, demais 0 ou -inf), vale o teorema classico (ponto fixo de Bellman-Ford
generalizado em semianel; convergencia monotona). Reconhecimento automatico por forma e coeficientes exatos.
E prova por reducao a teorema conhecido, nao prova formal em assistente de provas (declarado).
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


BIG = 1e4
INICIOS = (-BIG, BIG, 0.0, 1.0)  # ordem = preferencia no empate: inicio que nada supoe (+-infinito) primeiro
GRADE = [(a, b, c) for a in (0, .5, 1, 1.5, 2) for b in (0, .5, 1, 1.5, 2) for c in (-.5, 0, .5)]
PONTEIROS = [(sel, f, ab) for sel in ("argmin", "argmax") for f in ("lin", "minf", "maxf")
             for ab in ((1.0, 1.0), (1.0, 0.0), (0.0, 1.0))]


def snap(v):
    return round(v * 2) / 2


def erro_prog(regra, th, fonte, ini, S, W, A0, alvo, T):
    x0 = torch.where(S > 0, torch.full_like(S, fonte), torch.full_like(S, ini))
    x = executar(regra, torch.tensor(th, dtype=torch.float), x0, S, W, A0, T)
    return (x - alvo).abs().clamp(max=10).mean().item()


def escolher(cands, fonte, S, W, A0, alvo, T):
    """Circuito fechado: menor erro contra o alvo; empate -> inicio preferido, depois menor soma |coef|."""
    melhor = None
    for regra, th in cands:
        for i, ini in enumerate(INICIOS):
            e = round(erro_prog(regra, th, fonte, ini, S, W, A0, alvo, T), 6)
            k = (e, i, sum(abs(v) for v in th))
            if melhor is None or k < melhor[0]:
                melhor = (k, regra, [float(v) for v in th], ini)
    return {"erro": melhor[0][0], "regra": melhor[1], "th": melhor[2], "ini": melhor[3], "fonte": fonte}


def ajusta_transicoes(net, fam, rng):
    """Extracao mecanistica: coeficientes ajustados nas transicoes x^t -> x^t+1 decodificadas da rede."""
    trans = []
    with torch.no_grad():
        for n in (16, 32):
            W, A, S, Y, V, _ = lote(fam, 16, n, rng)
            _, _, xs = net(W, A, S, n, trilha=True)
            A0 = A - torch.eye(n)
            for t in range(1, len(xs) - 1):
                trans.append((xs[t], xs[t + 1], W, A0, S))
    cands = []
    for regra in REGRAS:
        th = torch.tensor([1.0, 1.0, 0.0], requires_grad=True)
        opt = torch.optim.Adam([th], 0.02)
        for _ in range(150):
            e, k = 0.0, 0
            for x, xn, W, A0, S in trans:
                m = S == 0
                e = e + ((aplica(regra, th, x, W, A0) - xn)[m] ** 2).sum()
                k += int(m.sum())
            opt.zero_grad()
            (e / k).backward()
            opt.step()
        cands.append((regra, [snap(float(v)) for v in th.detach()]))
    return cands


def escolher_ptr(valores, A0, W, S, bom):
    """bom(p) -> fracao de acerto do ponteiro p (contra a rede ou contra os pais validos).
    Como no programa: a fonte aponta para si; os demais escolhem entre os vizinhos."""
    melhor = None
    eu = torch.arange(W.shape[1]).expand_as(S)
    for sel, f, (a, b) in PONTEIROS:
        g = termo(f, (a, b, 0.0), valores.unsqueeze(1).expand_as(W), W)
        g = g.masked_fill(A0 == 0, INF if sel == "argmin" else -INF)
        p = g.argmin(-1) if sel == "argmin" else g.argmax(-1)
        p = torch.where(S > 0, eu, p)
        c = round(bom(p), 6)
        if melhor is None or c > melhor[0]:
            melhor = (c, sel, f, (a, b))
    return melhor


def reconhece(fam, prog, ptr):
    """Reconhecimento automatico da relaxacao do semianel da familia, com inicio que a torna correta para todo grafo:
    SP (min,+): x_s = 0, demais = +inf;  WP (max,min): x_s = 1, demais = 0 ou -inf (pesos em (0,1))."""
    r, th, ini, fonte = prog["regra"], prog["th"], prog["ini"], prog["fonte"]
    if fam == "SP":
        ok_r = tuple(r[:2]) == ("min", "lin") and th == [1.0, 1.0, 0.0] and fonte == 0.0 and ini == BIG
        ok_p = tuple(ptr[1:3]) == ("argmin", "lin") and tuple(ptr[3]) == (1.0, 1.0)
    else:
        ok_r = tuple(r[:2]) == ("max", "minf") and th == [1.0, 1.0, 0.0] and fonte == 1.0 and ini in (0.0, -BIG)
        # argmax min(x_u, w) ou argmax w: a aresta mais pesada de v sempre leva a um pai valido
        # (c_v <= w_max e c_u* >= min(c_v, w_max) = c_v); e o atalho da arvore geradora maxima
        ok_p = (tuple(ptr[1:3]) == ("argmax", "minf") and tuple(ptr[3]) == (1.0, 1.0)) or \
            (ptr[1] == "argmax" and ptr[2] in ("lin", "maxf") and tuple(ptr[3]) == (0.0, 1.0))
    return ok_r, ok_p


def programa(prog, ptr, adj, s):
    """Executa o programa extraido em Python puro (sem a rede) ate o ponto fixo."""
    n = len(adj)
    o, f, k = prog["regra"]
    a, b, c = prog["th"]
    x = [prog["ini"]] * n
    x[s] = prog["fonte"]

    def t(xu, w, a=a, b=b, c=c, f=f):
        return a * xu + b * w + c if f == "lin" else (min(a * xu, b * w) + c if f == "minf" else max(a * xu, b * w) + c)
    for _ in range(4 * n):
        nx = list(x)
        for v in range(n):
            if v == s or not adj[v]:
                continue
            ts = [t(x[u], w) for u, w in adj[v]]
            r = min(ts) if o == "min" else (max(ts) if o == "max" else sum(ts) / len(ts))
            if k:
                r = min(r, x[v]) if o == "min" else (max(r, x[v]) if o == "max" else (r + x[v]) / 2)
            nx[v] = r
        if max(abs(p - q) for p, q in zip(nx, x)) < 1e-12:
            break
        x = nx
    _, sel, fp, (pa, pb) = ptr
    pi = list(range(n))
    for v in range(n):
        if v == s or not adj[v]:
            continue
        sc = [(t(x[u], w, pa, pb, 0.0, fp), u) for u, w in adj[v]]
        pi[v] = min(sc)[1] if sel == "argmin" else max(sc, key=lambda z: (z[0], -z[1]))[1]
    return x, pi


METODOS = ("mecanistica", "comportamental", "sintese")


def uma(arg):
    seed, fam, sem_teste = arg
    torch.set_num_threads(1)
    t0 = time.time()
    r = {"seed": seed, "fam": fam}
    net = treinar(fam, seed * 10 + FAMILIAS.index(fam))
    trng = random.Random(sem_teste * 10 + FAMILIAS.index(fam))
    with torch.no_grad():
        for n in NS_REDE:
            W, A, S, Y, V, _ = lote(fam, N_TESTE, n, trng)
            lg, y, _ = net(W, A, S, n)
            r[f"rede|{n}|ptr"] = acuracia_ptr(lg.argmax(-1), V)
            r[f"rede|{n}|erro_val"] = (y - Y).abs().mean().item()
    xrng = random.Random(sem_teste * 10 + 5 + FAMILIAS.index(fam))
    cands = ajusta_transicoes(net, fam, xrng)
    W, A, S, Y, V, _ = lote(fam, 8, 32, xrng)  # lote de escolha (n = 32, fora do treino)
    A0 = A - torch.eye(32)
    with torch.no_grad():
        lg, yfin, _ = net(W, A, S, 32)
    pr = lg.argmax(-1)
    fonte_rede = snap(float(yfin[S > 0].mean()))
    todos = [(rg, list(g)) for rg in REGRAS for g in GRADE]
    progs = {
        "mecanistica": escolher(cands, fonte_rede, S, W, A0, yfin, 64),
        "comportamental": escolher(todos, fonte_rede, S, W, A0, yfin, 64),
        "sintese": escolher(todos, snap(float(Y[S > 0].mean())), S, W, A0, Y, 64),  # sem rede: verdade direta
    }
    ptr_rede = escolher_ptr(yfin, A0, W, S, lambda p: (p == pr).float().mean().item())
    ptr_sint = escolher_ptr(Y, A0, W, S, lambda p: acuracia_ptr(p, V))
    # diagnostico: erro do programa do semianel contra a saida da rede (fidelidade rede -> algoritmo)
    certo = ({"regra": ("min", "lin", True), "th": [1.0, 1.0, 0.0], "ini": BIG, "fonte": 0.0} if fam == "SP" else
             {"regra": ("max", "minf", True), "th": [1.0, 1.0, 0.0], "ini": 0.0, "fonte": 1.0})
    r["erro_semianel_vs_rede"] = erro_prog(certo["regra"], certo["th"], certo["fonte"], certo["ini"], S, W, A0, yfin, 64)
    for m in METODOS:
        ptr = ptr_sint if m == "sintese" else ptr_rede
        ok_r, ok_p = reconhece(fam, progs[m], ptr)
        pg = progs[m]
        r[f"{m}|prog"] = [list(pg["regra"]), pg["th"], pg["ini"], pg["fonte"], pg["erro"]]
        r[f"{m}|ptr"] = [ptr[0], ptr[1], ptr[2], list(ptr[3])]
        r[f"{m}|reconhece"] = bool(ok_r and ok_p)
        r[f"{m}|reconhece_regra"] = bool(ok_r)
        prng = random.Random(sem_teste * 10 + 7 + FAMILIAS.index(fam))
        for n in NS_PROG:
            accs = []
            for _ in range(N_PROG):
                adj = C.grafo_er(n, 0.5, prng, pesos=True)
                s = prng.randrange(n)
                _, val = verdade(fam, adj, s)
                _, pi = programa(pg, ptr, adj, s)
                accs.append(sum(pi[v] in val[v] for v in range(n)) / n)
            r[f"{m}|{n}|ptr"] = sum(accs) / len(accs)
    r["cpu_s"] = time.time() - t0
    print(f"{fam} semente {seed} ok ({r['cpu_s']:.0f}s)", flush=True)
    return r


def main():
    procs = next((int(a.split("=")[1]) for a in sys.argv if a.startswith("--procs=")), 4)
    teste = [1895, 1896] if QUICK else sementes.derivar(sementes.base_teste(__file__), len(SEMENTES))
    jobs = [(sd, fam, st) for sd, st in zip(SEMENTES, teste) for fam in FAMILIAS]
    with Pool(procs) as pool:
        res = pool.map(uma, jobs)
    json.dump(res, open(os.path.join(AQUI, f"resultados{SUF}.json"), "w"), indent=1, sort_keys=True)
    k = len(SEMENTES)
    L = [f"# E018 - resultados {'(SMOKE, nao vale)' if QUICK else ''}", "",
         f"{k} sementes por familia; rede: {N_TESTE} grafos por n; programa: {N_PROG} grafos por n.", "",
         "| família | quem | n | ponteiro IQM [IC95%] |", "|---|---|---|---|"]

    def linha(fam, quem, n, a):
        lo, hi = estat.bootstrap_ic(a, estat.iqm)
        L.append(f"| {fam} | {quem} | {n} | {estat.iqm(a):.3f} [{lo:.3f},{hi:.3f}] |")
    rec = {}
    for fam in FAMILIAS:
        rf = [x for x in res if x["fam"] == fam]
        for n in NS_REDE:
            linha(fam, "rede", n, [x[f"rede|{n}|ptr"] for x in rf])
        for m in METODOS:
            for n in NS_PROG:
                linha(fam, f"programa ({m})", n, [x[f"{m}|{n}|ptr"] for x in rf])
            rec[fam, m] = sum(x[f"{m}|reconhece"] for x in rf)
    L += ["", "| família | método | reconhecido (regra+ponteiro+início) | só a regra |", "|---|---|---|---|"]
    for fam in FAMILIAS:
        rf = [x for x in res if x["fam"] == fam]
        for m in METODOS:
            L.append(f"| {fam} | {m} | {rec[fam, m]}/{k} | {sum(x[f'{m}|reconhece_regra'] for x in rf)}/{k} |")
    L.append("")
    for x in res:
        L.append(f"- {x['fam']} {x['seed']}: " + " | ".join(f"{m}: {x[f'{m}|prog']} ptr {x[f'{m}|ptr']}" for m in METODOS)
                 + f" | erro do semianel contra a rede {x['erro_semianel_vs_rede']:.4f}")
    L += ["", "## Checagem das previsões", ""]

    def chk(nome, ok, txt):
        L.append(f"- {nome} {'OK' if ok else 'FALHOU'}: {txt}")
    for fam in FAMILIAS:
        chk(f"P1 {fam}", rec[fam, "sintese"] >= 0.8 * k, f"síntese direta (sem rede) reconhecida em >= 80%: {rec[fam, 'sintese']}/{k}")
    for fam in FAMILIAS:
        chk(f"P2 {fam}", rec[fam, "comportamental"] >= 0.8 * k, f"extração comportamental da rede reconhecida em >= 80%: {rec[fam, 'comportamental']}/{k}")
    for fam in FAMILIAS:
        chk(f"P3 {fam}", rec[fam, "mecanistica"] >= 0.8 * k, f"extração mecanística da rede reconhecida em >= 80%: {rec[fam, 'mecanistica']}/{k}")
    reconh = [x[f"{m}|256|ptr"] for x in res for m in METODOS if x[f"{m}|reconhece"]]
    chk("P4", bool(reconh) and min(reconh) == 1.0, f"todo programa reconhecido acerta 1,000 em n=256: min {min(reconh) if reconh else '-'} ({len(reconh)} programas)")
    for fam in FAMILIAS:
        a64 = estat.iqm([x["rede|64|ptr"] for x in res if x["fam"] == fam])
        chk(f"P5 {fam}", a64 < 0.99, f"a própria rede fica < 0,99 em n=64: {a64:.3f}")
    rn = sum(rec[f, m] for f in FAMILIAS for m in ("comportamental", "mecanistica")) / 2
    rs = sum(rec[f, "sintese"] for f in FAMILIAS)
    p = estat.fisher_exato(rs, 2 * k, sum(rec[f, "comportamental"] for f in FAMILIAS), 2 * k)
    chk("P6", rs > sum(rec[f, "comportamental"] for f in FAMILIAS),
        f"a síntese direta reconhece mais que a melhor extração da rede (comportamental), somando as famílias: "
        f"{rs}/{2 * k} contra {sum(rec[f, 'comportamental'] for f in FAMILIAS)}/{2 * k} (Fisher p = {p:.3f}); média rede {rn:.1f}")
    L.append(f"- CPU total: {sum(x['cpu_s'] for x in res):.0f}s")
    txt = "\n".join(L)
    open(os.path.join(AQUI, f"resultados{SUF}.md"), "w").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
