import sys, math, random, time
sys.path.insert(0,"/home/user/Unificando-JEV-E-LLM")
from lab import tarefas_clrs as C
def lse_min(vals,beta):
    m=min(vals); return m-math.log(sum(math.exp(-beta*(v-m)) for v in vals))/beta
def rodar(th,adj,s,T=None,beta_mult=1.0,tol=1e-7,Tmax=None):
    beta=math.exp(th[0])*beta_mult; a,b,D0=th[1],th[2],th[3]
    n=len(adj); d=[D0]*n; d[s]=0.0
    Tmax=Tmax or 4*n; t=0
    while True:
        nd=[0.0 if v==s else lse_min([d[u]+a*w+b for u,w in adj[v]],beta) for v in range(n)]
        t+=1; dif=max(abs(x-y) for x,y in zip(nd,d)); d=nd
        if (T is not None and t>=T) or (T is None and (dif<tol or t>=Tmax)): break
    return d,t
def ponteiros(th,adj,s,d,beta_mult=1.0):
    bp=math.exp(th[4])*beta_mult; n=len(adj); pi=list(range(n)); P=[]
    for v in range(n):
        if v==s or not adj[v]: P.append(None); continue
        sc=[(-bp*(d[u]+w),u) for u,w in adj[v]]; m=max(x for x,_ in sc); Z=sum(math.exp(x-m) for x,_ in sc)
        P.append({u:math.exp(x-m)/Z for x,u in sc}); pi[v]=max(sc)[1]
    return pi,P
def perda(th,lote,T=None,rng=None):
    L=0;k=0
    for adj,s,pv in lote:
        TT=T if T is not None else (rng.randint(1,2*len(adj)) if rng else None)
        d,_=rodar(th,adj,s,T=TT if TT else 2*len(adj))
        _,P=ponteiros(th,adj,s,d)
        for v,p in enumerate(P):
            if p is None: continue
            L-=math.log(p.get(pv[v],0)+1e-9); k+=1
    return L/k
def treinar(rng,prog=False,iters=120,lr=0.1):
    th=[math.log(2.0),0.5,0.0,3.0,math.log(2.0)]
    dados=[C.exemplo("bellman_ford",16,rng) for _ in range(200)]
    m=[0]*5;v=[0]*5
    for it in range(1,iters+1):
        lote=[dados[rng.randrange(200)] for _ in range(8)]
        sr=random.Random(it)
        g=[]
        for i in range(5):
            e=[0]*5;e[i]=1e-3
            tp=[x+y for x,y in zip(th,e)]; tm=[x-y for x,y in zip(th,e)]
            if prog:
                g.append((perda(tp,lote,rng=random.Random(it))-perda(tm,lote,rng=random.Random(it)))/2e-3)
            else:
                g.append((perda(tp,lote,T=16)-perda(tm,lote,T=16))/2e-3)
        for i in range(5):
            m[i]=0.9*m[i]+0.1*g[i]; v[i]=0.999*v[i]+0.001*g[i]**2
            th[i]-=lr*(m[i]/(1-0.9**it))/(math.sqrt(v[i]/(1-0.999**it))+1e-8)
    return th
def avaliar(th,n,rng,nex=10,bm=1.0):
    acc=[];ts=[]
    for _ in range(nex):
        adj,s,pv=C.exemplo("bellman_ford",n,rng)
        d,t=rodar(th,adj,s,beta_mult=bm); pi,_=ponteiros(th,adj,s,d,beta_mult=bm)
        acc.append(C.acuracia_ponteiros(pi,pv)); ts.append(t)
    return sum(acc)/nex, sum(ts)/nex
if __name__=="__main__":
    for prog in (False,True):
        t=time.time(); th=treinar(random.Random(1690),prog=prog)
        print("prog",prog,[round(x,2) for x in th],f"{time.time()-t:.0f}s",flush=True)
        for n in (16,32,64):
            print("  n",n,avaliar(th,n,random.Random(7)),flush=True)
