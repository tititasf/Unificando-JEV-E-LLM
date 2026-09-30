import sys, time, random, itertools, torch
sys.path.insert(0, "/home/user/Unificando-JEV-E-LLM/experimentos/E018_extracao")
import e018 as E
torch.set_num_threads(1)
BIG = 1e4
INICIOS = (-BIG, 0.0, 1.0, BIG)
GRADE = [(a, b, c) for a in (0, .5, 1, 1.5, 2) for b in (0, .5, 1, 1.5, 2) for c in (-.5, 0, .5)]

def snap(v): return round(v * 2) / 2

def erro(regra, th, fonte, ini, S, W, A0, alvo, T):
    x0 = torch.where(S > 0, torch.full_like(S, fonte), torch.full_like(S, ini))
    x = E.executar(regra, torch.tensor(th), x0, S, W, A0, T)
    return (x - alvo).abs().clamp(max=10).mean().item()

def escolher(cands, fonte, S, W, A0, alvo, T):
    best = None
    for regra, th in cands:
        for ini in INICIOS:
            e = round(erro(regra, th, fonte, ini, S, W, A0, alvo, T), 6)
            k = (e, sum(abs(v) for v in th), abs(ini) > 1, regra, th, ini)
            if best is None or k[:3] < best[:3]:
                best = k
    return best

def ajusta_trans(net, fam, rng):
    trans = []
    with torch.no_grad():
        for n in (16, 32):
            W, A, S, Y, V, _ = E.lote(fam, 16, n, rng)
            _, _, xs = net(W, A, S, n, trilha=True)
            A0 = A - torch.eye(n)
            for t in range(1, len(xs) - 1):
                trans.append((xs[t], xs[t + 1], W, A0, S))
    cands = []
    for regra in E.REGRAS:
        th = torch.tensor([1.0, 1.0, 0.0], requires_grad=True)
        opt = torch.optim.Adam([th], 0.02)
        for _ in range(150):
            e, k = 0.0, 0
            for x, xn, W, A0, S in trans:
                m = S == 0
                e = e + ((E.aplica(regra, th, x, W, A0) - xn)[m] ** 2).sum(); k += int(m.sum())
            l = e / k
            opt.zero_grad(); l.backward(); opt.step()
        cands.append((regra, [snap(float(v)) for v in th.detach()]))
    return cands

if __name__ == "__main__":
    for fam in ("SP", "WP"):
        net = E.Rede(); net.load_state_dict(torch.load(f"e018_{fam}.pt"))
        rng = random.Random(11)
        t0 = time.time()
        W, A, S, Y, V, _ = E.lote(fam, 8, 32, rng)
        A0 = A - torch.eye(32)
        with torch.no_grad():
            lg, yfin, _ = net(W, A, S, 32)
        fonte = snap(float(yfin[S > 0].mean()))
        print(fam, "fonte", fonte)
        mec = escolher(ajusta_trans(net, fam, rng), fonte, S, W, A0, yfin, 64)
        print(" mecanistica", mec, time.time() - t0, flush=True)
        todos = [(r, list(g)) for r in E.REGRAS for g in GRADE]
        comp = escolher(todos, fonte, S, W, A0, yfin, 64)
        print(" comportamental", comp, time.time() - t0, flush=True)
        fonte_v = snap(float(Y[S > 0].mean()))
        sint = escolher(todos, fonte_v, S, W, A0, Y, 64)
        print(" sintese direta", sint, time.time() - t0, flush=True)
