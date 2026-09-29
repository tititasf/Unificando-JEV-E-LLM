"""
lab/jev.py - o JEV (TypeSafe, "System One") como S1 externo do laboratorio.

Duas partes:
  1. deteccao: ha credencial (TYPESAFE_API_KEY) e rede ate a API?
  2. cliente: wrapper fino sobre o SDK oficial `typesafe-sdk` (TypeSafeClient.system_one),
     usado so quando a deteccao passa.

Regra 12: o JEV e peca SOB TESTE ou ferramenta de TRIAGEM. Nunca avaliador nem metrica.
A credencial nunca entra no repositorio: vem do ambiente (configuracao do ambiente de nuvem)
ou de ~/.config/typesafe/env (fora do git, so na sessao).

Uso: python3 -m lab.jev            (diagnostico; sai 1 se nao acessivel)
     python3 -m lab.jev --teste    (uma pergunta Noul/Choice de fumaca, se acessivel)
"""
import os
import sys
import urllib.error
import urllib.request

CREDENCIAIS = ("TYPESAFE_API_KEY", "OPENROUTER_API_KEY")
ARQ_ENV = os.path.expanduser("~/.config/typesafe/env")


def _base_url():
    try:
        from typesafe_sdk.constants import DEFAULT_BASE_URL
    except ImportError:
        DEFAULT_BASE_URL = "https://api.typesafe.ai"
    return os.environ.get("TYPESAFE_BASE_URL", DEFAULT_BASE_URL)


def _carregar_env_local():
    """Le export NOME='valor' de ~/.config/typesafe/env, sem sobrescrever o ambiente."""
    if not os.path.exists(ARQ_ENV):
        return
    for linha in open(ARQ_ENV):
        linha = linha.strip()
        if linha.startswith("export "):
            linha = linha[7:]
        if "=" in linha and not linha.startswith("#"):
            k, v = linha.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def credencial():
    _carregar_env_local()
    for nome in CREDENCIAIS:
        if os.environ.get(nome):
            return nome
    return None


def sdk():
    try:
        import typesafe_sdk
        return getattr(typesafe_sdk, "__version__", "?")
    except ImportError:
        return None


def rede():
    ok = {}
    for url in (_base_url(), "https://openrouter.ai/api/v1/models"):
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                ok[url] = r.status
        except urllib.error.HTTPError as e:     # respondeu (ex.: 401/404): rede liberada
            ok[url] = e.code
        except Exception:                        # bloqueado ou sem rota
            ok[url] = None
    return ok


def estado():
    c = credencial()
    r = rede()
    s = sdk()
    acessivel = c == "TYPESAFE_API_KEY" and s is not None and r.get(_base_url()) is not None
    return dict(credencial=c, rede=r, sdk=s, acessivel=acessivel)


# ---------------- cliente (so com acesso) ----------------

def cliente():
    credencial()
    from typesafe_sdk import TypeSafeClient
    return TypeSafeClient()


def escolher(estado_txt, instrucoes, opcoes, cli=None):
    """Pergunta Choice. Devolve (rotulo, resposta_bruta_dict)."""
    from typesafe_sdk import Choice
    fechar = cli is None
    cli = cli or cliente()
    try:
        r = cli.system_one(state=estado_txt,
                           questions={"q": Choice(instructions=instrucoes, criteria={o: None for o in opcoes})})
        a = r.choices["q"]
        return a.choice, a.model_dump()
    finally:
        if fechar:
            cli.close()


def sim_nao(estado_txt, instrucoes, cli=None):
    """Pergunta Noul. Devolve a probabilidade de 'sim'."""
    from typesafe_sdk import Noul
    fechar = cli is None
    cli = cli or cliente()
    try:
        r = cli.system_one(state=estado_txt, questions={"q": Noul(instructions=instrucoes)})
        return r.nouls["q"].noul
    finally:
        if fechar:
            cli.close()


def main(argv):
    e = estado()
    print(f"sdk typesafe: {e['sdk'] or 'NAO instalado (pip install typesafe-sdk)'}")
    print(f"credencial: {e['credencial'] or 'nenhuma (' + ' ou '.join(CREDENCIAIS) + ')'}")
    for url, st in e["rede"].items():
        print(f"rede {url}: {'bloqueada' if st is None else f'alcancavel (HTTP {st})'}")
    print("JEV ACESSIVEL" if e["acessivel"] else "JEV NAO ACESSIVEL neste ambiente (ver docs/JEV.md)")
    if e["acessivel"] and "--teste" in argv:
        print("Noul 'o no 3 aponta para si?':",
              sim_nao({"pai": {"1": 3, "2": 3, "3": 3}}, "O no 3 aponta para si mesmo?"))
        print("Choice 'raiz':", escolher({"pai": {"1": 2, "2": 3, "3": 3}},
                                         "Seguindo os ponteiros de pai a partir do no 1, em que no se chega a raiz?",
                                         ["1", "2", "3"])[0])
    sys.exit(0 if e["acessivel"] else 1)


if __name__ == "__main__":
    main(sys.argv)
