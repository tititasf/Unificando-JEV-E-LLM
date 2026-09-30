import sys, random, torch, itertools
sys.argv=['x']
from g1_piloto import Rede, lote
torch.manual_seed(0)
net=Rede(); net.load_state_dict(torch.load('g1_max.pt')); net.eval()
# 1. transicoes observadas: estado decodificado d^t -> d^{t+1}
Xs=[]
with torch.no_grad():
    for n in (16,32):
        W,A,S,D,P=lote(16,n,random.Random(11+n)); B=W.shape[0]
        h=net.enc(S.unsqueeze(-1)); Wf=W.unsqueeze(-1); dprev=net.dist(h).squeeze(-1)
        for t in range(n):
            hv=h.unsqueeze(2).expand(B,n,n,net.H); hu=h.unsqueeze(1).expand(B,n,n,net.H)
            m=net.msg(torch.cat([hv,hu,Wf],-1)).masked_fill(A.unsqueeze(-1)==0,-1e9).max(2).values
            h=net.upd(torch.cat([h,m],-1)); dnew=net.dist(h).squeeze(-1)
            if t>=1: Xs.append((dprev,dnew,W,A-torch.eye(n),S))
            dprev=dnew
print("transicoes:",len(Xs))
# 2. linguagem de regras: d_v' = AGG_OUT( [d_v se keep], AGG_u f(d_u,w) ), f linear alpha*d_u+beta*w+gamma, ou min/max(d_u,w)
def aplica(regra, th, dprev, W, A):
    agg, termo, keep = regra
    a,b,c = th
    du=dprev.unsqueeze(1).expand_as(W)
    f = a*du+b*W+c if termo=="lin" else (torch.minimum(a*du,b*W)+c if termo=="minf" else torch.maximum(a*du,b*W)+c)
    if agg=="min": r=f.masked_fill(A==0,1e9).min(2).values; r=torch.minimum(r,dprev) if keep else r
    elif agg=="max": r=f.masked_fill(A==0,-1e9).max(2).values; r=torch.maximum(r,dprev) if keep else r
    else: r=(f*A).sum(2)/A.sum(2).clamp(min=1); r=(r+dprev)/2 if keep else r
    return r
def erro(regra, th):
    e=0;k=0
    for dprev,dnew,W,A,S in Xs:
        r=aplica(regra,th,dprev,W,A); msk=S==0
        e+=((r-dnew)[msk]**2).sum(); k+=msk.sum()
    return e/k
res=[]
for regra in itertools.product(("min","max","mean"),("lin","minf","maxf"),(True,False)):
    th=torch.tensor([1.0,1.0,0.0],requires_grad=True); opt=torch.optim.Adam([th],0.02)
    for _ in range(150):
        l=erro(regra,th); opt.zero_grad(); l.backward(); opt.step()
    th=th.detach(); e=erro(regra,th).item()
    # arredondamento de Occam
    cand=[round(float(x)*2)/2 for x in th]; es=erro(regra,torch.tensor(cand)).item()
    res.append((e,regra,[round(float(x),3) for x in th],cand,es))
for r in sorted(res)[:6]: print(f"mse {r[0]:.5f}  {r[1]}  th={r[2]}  arred={r[3]} mse_arred {r[4]:.5f}")
