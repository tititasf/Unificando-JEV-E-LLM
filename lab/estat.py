"""
lab/estat.py - regua estatistica do laboratorio (Python puro, sem dependencias).

Toda afirmacao do tipo "A e melhor que B" neste repositorio precisa passar por
aqui. Referencias:
  - Agarwal et al. 2021, "Deep RL at the Edge of the Statistical Precipice"
    (IQM, bootstrap estratificado, probabilidade de melhoria)
  - Geifman & El-Yaniv 2017 / literatura de predicao seletiva (risk-coverage, AURC)
  - Guo et al. 2017 (ECE)
"""
import math
import random


# ------------------------------------------------------------ agregados
def media(xs):
    return sum(xs) / len(xs)


def iqm(xs):
    """Media interquartil: descarta 25% de cada ponta. Robusta a sementes atipicas."""
    s = sorted(xs)
    n = len(s)
    lo, hi = int(math.floor(0.25 * n)), int(math.ceil(0.75 * n))
    meio = s[lo:hi] or s
    return media(meio)


def bootstrap_ic(xs, estat=media, n_boot=2000, alfa=0.05, seed=0):
    """Intervalo de confianca percentil por bootstrap."""
    rng = random.Random(seed)
    n = len(xs)
    vals = sorted(estat([xs[rng.randrange(n)] for _ in range(n)]) for _ in range(n_boot))
    return vals[int(alfa / 2 * n_boot)], vals[int((1 - alfa / 2) * n_boot) - 1]


def ic_proporcao(acertos, n, z=1.96):
    """Intervalo de Wilson para uma taxa de acerto (bom para n pequeno e p perto de 0/1)."""
    if n == 0:
        return (0.0, 1.0)
    p = acertos / n
    den = 1 + z * z / n
    centro = (p + z * z / (2 * n)) / den
    meia = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, centro - meia), min(1.0, centro + meia)


def prob_melhoria(a, b):
    """P(X_a > X_b) + 0.5 P(empate), estimada sobre todos os pares de sementes.
    0.5 = indistinguivel. Rliable considera relevante quando o IC exclui 0.5."""
    tot = 0.0
    for x in a:
        for y in b:
            tot += 1.0 if x > y else (0.5 if x == y else 0.0)
    return tot / (len(a) * len(b))


def teste_permutacao(a, b, n_perm=5000, seed=0):
    """p-valor bilateral para diferenca de medias (sem suposicao de normalidade)."""
    rng = random.Random(seed)
    obs = abs(media(a) - media(b))
    todos = list(a) + list(b)
    na = len(a)
    extremos = 0
    for _ in range(n_perm):
        rng.shuffle(todos)
        if abs(media(todos[:na]) - media(todos[na:])) >= obs - 1e-12:
            extremos += 1
    return (extremos + 1) / (n_perm + 1)


def cohen_d(a, b):
    ma, mb = media(a), media(b)
    va = sum((x - ma) ** 2 for x in a) / max(1, len(a) - 1)
    vb = sum((x - mb) ** 2 for x in b) / max(1, len(b) - 1)
    sp = math.sqrt(((len(a) - 1) * va + (len(b) - 1) * vb) / max(1, len(a) + len(b) - 2))
    if sp < 1e-9:   # variancia nula: d nao e informativo
        return float("inf") if abs(ma - mb) > 1e-12 else 0.0
    return (ma - mb) / sp


def taxa_colapso(por_semente, limiar=0.5):
    """Fracao de sementes em que o metodo desaba (< limiar). O IQM esconde isso,
    entao todo relatorio deve mostrar os dois."""
    return sum(1 for x in por_semente if x < limiar) / len(por_semente)


# ------------------------------------------- predicao seletiva / S3
def risco_cobertura(confiancas, corretos):
    """Ordena por confianca decrescente e devolve [(cobertura, risco)]."""
    pares = sorted(zip(confiancas, corretos), key=lambda t: -t[0])
    n = len(pares)
    erros = 0
    curva = []
    for k, (_, ok) in enumerate(pares, 1):
        erros += 0 if ok else 1
        curva.append((k / n, erros / k))
    return curva


def aurc(confiancas, corretos):
    """Area sob a curva risco-cobertura. Menor = melhor."""
    curva = risco_cobertura(confiancas, corretos)
    return media([r for _, r in curva])


def e_aurc(confiancas, corretos):
    """AURC excedente sobre o oraculo (que rejeita todos os erros primeiro). 0 = perfeito."""
    n = len(corretos)
    ordem_oraculo = [1.0 if ok else 0.0 for ok in corretos]
    return aurc(confiancas, corretos) - aurc(ordem_oraculo, corretos) if n else 0.0


def ece(confiancas, corretos, bins=10):
    """Erro de calibracao esperado."""
    n = len(confiancas)
    tot = 0.0
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        idx = [i for i, c in enumerate(confiancas) if (lo < c <= hi) or (b == 0 and c == 0)]
        if not idx:
            continue
        acc = media([1.0 if corretos[i] else 0.0 for i in idx])
        conf = media([confiancas[i] for i in idx])
        tot += len(idx) / n * abs(acc - conf)
    return tot


# ------------------------------------------------ custo x desempenho
def fronteira_pareto(pontos):
    """pontos: [(nome, custo, desempenho)]. Devolve os nao-dominados
    (ninguem mais barato E melhor)."""
    nd = []
    for n1, c1, d1 in pontos:
        dominado = any((c2 <= c1 and d2 >= d1) and (c2 < c1 or d2 > d1)
                       for n2, c2, d2 in pontos if n2 != n1)
        if not dominado:
            nd.append((n1, c1, d1))
    return sorted(nd, key=lambda t: t[1])


def razao_extrapolacao(acc_por_tamanho, tamanho_treino, limiar=0.95):
    """Maior tamanho resolvido com acuracia >= limiar, dividido pelo maior do treino."""
    ok = [t for t, a in acc_por_tamanho.items() if a >= limiar]
    return (max(ok) / tamanho_treino) if ok else 0.0


def resumo(nome, por_semente):
    """Linha padrao de relatorio: IQM [IC95%] (n sementes)."""
    lo, hi = bootstrap_ic(por_semente, iqm)
    return f"{nome}: IQM {iqm(por_semente):.3f} [IC95% {lo:.3f}, {hi:.3f}] (n={len(por_semente)})"


def fisher_exato(a_sim, a_n, b_sim, b_n):
    """p-valor bilateral do teste exato de Fisher para duas proporcoes
    (ex.: taxa de colapso 5/30 vs 0/30)."""
    def comb(n, k):
        return math.comb(n, k)
    tot_sim = a_sim + b_sim
    N = a_n + b_n
    den = comb(N, tot_sim)
    p_obs = comb(a_n, a_sim) * comb(b_n, b_sim) / den
    p = 0.0
    for k in range(max(0, tot_sim - b_n), min(a_n, tot_sim) + 1):
        pk = comb(a_n, k) * comb(b_n, tot_sim - k) / den
        if pk <= p_obs * (1 + 1e-9):
            p += pk
    return min(1.0, p)


# ------------------------------------------------ tamanho de amostra
def _z(p):
    """Quantil da normal padrao (aproximacao de Acklam simplificada via bissecao)."""
    lo, hi = -10.0, 10.0
    for _ in range(100):
        m = (lo + hi) / 2
        if 0.5 * (1 + math.erf(m / math.sqrt(2))) < p:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def n_para_diferenca(p0, p1, alfa=0.01, poder=0.8):
    """Exemplos POR BRACO para distinguir duas taxas p0 e p1 (teste bilateral
    de duas proporcoes). Use no PREREG para justificar o tamanho das celulas."""
    za, zb = _z(1 - alfa / 2), _z(poder)
    pm = (p0 + p1) / 2
    num = (za * math.sqrt(2 * pm * (1 - pm)) + zb * math.sqrt(p0 * (1 - p0) + p1 * (1 - p1))) ** 2
    return math.ceil(num / (p0 - p1) ** 2) if p0 != p1 else float("inf")


def n_para_largura(p, meia_largura, z=1.96):
    """Exemplos para o IC de Wilson de uma taxa ~p ter meia-largura <= meia_largura."""
    n = 1
    while n < 10 ** 7:
        lo, hi = ic_proporcao(round(p * n), n, z)
        if (hi - lo) / 2 <= meia_largura:
            return n
        n = max(n + 1, int(n * 1.1))
    return n
