from piloto_h13 import *
import sys
rng=random.Random(1591)
for N in (16,32):
    oh={s:erro(onehot(N),s,rng) for s in (0.3,0.4)}
    bo={s:erro(biort(N),s,rng) for s in (0.3,0.4)}
    for L,it,lr,st in ((N//2,4000,0.05,0.4),(N//2,4000,0.02,0.3),(N-1,3000,0.05,0.4)):
        t=time.time(); C=treinar(N,L,st,rng,iters=it,lr=lr)
        e={s:erro(C,s,rng) for s in (0.3,0.4)}
        print(N,L,it,lr,st,f"{time.time()-t:.0f}s"," ".join(f"s{s}: apr {e[s]:.4f} oh {oh[s]:.4f} bo {bo[s]:.4f} r {e[s]/oh[s]:.2f}" for s in e),flush=True)
