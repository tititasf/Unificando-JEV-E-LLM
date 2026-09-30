import json, random, sys, time, os
sys.path.insert(0, "experimentos/E005_t2_salto"); sys.path.insert(0, "experimentos/E001_mlu")
sys.argv = [sys.argv[0]]
import tarefa_t2 as T2, mlu
from lab import jev
jev.credencial()
from typesafe_sdk import TypeSafeClient, Choice
rng = random.Random(1290)
cli = TypeSafeClient()
def pergunta(estado, instr, N):
    t = time.time()
    r = cli.system_one(state=estado, questions={"q": Choice(instructions=instr, criteria={str(i): None for i in range(N)})})
    a = r.choices["q"]
    return a, r.usage, time.time() - t, r.model
a, u, dt, m = pergunta({"ponteiros": {str(i): p for i, p in enumerate([1,2,0])}, "inicio": 0, "k": 2},
                  "Comece no no 'inicio' e siga 'ponteiros' exatamente k vezes. Em que no voce termina?", 3)
print("MODELO", m); print("DUMP", json.dumps(a.model_dump(), default=str)[:600]); print("USAGE", u.model_dump(), "dt", round(dt,2))
for N in (8, 32):
    for k in (1, 2, 4):
        ok = 0
        for _ in range(4):
            pi, s, k_, alvo = T2.exemplo(N, k, rng)
            a, u, dt, _ = pergunta({"ponteiros": {str(i): p for i, p in enumerate(pi)}, "inicio": s, "k": k},
                  "Comece no no 'inicio' e siga 'ponteiros' exatamente k vezes. Em que no voce termina?", N)
            ok += a.choice == str(alvo)
        print(f"T2 N={N} k={k}: {ok}/4  tokens_in={u.input_tokens} dt={dt:.2f}")
for N in (8, 32):
    for d in (1, 3):
        ok = 0
        for _ in range(4):
            par, s, raiz = mlu.make_example(N, d, rng)
            a, u, dt, _ = pergunta({"pai": {str(i): p for i, p in enumerate(par)}, "inicio": s},
                  "Comece no no 'inicio' e siga 'pai' ate chegar a um no que e pai de si mesmo (a raiz). Qual e essa raiz?", N)
            ok += a.choice == str(raiz)
        print(f"T1 N={N} d={d}: {ok}/4  tokens_in={u.input_tokens} dt={dt:.2f}")
