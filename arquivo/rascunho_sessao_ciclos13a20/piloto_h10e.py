from piloto_h10 import *
def passo_mist(z,succ,pred,W,beta):
    # cada no j distribui sua massa por softmax_i(beta*S_ji): mistura de softmaxes
    N=len(z); g=W['g']; out=[0.]*N; generico=0.
    for j in range(N):
        if not z[j]: continue
        esp={}
        for i in succ[j]: esp[i]=esp.get(i,0)+W['suc']-g
        for i in pred[j]: esp[i]=esp.get(i,0)+W['pre']-g
        esp[j]=esp.get(j,0)+W['eu']-g
        e={i:math.exp(beta*d) for i,d in esp.items()}
        Z=sum(e.values())+(N-len(e))
        generico+=z[j]/Z
        for i,v in e.items(): out[i]+=z[j]*(v-1)/Z
    return [x+generico for x in out]
def tarefa(N,F,k,modo,rng):
    if modo=="SUP":
        pi=list(range(N)); rng.shuffle(pi); succ=[[pi[i]] for i in range(N)]
        ini=rng.sample(range(N),F); pes=[i+1 for i in range(F)]; t=sum(pes); z0={s:w/t for s,w in zip(ini,pes)}
        alvo=set()
        for s in ini:
            for _ in range(k): s=pi[s]
            alvo.add(s)
    else:
        p1=list(range(N)); p2=list(range(N)); rng.shuffle(p1); rng.shuffle(p2)
        succ=[[p1[i],p2[i]] if p1[i]!=p2[i] else [p1[i]] for i in range(N)]
        s=rng.randrange(N); z0={s:1.}; fr={s}
        for _ in range(k): fr={i for j in fr for i in succ[j]}
        alvo=fr
    pred=[[] for _ in range(N)]
    for j in range(N):
        for i in succ[j]: pred[i].append(j)
    return succ,pred,z0,alvo
def rodar(W,N,F,k,modo,braco,beta,rng):
    succ,pred,z0,alvo=tarefa(N,F,k,modo,rng)
    z=[0.]*N
    for s,w in z0.items(): z[s]=w
    for _ in range(k):
        z=passo_mist(z,succ,pred,W,beta) if braco=="MIST" else passo(z,succ,pred,W,beta,braco=="CRIST")
    top=set(sorted(range(N),key=lambda i:-z[i])[:len(alvo)])
    return top==alvo, sum(z[i] for i in alvo)
if __name__=="__main__":
  W=valores(treinar(1590)); m=W['suc']-W['g']; rng=random.Random(13)
  for modo,F,ks in (("SUP",4,(16,64)),("SUP",8,(16,)),("BFS",1,(3,5))):
    for N in (256,1024):
      for k in ks:
        row=[]
        for braco,beta in (("GLOB",1),("GLOB",2.5),("CRIST",1),("MIST",1),("MIST",2.5)):
          r=[rodar(W,N,F,k,modo,braco,beta,rng) for _ in range(3)]
          row.append(f"{braco}{beta}:{sum(x[0] for x in r)}/3 M{sum(x[1] for x in r)/3:.2f}")
        print(modo,F,N,k," | ".join(row),flush=True)
