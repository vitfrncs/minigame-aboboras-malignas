import numpy as np
import math

class Transformacoes:
    """função de retorna a matriz de translação"""
    @staticmethod
    def translacao(dx, dy):
        return np.array([
            [1, 0, 0],
            [0, 1, 0],
            [dx, dy, 1]
        ])

    """função de retorna a matriz de rotacao"""
    @staticmethod
    def escala(sx, sy):
        return np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])

    """função de retorna a matriz de escala"""
    @staticmethod
    def rotacao(cos, sen):
        return np.array([
            [cos, -sen, 0],
            [sen, cos, 0],
            [0, 0, 1]
        ])

    @staticmethod
    def composicao(*matrizes):
        """matriz de resultado começa como identidade para não afetar o resultado"""
        resultado = np.eye(3)

        for matriz in matrizes:
            resultado = resultado @ matriz

        return resultado

    @staticmethod
    def aplicar_transformacoes(vertices, matriz):
        """faz as transformacoes nos vertices"""
        transformados = []

        for x, y in vertices:
            """define a coordenada"""
            coordenada = np.array([x, y, 1])

            """aplica no ponto"""
            resultado = coordenada @ matriz

            transformados.append(
                (resultado[0], resultado[1])
            )

        return transformados

    @staticmethod
    def centro_geometrico(vertices):
        soma_x = 0
        soma_y = 0

        for x, y in vertices:
            soma_x = soma_x + x
            soma_y = soma_y + y

        quantidade = len(vertices)

        return (
            soma_x / quantidade,
            soma_y / quantidade
        )

    @staticmethod
    def rotaciona_proprio_centro(vertices, angulo):
        """para rotacionar o objeto no proprio centro"""

        dx, dy = Transformacoes.centro_geometrico(vertices)

        rad = math.radians(angulo)

        cos = math.cos(rad)
        sen = math.sin(rad)

        """Gera as matrizes"""

        T1 = Transformacoes.translacao(-dx, -dy)
        R = Transformacoes.rotacao(cos, sen)
        T2 = Transformacoes.translacao(dx, dy)

        """Faz a composicao"""

        M = Transformacoes.composicao(T1, R, T2)

        return Transformacoes.aplicar_transformacoes(vertices, M)

    @staticmethod
    def matriz_mundo(x, y, angulo=0, sx=1, sy=1):
        """R(θ) @ T(x,y) @ E(sx,sy) — angulo em graus"""
        rad = math.radians(angulo)
        cos = math.cos(rad)
        sen = math.sin(rad)
        return Transformacoes.composicao(
            Transformacoes.escala(sx, sy),
            Transformacoes.rotacao(cos, sen),
            Transformacoes.translacao(x, y)
        )


    @staticmethod
    def colisao(obj1, obj2):
        # pega a escala do objeto 1
        escala1x = getattr(obj1, "escala_x", 1)
        escala1y = getattr(obj1, "escala_y", 1)

        # pega a escala do objeto 2
        escala2x = getattr(obj2, "escala_x", 1)
        escala2y = getattr(obj2, "escala_y", 1)

        #multiplica tamanho oroginal do objeto pelo fator de escala atual
        largura1 = obj1.largura * escala1x
        altura1 = obj1.altura * escala1y

        largura2 = obj2.largura * escala2x
        altura2 = obj2.altura * escala2y

        # desenhamos os objs a partir do centro
        # então temos que achar as bordas, a partir do centro
        esquerda1 = obj1.x - largura1 / 2
        direita1 = obj1.x + largura1 / 2
        topo1 = obj1.y - altura1 / 2
        baixo1 = obj1.y + altura1 / 2

        esquerda2 = obj2.x - largura2 / 2
        direita2 = obj2.x + largura2 / 2
        topo2 = obj2.y - altura2 / 2
        baixo2 = obj2.y + altura2 / 2

        # verifica se há colisão entre bordas
        # há colisao se tudo for verdade
        return (
                esquerda1 < direita2
                and direita1 > esquerda2
                and topo1 < baixo2
                and baixo1 > topo2
        )
