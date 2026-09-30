import math, random, sys, time, os
R="/home/user/Unificando-JEV-E-LLM"
sys.path.insert(0,R); sys.path.insert(0,R+"/experimentos/E005_t2_salto"); sys.path.insert(0,R+"/experimentos/E006_lei_margem")
import tarefa_t2 as T2, passo_rapido as PR
def treinar(seed):
    rng=random.Random(seed+1000); s2=T2.novo_s2(rng)
    T2.treinar(s2,T2.dados(12,range(1,5),20000,rng),iters=600,rng=rng); return s2
def valores(s2):
    V=PR.tabela(s2)
    return dict(suc=V((1.,0,0,0,0,1.)), pre=V((0,1.,0,0,0,1.)), eu=V((0,0,1.,0,0,1.)), g=V((0,0,0,0,0,1.)))
def grafo(N,F,k,rng):
    nos=list(range(N)); rng.shuffle(nos); s=nos[0]; it=1
    succ=[None]*N; cadeias=[]
    for f in range(F):
        c=nos[it:it+k]; it+=k; cadeias.append(c)
        for a,b in zip(c,c[1:]): succ[a]=[b]
    succ[s]=[c[0] for c in cadeias]
    resto=nos[it:]+[c[-1] for c in cadeias]
    alvo=resto[:]; rng.shuffle(alvo)
    for a,b in zip(resto,alvo): succ[a]=[b]
    return succ,s,set(c[-1] for c in cadeias)
def passo(z,succ,pred,W,beta,crist):
    N=len(z); d1,d2,d3,g=W['suc']-W['g'],W['pre']-W['g'],W['eu']-W['g'],W['g']
    lg=[g]*N  # base: sum z_j g = g
    for j in range(N):
        if z[j]:
            for i in succ[j]: lg[i]+=z[j]*d1
            for i in pred[j]: lg[i]+=z[j]*d2
            lg[j]+=z[j]*d3
    lg=[beta*x for x in lg]
    if crist:
        k=max(range(N),key=lambda i:lg[i]); o=[0.]*N; o[k]=1.; return o
    m=max(lg); e=[math.exp(x-m) for x in lg]; t=sum(e); return [x/t for x in e]
def rodar(W,N,F,k,beta,crist,rng):
    succ,s,alvo=grafo(N,F,k,rng); pred=[[] for _ in range(N)]
    for j in range(N):
        for i in succ[j]: pred[i].append(j)
    z=[0.]*N; z[s]=1.
    for _ in range(k): z=passo(z,succ,pred,W,beta,crist)
    top=set(sorted(range(N),key=lambda i:-z[i])[:F])
    return top==alvo, sum(z[i] for i in alvo)
if __name__=="__main__":
    for seed in (1590,1591):
        t=time.time(); s2=treinar(seed); W=valores(s2)
        print(seed, {a:round(b,2) for a,b in W.items()}, "m_raw", round(W['suc']-W['g'],2), f"{time.time()-t:.0f}s")
        rng=random.Random(5)
        for N in (64,256,1024):
            for F in (1,2,4,8):
                row=[]
                for beta in (1,2,4,8,16):
                    ok=0;mass=0
                    for _ in range(5):
                        a,b=rodar(W,N,F,8,beta,False,rng); ok+=a; mass+=b
                    row.append(f"b{beta}:{ok}/5 {mass/5:.2f}")
                c=sum(rodar(W,N,F,8,1,True,rng)[0] for _ in range(5))
                print(N,F," ".join(row),"CRIST",c)
