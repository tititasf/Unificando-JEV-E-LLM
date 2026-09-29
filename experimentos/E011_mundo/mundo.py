"""
Modelo de mundo com o mesmo passo (S6.1): particula numa caixa 1D com paredes.

Mundo verdadeiro (desconhecido do modelo): posicao x em 0..L-1, velocidade v em
{-2, -1, +1, +2}. y = x + v; se y passa da parede, reflete (x' = espelho, v' = -v).

Modelo: estado = distribuicao sobre pares (x, v); um unico passo relacional
aprendido, com atributos LOCAIS do par (x, v) -> (x', v'):
  dx = x' - x em {-2..2} ou "longe"        (6, one-hot)
  relacao de velocidade: igual | oposta | outra (3)
  v atual                                    (4, one-hot)
  distancia a parede a frente: 0 | 1 | >= 2  (3, one-hot)   [ablacao SEM_PAREDE: zerada]
  vies                                        (1)
Nada diz "rebata": o passo aprende a fisica a partir de trajetorias.
Treino em L = 8; teste em L = 8, 32, 64 (o passo e local, entao serve em qualquer L).
"""
import os
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "experimentos", "E001_mlu"))
import mlu  # noqa: E402

VELS = (-2, -1, 1, 2)


def fisica(L, x, a):
    v = VELS[a]
    y = x + v
    if y > L - 1:
        return 2 * (L - 1) - y, VELS.index(-v)
    if y < 0:
        return -y, VELS.index(-v)
    return y, a


class Caixa:
    """'Grafo' do espaco de pares (x, v); indice = x * 4 + a."""

    def __init__(self, L):
        self.L = L

    def __len__(self):
        return self.L * 4

    @staticmethod
    def idx(x, a):
        return x * 4 + a


def atributos(L, x, a, x2, b, com_parede=True):
    f = [0.0] * 17
    dx = x2 - x
    f[dx + 2 if -2 <= dx <= 2 else 5] = 1.0
    v, v2 = VELS[a], VELS[b]
    f[6 if v2 == v else (7 if v2 == -v else 8)] = 1.0
    f[9 + a] = 1.0
    if com_parede:
        frente = (L - 1 - x) if v > 0 else x
        f[13 + min(frente, 2)] = 1.0
    f[16] = 1.0
    return tuple(f)


class MotorMundo(mlu.S2Step):
    F = 17
    COM_PAREDE = True

    def feat(self, g, u, w):
        x, a = divmod(u, 4)
        x2, b = divmod(w, 4)
        return atributos(g.L, x, a, x2, b, self.COM_PAREDE)


class MotorSemParede(MotorMundo):
    COM_PAREDE = False


def rollout(motor, L, x0, a0, T):
    g = Caixa(L)
    S = motor.affinity(g)
    z = [0.0] * len(g)
    z[g.idx(x0, a0)] = 1.0
    prev = []
    for _ in range(T):
        z = motor.step(z, S)
        prev.append(max(range(len(z)), key=lambda i: z[i]))
    return prev


def verdade(L, x0, a0, T):
    x, a = x0, a0
    out = []
    for _ in range(T):
        x, a = fisica(L, x, a)
        out.append(Caixa.idx(x, a))
    return out
