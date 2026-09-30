import sys,random,math
sys.path.insert(0,'/home/user/Unificando-JEV-E-LLM/experimentos/E016_clrs'); sys.path.insert(0,'/home/user/Unificando-JEV-E-LLM'); sys.argv=['x']
import e016 as E
from lab import tarefas_clrs as C
th=[3.8765918537724517, 0.8807962493965181, 0.00017512002740048896, 3.853329024832417, 3.0428140053896686]
for b in (0.0002,0.01,0.03,0.06):
  t2=list(th); t2[2]=b
  for n in (16,64):
    rng=random.Random(7)
    accs=[];ts=[];mins=[];sur=[]
    for _ in range(10):
      adj,s,pv=C.exemplo("bellman_ford",n,rng)
      d,t=E.rodar(t2,adj,s)
      accs.append(C.acuracia_ponteiros(E.ponteiros(t2,adj,s,d)[0],pv))
      sur.append(C.acuracia_ponteiros(E.surrogado(t2,adj,s),pv))
      ts.append(t); mins.append(min(x for i,x in enumerate(d) if i!=s))
    print(b,n,'acc %.3f surr %.3f passos %.1f min_d %.3f'%(sum(accs)/10,sum(sur)/10,sum(ts)/10,min(mins)))
