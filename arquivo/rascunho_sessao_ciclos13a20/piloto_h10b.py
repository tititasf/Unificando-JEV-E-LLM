from piloto_h10 import *
def grafo_desigual(N,F,k,rng):
    # s -> F filhos; cadeias; os 2 primeiros filhos se fundem no 2o no (ramo pesado 2/F); os outros F-2 ramos leves 1/F
    nos=list(range(N)); rng.shuffle(nos); s=nos[0]; it=1
    succ=[None]*N; filhos=nos[it:it+F]; it+=F
    succ[s]=filhos
    cad=[]
    # ramo pesado: filhos 0 e 1 -> cadeia H de comprimento k-1
    H=nos[it:it+k-1]; it+=k-1
    succ[filhos[0]]=[H[0]]; succ[filhos[1]]=[H[0]]
    for a,b in zip(H,H[1:]): succ[a]=[b]
    alvo=[H[-1]]
    for f in filhos[2:]:
        c=[f]+nos[it:it+k-1]; it+=k-1
        for a,b in zip(c,c[1:]): succ[a]=[b]
        alvo.append(c[-1])
    resto=nos[it:]+alvo
    dest=resto[:]; rng.shuffle(dest)
    for a,b in zip(resto,dest): succ[a]=[b]
    return succ,s,alvo
def rodar2(W,N,F,k,beta,rng):
    succ,s,alvo=grafo_desigual(N,F,k,rng); pred=[[] for _ in range(N)]
    for j in range(N):
        for i in succ[j]: pred[i].append(j)
    z=[0.]*N; z[s]=1.
    for _ in range(k): z=passo(z,succ,pred,W,beta,False)
    top=set(sorted(range(N),key=lambda i:-z[i])[:len(alvo)])
    leves=alvo[1:]
    return top==set(alvo), z[alvo[0]], sum(z[i] for i in leves)
for seed in (1590,):
    W=valores(treinar(seed)); rng=random.Random(7)
    for N in (256,1024):
        for F in (3,5,9):
            row=[]
            for beta in (0.25,0.5,1,2,4,8,16):
                r=[rodar2(W,N,F,8,beta,rng) for _ in range(4)]
                row.append(f"b{beta}:{sum(x[0] for x in r)}/4 H{sum(x[1] for x in r)/4:.2f} L{sum(x[2] for x in r)/4:.3f}")
            print(N,F," | ".join(row))
