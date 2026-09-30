import sys, random, torch
sys.path.insert(0, "/home/user/Unificando-JEV-E-LLM/experimentos/E018_extracao")
import e018 as E
for fam in ("SP","WP"):
    rng=random.Random(5); W,A,S,Y,V,adjs=E.lote(fam,8,32,rng); A0=A-torch.eye(32)
    print(fam, E.escolher_ptr(Y,A0,W,S,lambda p:E.acuracia_ptr(p,V)))
    net=E.Rede(); net.load_state_dict(torch.load(f"e018_{fam}.pt"))
    with torch.no_grad(): lg,y,_=net(W,A,S,32)
    pr=lg.argmax(-1); print(" rede", E.escolher_ptr(y,A0,W,S,lambda p:(p==pr).float().mean().item()))
