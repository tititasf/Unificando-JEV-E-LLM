import sys, random, torch
sys.argv=['x']
from g1_piloto import Rede, lote
import g1_piloto as G
net=Rede(); net.load_state_dict(torch.load('g1_max.pt')); net.eval()
def khop(W,A,S,T):
    B,n,_=W.shape; INF=1e9
    d=torch.where(S>0,0.0,INF); out=[d]
    Wm=W.masked_fill((A==0)|torch.eye(n,dtype=torch.bool),INF)
    for _ in range(T):
        d=torch.minimum(d,(d.unsqueeze(1)+Wm).min(2).values); out.append(d)
    return out
for n in (16,64):
    W,A,S,D,P=lote(8,n,random.Random(3))
    B=W.shape[0]; h=net.enc(S.unsqueeze(-1)); Wf=W.unsqueeze(-1)
    ks=khop(W,A,S,n)
    with torch.no_grad():
        for t in range(1,n+1):
            hv=h.unsqueeze(2).expand(B,n,n,net.H); hu=h.unsqueeze(1).expand(B,n,n,net.H)
            m=net.msg(torch.cat([hv,hu,Wf],-1)).masked_fill(A.unsqueeze(-1)==0,-1e9).max(2).values
            h=net.upd(torch.cat([h,m],-1))
            dh=net.dist(h).squeeze(-1); k=ks[t]; fin=k<1e8
            if t in (1,2,3,4,6,8,12,16,32,64) and t<=n:
                erk=(dh-k)[fin].abs().mean().item(); erf=(dh-D).abs().mean().item()
                print(f"n={n} t={t:2d} |d_hat - d_khop| {erk:.3f} (alcancaveis {fin.float().mean():.2f}) |d_hat - d_final| {erf:.3f}")
