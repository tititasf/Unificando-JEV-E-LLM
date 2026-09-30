import sys,random,math
sys.path.insert(0,'/home/user/Unificando-JEV-E-LLM')
from lab import tarefas_clrs as C
INF=float('inf')
def E(adj): return sum(len(a) for a in adj)
def jacobi(adj,s,d0=None):
    n=len(adj); d=list(d0) if d0 else [INF]*n; d[s]=0.0; r=0
    while True:
        nd=list(d)
        for v in range(n):
            for u,w in adj[v]:
                if d[u]+w<nd[v]-1e-12: nd[v]=d[u]+w
        r+=1
        if nd==d: return d,r
        d=nd
def ptr(adj,s,d):
    n=len(adj);pi=list(range(n))
    for v in range(n):
        if v==s or d[v]==INF: continue
        pi[v]=min((d[u]+w,u) for u,w in adj[v])[1]
    return pi
def dist_arvore(adj,s,pi):
    n=len(adj); W={}
    for v in range(n):
        for u,w in adj[v]: W[(u,v)]=w
    d=[None]*n; d[s]=0.0
    def go(v,vis):
        if d[v] is not None: return d[v]
        if v in vis or pi[v]==v: return INF
        vis.add(v); x=go(pi[v],vis)+W.get((pi[v],v),INF); d[v]=x; return x
    for v in range(n): go(v,set())
    return d
def cert(adj,s,d):
    if d[s]!=0: return False
    for v in range(len(adj)):
        for u,w in adj[v]:
            if d[v]>d[u]+w+1e-12: return False
    return True
def s1_2salto(adj,s):
    n=len(adj); ws={u:w for u,w in adj[s]}
    pi=list(range(n))
    for v in range(n):
        if v==s: continue
        best=(ws.get(v,INF),s)
        for u,w in adj[v]:
            if u in ws and ws[u]+w<best[0]: best=(ws[u]+w,u)
        pi[v]=best[1]
    return pi
def grade(L,rng):
    n=L*L; adj=[[] for _ in range(n)]
    for i in range(L):
        for j in range(L):
            v=i*L+j
            for di,dj in((0,1),(1,0)):
                a,b=i+di,j+dj
                if a<L and b<L:
                    u=a*L+b; w=rng.random(); adj[v].append((u,w)); adj[u].append((v,w))
    return adj
rng=random.Random(5)
for fam in ('er','grade'):
  for n in ((16,64,256) if fam=='er' else (4,8,16)):
    R=[];acc=[];rat=[];ratw=[]
    for _ in range(10):
        adj=C.grafo_er(n,0.5,rng,pesos=True) if fam=='er' else grade(n,rng)
        s=rng.randrange(len(adj)); e=E(adj)
        d,r=jacobi(adj,s); R.append(r)
        pi=s1_2salto(adj,s); dh=dist_arvore(adj,s,pi); ok=cert(adj,s,dh); acc.append(ok)
        c_s2=r*e; c_comp=e+len(adj)+e+(0 if ok else r*e)
        _,r2=jacobi(adj,s,dh); c_w=e+len(adj)+e+(0 if ok else r2*e)
        rat.append(c_s2/c_comp); ratw.append(c_s2/c_w)
    print(fam,n,'rounds',sum(R)/10,'cert_ok',sum(acc)/10,'ratio cold %.2f warm %.2f'%(sum(rat)/10,sum(ratw)/10))
print('--- reparo localizado')
from collections import deque
def reparo(adj,s,d):
    # worklist a partir dos nos que violam o certificado (S3 localiza)
    n=len(adj); d=list(d); c=0
    q=deque(); inq=[False]*n
    for v in range(n):
        for u,w in adj[v]:
            c+=1
            if d[u]+w<d[v]-1e-12 and not inq[u]: q.append(u); inq[u]=True
    while q:
        u=q.popleft(); inq[u]=False
        for v,w in adj[u]:
            c+=1
            if d[u]+w<d[v]-1e-12:
                d[v]=d[u]+w
                if not inq[v]: q.append(v); inq[v]=True
    return d,c
def spfa(adj,s):
    return reparo(adj,s,[0.0 if v==s else INF for v in range(len(adj))])
def s1_manh(adj,s,L,c=0.3):
    n=len(adj); si,sj=divmod(s,L); pi=list(range(n))
    for v in range(n):
        if v==s: continue
        pi[v]=min((w+c*(abs(u//L-si)+abs(u%L-sj)),u) for u,w in adj[v] if abs(u//L-si)+abs(u%L-sj)<abs(v//L-si)+abs(v%L-sj))[1]
    return pi
rng=random.Random(6)
for fam in ('er','grade'):
  for n in ((16,64,256) if fam=='er' else (4,8,16)):
    tab=[]
    for _ in range(10):
        adj=C.grafo_er(n,0.5,rng,pesos=True) if fam=='er' else grade(n,rng)
        N=len(adj); s=rng.randrange(N); e=E(adj)
        d,r=jacobi(adj,s); pv=ptr(adj,s,d)
        pi=s1_2salto(adj,s) if fam=='er' else s1_manh(adj,s,n)
        nodeacc=sum(a==b for a,b in zip(pi,pv))/N
        dh=dist_arvore(adj,s,pi); d2,crep=reparo(adj,s,dh)
        assert all(abs(a-b)<1e-9 for a,b in zip(d2,d))
        _,csp=spfa(adj,s)
        tab.append((r*e/(e+N+crep), csp/(e+N+crep), nodeacc, r))
    m=lambda i: sum(t[i] for t in tab)/len(tab)
    print(fam,n,'S1 acc no %.2f  jacobi/comp %.2f  spfa/comp %.2f rounds %.1f'%(m(2),m(0),m(1),m(3)))
