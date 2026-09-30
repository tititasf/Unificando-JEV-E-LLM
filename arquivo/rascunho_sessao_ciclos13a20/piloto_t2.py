import sys, math, random, time
sys.argv=['x']; sys.path.insert(0,'experimentos/E013_temperatura'); sys.path.insert(0,'experimentos/E005_t2_salto')
import passo_geral as PG, mlu, tarefa_t2 as T2
def margem(s2, gerar):
    r=random.Random(1); eps=0; n=0
    for _ in range(5):
        p=gerar(30,r); P=PG.preparar(s2,p)
        for j in r.sample([j for j in range(30) if p[j]!=j],6): eps+=PG.vazamento(P,j); n+=1
    eps/=n; return -math.log(eps/((1-eps)*29)), eps
for seed in (1392,1393):
    rng=random.Random(seed); t=time.time(); s2=T2.novo_s2(rng)
    T2.treinar(s2, T2.dados(12, range(1,5), 20000, rng), iters=600, rng=rng)
    m,e30=margem(s2, lambda N,r: T2.exemplo(N,1,r)[0]); print(f"T2 seed {seed} treino {time.time()-t:.0f}s m={m:.2f} eps30={e30:.4f}")
    for N in (12,256,4096):
        out=[]
        for nome,beta,cr in (("b1",1,False),("teoria",1+math.log((N-1)/11)/m,False),("ssmax",math.log(N-1)/math.log(11),False),("crist",1,True)):
            r=random.Random(9); ok=0; le=0
            for _ in range(6):
                pi,s,k,alvo=T2.exemplo(N,16,r); P=PG.preparar(s2,pi); z=[0.0]*N; z[s]=1.0
                for _ in range(k): z=PG.passo(z,P,beta,cr)
                ok+=max(range(N),key=lambda i:z[i])==alvo; le+=PG.vazamento(P,s,beta)
            out.append(f"{nome}(β={beta:.2f}) acc {ok/6:.2f} eps {le/6:.4f}")
        print("  N",N," | ".join(out),flush=True)
