import json, sys, random
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'.'); sys.argv=['x']; sys.path.insert(0,'experimentos/E012_jev')
import e012
from lab import jev
jev.credencial()
from typesafe_sdk import TypeSafeClient, Noul
insts={i[0]:i for i in e012.instancias()}
amostra={}
for r in map(json.loads,open('experimentos/E012_jev/respostas_jev.jsonl')):
    if r['braco']!='ITER': continue
    _,t,N,p,(g,s),v,um=insts[r['id']]
    for q in r['passos']:
        ok=int(q['escolha'])==g[q['x']]
        amostra.setdefault((N,ok),[]).append((g,q['x'],int(q['escolha'])))
rng=random.Random(7)
tarefas=[]
for (N,ok),L in amostra.items():
    for item in rng.sample(L,min(25,len(L))): tarefas.append((N,ok)+item)
cli=TypeSafeClient()
def f(t):
    N,ok,g,x,y=t
    r=cli.system_one(state={"ponteiros":{str(i):v for i,v in enumerate(g)},"no":x,"candidato":y},
        questions={"q":Noul(instructions="O valor de ponteiros[no] e igual a candidato?")})
    return N,ok,r.nouls["q"].noul
res=list(ThreadPoolExecutor(8).map(f,tarefas))
for N in (8,32,64):
    c=[p for n,o,p in res if n==N and o]; w=[p for n,o,p in res if n==N and not o]
    print(N,"certos: media %.2f min %.2f (n=%d) | errados: media %.2f max %.2f (n=%d)"%(sum(c)/len(c),min(c),len(c),sum(w)/len(w),max(w),len(w)))
    for lam in (0.5,0.7,0.9):
        print("   lam",lam,"aceita certos %d/%d errados %d/%d"%(sum(p>=lam for p in c),len(c),sum(p>=lam for p in w),len(w)))
