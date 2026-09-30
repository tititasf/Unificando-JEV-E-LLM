import math, random, time
def norm(v):
    n=math.sqrt(sum(x*x for x in v)); return [x/n for x in v]
def onehot(N): return [[1.0 if i==j else 0.0 for j in range(N)] for i in range(N)]
def biort(N):
    L=N//2; C=[]
    for i in range(L):
        e=[0.0]*L; e[i]=1.0; C.append(e); C.append([-x for x in e])
    return C
def binario(N):
    L=int(round(math.log2(N))); return [[(1 if (i>>b)&1 else -1)/math.sqrt(L) for b in range(L)] for i in range(N)]
def aleat(N,L,rng): return [norm([rng.gauss(0,1) for _ in range(L)]) for _ in range(N)]
def treinar(N,L,sig,rng,iters=1500,lote=32,lr=0.05):
    C=aleat(N,L,rng); beta=1/sig**2
    for it in range(iters):
        G=[[0.0]*L for _ in range(N)]
        for _ in range(lote):
            s=rng.randrange(N); r=[c+rng.gauss(0,sig) for c in C[s]]
            lg=[beta*sum(a*b for a,b in zip(c,r)) for c in C]; m=max(lg); e=[math.exp(x-m) for x in lg]; t=sum(e); p=[x/t for x in e]
            for i in range(N):
                g=p[i]-(1 if i==s else 0)
                if abs(g)<1e-9: continue
                Gi=G[i]
                for d in range(L): Gi[d]+=g*beta*r[d]; G[s][d]+=g*beta*C[i][d]
        C=[norm([c-lr*g/lote for c,g in zip(C[i],G[i])]) for i in range(N)]
    return C
def erro(C,sig,rng,n=20000):
    N=len(C); L=len(C[0]); err=0
    for _ in range(n):
        s=rng.randrange(N); r=[c+rng.gauss(0,sig) for c in C[s]]
        k=max(range(N),key=lambda i:sum(a*b for a,b in zip(C[i],r)))
        err+=k!=s
    return err/n
N=16; rng=random.Random(1590)
for sig in (0.3,0.4,0.5):
    print("sig",sig,"onehot",erro(onehot(N),sig,rng),"biort",erro(biort(N),sig,rng),"bin",erro(binario(N),sig,rng))
for L in (4,8):
    t=time.time(); C=treinar(N,L,0.4,rng)
    print("L",L,f"{time.time()-t:.0f}s", " ".join(f"s{sig}: apr {erro(C,sig,rng):.4f} ale {erro(aleat(N,L,rng),sig,rng):.4f}" for sig in (0.3,0.4,0.5)))
