import sys, time, random, torch
sys.argv.append("--x")
sys.path.insert(0, "/home/user/Unificando-JEV-E-LLM/experimentos/E018_extracao")
import e018 as E
fam = sys.argv[1]; E.PASSOS = int(sys.argv[2])
torch.set_num_threads(1)
t0 = time.time()
net = E.treinar(fam, 7)
print(fam, "treino", time.time() - t0, flush=True)
torch.save(net.state_dict(), f"e018_{fam}.pt")
trng = random.Random(3)
with torch.no_grad():
    for n in (16, 32, 64):
        W, A, S, Y, V, _ = E.lote(fam, 32, n, trng)
        lg, y, xs = net(W, A, S, n, trilha=True)
        print(n, E.acuracia_ptr(lg.argmax(-1), V), (y - Y).abs().mean().item(), flush=True)
placar, ptr, x0val, xf = E.extrair(net, fam, random.Random(4))
for p in placar[:5]: print(p)
print(ptr, x0val, xf, time.time() - t0)
