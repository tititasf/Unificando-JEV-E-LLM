import sys, os, math, random, contextlib, io, time
R=os.getcwd(); sys.argv=['x']
sys.path[:0]=[R, R+'/experimentos/E001_mlu', R+'/experimentos/E006_lei_margem', R+'/experimentos/E007_lei_eps']
import mlu, passo_rapido as PR, importlib.util
_sp=importlib.util.spec_from_file_location('dg7',R+'/experimentos/E007_lei_eps/diagnostico.py'); DG=importlib.util.module_from_spec(_sp); _sp.loader.exec_module(DG)
def passo_beta(z,P,beta,crist=False):
    # copia de PR.passo com temperatura
    N,parent,raiz,G=P["N"],P["parent"],P["raiz"],P["G"]
    Z=[0.0,0.0]
    for j in range(N): Z[raiz[j]]+=z[j]
    lg=[0.0]*N
    for i in range(N):
        ri=raiz[i]; v=Z[0]*G[0][ri]+Z[1]*G[1][ri]; corr=P["Vpai"][ri]-G[0][ri]
        for j in P["filhos"][i]: v+=z[j]*corr
        if not ri:
            p=parent[i]; v+=z[p]*(P["Vfilho"][raiz[p]]-G[raiz[p]][0])
        v+=z[i]*(P["Vself"][ri]-G[ri][ri]); lg[i]=beta*v
    if crist:
        j=max(range(N),key=lambda i:lg[i]); o=[0.0]*N; o[j]=1.0; return o
    m=max(lg); e=[math.exp(x-m) for x in lg]; t=sum(e); return [x/t for x in e]
def avaliar(s2,N,d,beta,crist,rng,n=10,T=None):
    ok=0; ms=0
    for _ in range(n):
        p,s,r=mlu.make_example(N,d,rng); P=PR.preparar(s2,p); z=[0.0]*N; z[s]=1.0
        for _ in range(T or d+8): z=passo_beta(z,P,beta,crist)
        ok+= max(range(N),key=lambda i:z[i])==r; ms+=max(z)
    return ok/n, ms/n
for seed in (1390,1391):
    rng=random.Random(seed); s2=mlu.S2Step(4,rng); t=time.time()
    with contextlib.redirect_stdout(io.StringIO()):
        s2.train(mlu.dataset(mlu.N_TRAIN,mlu.TRAIN_DEPTHS,20000,rng),iters=600,rng=rng)
    m=DG.margem_efetiva(s2); print(f"seed {seed} treino {time.time()-t:.0f}s margem m={m:.2f} eps_c={DG.eps_c_teoria(m)}")
    for N in (12,256,4096):
        linha=[]
        for nome,beta,cr in (("b1",1,False),("teoria",1+math.log((N-1)/11)/m,False),("ssmax",math.log(N-1)/math.log(11),False),("b3",3,False),("crist",1,True)):
            a,ms=avaliar(s2,N,10 if N>12 else 6,beta,cr,random.Random(5))
            linha.append(f"{nome}(β={beta:.2f}) acc {a:.1f} massa {ms:.2f}")
        print(" N",N," | ".join(linha),flush=True)
