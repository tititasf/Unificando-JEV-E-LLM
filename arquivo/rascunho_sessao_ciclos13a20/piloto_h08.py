import sys, json, math, importlib.util
R="/home/user/Unificando-JEV-E-LLM"
sys.argv=[sys.argv[0]]
sp=importlib.util.spec_from_file_location("e012",R+"/experimentos/E012_jev/e012.py"); E=importlib.util.module_from_spec(sp); sp.loader.exec_module(E)
inst={i[0]:i for i in E.instancias()}
saltos=[]
for l in open(R+"/experimentos/E012_jev/respostas_jev.jsonl"):
    r=json.loads(l)
    if r["braco"] not in ("ITER","ITER_PF"): continue
    iid,tarefa,N,p,(g,s),_,_=inst[r["id"]]
    for q in r["passos"]:
        if "erro" in q: continue
        pr=sorted(q["probs"].values(),reverse=True); p1=q["probs"].get(q["escolha"],0)
        certo=int(q["escolha"])==g[q["x"]]
        saltos.append(dict(t=tarefa,N=N,certo=certo,p1=p1,conf=q["conf"],pr=pr))
def esc(h,nome):
    N=h["N"]; p1=min(max(h["p1"],1e-4),1-1e-4)
    if nome=="p1": return p1
    if nome=="m": return math.log(p1*(N-1)/(1-p1))
    if nome=="m2": return math.log(p1/max(h["pr"][1],1e-4)) if h["pr"][0]==h["p1"] else -9
    if nome=="logit": return math.log(p1/(1-p1))
from collections import defaultdict
for nome in ("p1","logit","m"):
    cal=[h for h in saltos if h["t"]=="T2" and h["N"]==8]
    # menor limiar com risco empirico <= 2%
    vals=sorted(set(esc(h,nome) for h in cal))
    lam=None
    for v in vals:
        ac=[h for h in cal if esc(h,nome)>=v]
        if ac and sum(not h["certo"] for h in ac)/len(ac)<=0.02: lam=v;break
    row=[]
    for t in ("T2","T1"):
        for N in (8,32,64):
            S=[h for h in saltos if h["t"]==t and h["N"]==N]; ac=[h for h in S if esc(h,nome)>=lam]
            row.append(f"{t}{N}: risco {sum(not h['certo'] for h in ac)/max(1,len(ac)):.3f} cob {len(ac)/len(S):.2f}")
    print(nome,f"lam {lam:.2f}"," | ".join(row))
print(len(saltos))
