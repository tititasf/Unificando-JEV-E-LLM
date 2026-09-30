from piloto_h10 import *
def rodar_sup(W,N,pesos,k,beta,rng):
    pi=list(range(N)); rng.shuffle(pi); succ=[[pi[i]] for i in range(N)]; pred=[[] for _ in range(N)]
    for j in range(N): pred[pi[j]].append(j)
    ini=rng.sample(range(N),len(pesos)); z=[0.]*N
    for s,w in zip(ini,pesos): z[s]=w
    for _ in range(k): z=passo(z,succ,pred,W,beta,False)
    alvo=[]
    for s in ini:
        for _ in range(k): s=pi[s]
        alvo.append(s)
    top=set(sorted(range(N),key=lambda i:-z[i])[:len(alvo)])
    za=[z[i] for i in alvo]
    return top==set(alvo), sum(za), min(za)/max(za)
if __name__=="__main__":
  W=valores(treinar(1590)); m=W['suc']-W['g']; rng=random.Random(11)
  pesos=(0.4,0.3,0.2,0.1)
  for N in (256,1024):
    for k in (4,16,64):
      row=[]
      for beta in (0.1,0.25,0.5,0.75,1,1.5,2,4):
        r=[rodar_sup(W,N,pesos,k,beta,rng) for _ in range(3)]
        row.append(f"b{beta}:{sum(x[0] for x in r)}/3 M{sum(x[1] for x in r)/3:.2f} r{sum(x[2] for x in r)/3:.2f}")
      print(N,k," | ".join(row))
