from piloto_h23 import *
th=treinar(random.Random(1690),iters=300)
print([round(x,2) for x in th])
for n in (16,32,64):
    print(n," ".join(f"x{bm}:{avaliar(th,n,random.Random(7),nex=6,bm=bm)}" for bm in (1,2,4,8,16,32)),flush=True)
