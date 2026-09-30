import sys,random,math
sys.path.insert(0,'/home/user/Unificando-JEV-E-LLM/experimentos/E016_clrs'); sys.path.insert(0,'/home/user/Unificando-JEV-E-LLM'); sys.argv=['x']
import e016 as E
from lab import tarefas_clrs as C
for n in (16,64,160):
  rng=random.Random(11)
  ex=[C.exemplo("bellman_ford",n,rng) for _ in range(6)]
  for lb in (16,64,256,1024):
    th=[math.log(lb),1.0,0.0,10.0,math.log(lb)]
    acc=[];ts=[]
    for adj,s,pv in ex:
      d,t=E.rodar(th,adj,s); acc.append(C.acuracia_ponteiros(E.ponteiros(th,adj,s,d)[0],pv)); ts.append(t)
    print(n,lb,'acc %.3f passos %.1f'%(sum(acc)/6,sum(ts)/6),flush=True)
