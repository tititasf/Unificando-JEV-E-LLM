import sys,random,math,time
sys.path.insert(0,'/home/user/Unificando-JEV-E-LLM/experimentos/E016_clrs'); sys.path.insert(0,'/home/user/Unificando-JEV-E-LLM'); sys.argv=['x']
import e016 as E
from lab import tarefas_clrs as C
for n in (16,64,160):
  rng=random.Random(12)
  ex=[C.exemplo("bellman_ford",n,rng) for _ in range(6)]
  for k in (0.5,2,8):
    acc=[];ts=[];t0=time.time();bs=[]
    for adj,s,pv in ex:
      wmin=min(w for a in adj for _,w in a); b=k/wmin; bs.append(b)
      th=[math.log(b),1.0,0.0,10.0,math.log(b)]
      d,t=E.rodar(th,adj,s); acc.append(C.acuracia_ponteiros(E.ponteiros(th,adj,s,d)[0],pv)); ts.append(t)
    print(n,k,'beta~%.0f acc %.3f passos %.1f  %.1fs'%(sum(bs)/6,sum(acc)/6,sum(ts)/6,time.time()-t0),flush=True)
