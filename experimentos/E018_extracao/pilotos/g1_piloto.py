"""Piloto G1: MPNN generico (mensagens MLP, agregacao max), sem dicas, em Bellman-Ford. n=16 -> 64."""
import sys, random, time, math
import torch, torch.nn as nn
sys.path.insert(0, '/home/user/Unificando-JEV-E-LLM')
from lab import tarefas_clrs as C
torch.set_num_threads(4)

def lote(B, n, rng):
    W = torch.zeros(B, n, n); A = torch.zeros(B, n, n); S = torch.zeros(B, n)
    D = torch.zeros(B, n); P = torch.zeros(B, n, dtype=torch.long)
    for b in range(B):
        adj, s, pi = C.exemplo("bellman_ford", n, rng)
        d, _ = C.bellman_ford(adj, s)
        for v in range(n):
            for u, w in adj[v]:
                W[b, v, u] = w; A[b, v, u] = 1
        S[b, s] = 1
        D[b] = torch.tensor([x if x < 1e9 else 0.0 for x in d]); P[b] = torch.tensor(pi)
    A = A + torch.eye(n).unsqueeze(0)  # candidato a si mesmo (fonte aponta para si)
    return W, A, S, D, P

def mlp(i, h, o):
    return nn.Sequential(nn.Linear(i, h), nn.ReLU(), nn.Linear(h, o))

class Rede(nn.Module):
    def __init__(s, H=32, agg="max"):
        super().__init__()
        s.H, s.agg = H, agg
        s.enc = nn.Linear(1, H)
        s.msg = mlp(2 * H + 1, H, H)
        s.upd = mlp(2 * H, H, H)
        s.ptr = mlp(2 * H + 1, H, 1)
        s.dist = nn.Linear(H, 1)

    def forward(s, W, A, S, T):
        B, n, _ = W.shape
        h = s.enc(S.unsqueeze(-1))
        Wf = W.unsqueeze(-1)
        for _ in range(T):
            hv = h.unsqueeze(2).expand(B, n, n, s.H); hu = h.unsqueeze(1).expand(B, n, n, s.H)
            m = s.msg(torch.cat([hv, hu, Wf], -1))
            if s.agg == "max":
                m = m.masked_fill(A.unsqueeze(-1) == 0, -1e9).max(2).values
            else:
                m = (m * A.unsqueeze(-1)).sum(2)
            h = s.upd(torch.cat([h, m], -1))
        hv = h.unsqueeze(2).expand(B, n, n, s.H); hu = h.unsqueeze(1).expand(B, n, n, s.H)
        lg = s.ptr(torch.cat([hv, hu, Wf], -1)).squeeze(-1).masked_fill(A == 0, -1e9)
        return lg, s.dist(h).squeeze(-1)

def treinar(agg, seed, passos, usa_dist=True):
    torch.manual_seed(seed); rng = random.Random(seed)
    net = Rede(agg=agg); opt = torch.optim.Adam(net.parameters(), 5e-4)
    dados = [lote(32, 16, rng) for _ in range(100)]
    rv = random.Random(7)
    t0 = time.time()
    for it in range(passos):
        W, A, S, D, P = dados[it % len(dados)]
        T = rng.randint(8, 24)
        lg, dh = net(W, A, S, T)
        loss = nn.functional.cross_entropy(lg.reshape(-1, 16), P.reshape(-1))
        if usa_dist:
            loss = loss + ((dh - D) ** 2).mean()
        opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0); opt.step()
        if (it + 1) % 500 == 0:
            a16 = avaliar(net, 16, random.Random(5), 16)[0]; a64 = avaliar(net, 64, random.Random(5), 64)[0]
            print(f"  it {it+1} loss {loss.item():.3f} n16 {a16:.3f} n64 {a64:.3f}", flush=True)
    return net, time.time() - t0

def avaliar(net, n, rng, T):
    W, A, S, D, P = lote(16, n, rng)
    with torch.no_grad():
        lg, dh = net(W, A, S, T)
    return (lg.argmax(-1) == P).float().mean().item(), (dh - D).abs().mean().item()

if __name__ == "__main__":
    passos = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    for agg in ("max",):
        net, t = treinar(agg, 0, passos)
        r = random.Random(99)
        res = [avaliar(net, n, r, n) for n in (16, 32, 64)]
        print(agg, f"treino {t:.0f}s", " | ".join(f"n={n}: ptr {a:.3f} dist {e:.3f}" for n, (a, e) in zip((16, 32, 64), res)), flush=True)
    torch.save(net.state_dict(), "g1_max.pt")
