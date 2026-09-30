from piloto_h10b import *
import piloto_h10b as B
W=valores(treinar(1590)); rng=random.Random(9)
for N in (256,1024):
  for k in (4,8,16,32):
    for beta in (0.25,1):
      res=[];cons=[]
      for _ in range(4):
        succ,s,alvo=grafo_desigual(N,5,k,rng); pred=[[] for _ in range(N)]
        for j in range(N):
          for i in succ[j]: pred[i].append(j)
        z=[0.]*N; z[s]=1.
        for _ in range(k): z=passo(z,succ,pred,W,beta,False)
        A=set(alvo); mn=min(z[i] for i in A); mx=max(z[i] for i in range(N) if i not in A)
        res.append(mn>mx); cons.append((mn-mx)/(1/N))
      print(N,k,beta,sum(res),"/4 contraste rel", " ".join(f"{c:.1e}" for c in cons))
