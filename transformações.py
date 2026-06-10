import numpy as np
import math


class Transformacoes:

    @staticmethod
    def translacao(dx, dy):
        """retorna a matriz de translação"""
        return np.array([
            [1, 0, 0],
            [0, 1, 0],
            [dx, dy, 1]
        ])

    @staticmethod
    def escala(sx, sy):
        """retorna a matriz de escala"""
        return np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ])

    @staticmethod
    def rotacao(cos, sen):
        """retorna a matriz de rotação"""
        return np.array([
            [cos, -sen, 0],
            [sen, cos, 0],
            [0, 0, 1]
        ])

    @staticmethod
    def composicao(*matrizes):
        """multiplica todas as matrizes em sequência"""
        # começa como identidade para não afetar o resultado
        resultado = np.eye(3)
        for matriz in matrizes:
            resultado = resultado @ matriz
        return resultado

    @staticmethod
    def aplicar_transformacoes(vertices, matriz):
        """aplica a matriz de transformação em todos os vértices"""
        transformados = []
        for x, y in vertices:
            # converte o ponto para coordenada homogênea
            coordenada = np.array([x, y, 1])
            # aplica a matriz no ponto
            resultado = coordenada @ matriz
            transformados.append((resultado[0], resultado[1]))
        return transformados

    @staticmethod
    def centro_geometrico(vertices):
        """calcula o centro geométrico a partir da média dos vértices"""
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
        """rotaciona o objeto em torno do seu próprio centro geométrico"""
        dx, dy = Transformacoes.centro_geometrico(vertices)
        rad = math.radians(angulo)
        cos = math.cos(rad)
        sen = math.sin(rad)

        # translada para a origem, rotaciona, translada de volta
        T1 = Transformacoes.translacao(-dx, -dy)
        R  = Transformacoes.rotacao(cos, sen)
        T2 = Transformacoes.translacao(dx, dy)

        # compõe as matrizes e aplica nos vértices
        M = Transformacoes.composicao(T1, R, T2)
        return Transformacoes.aplicar_transformacoes(vertices, M)

    @staticmethod
    def matriz_mundo(x, y, angulo=0, sx=1, sy=1):
        """monta a matriz mundo: escala → rotação → translação (ângulo em graus)"""
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
        """verifica colisão AABB entre dois objetos"""
        # boundbox

        # pega o fator de escala atual de cada objeto
        escala1x = getattr(obj1, "escala_x", 1)
        escala1y = getattr(obj1, "escala_y", 1)
        escala2x = getattr(obj2, "escala_x", 1)
        escala2y = getattr(obj2, "escala_y", 1)

        # tamanho real = tamanho original * escala atual
        largura1 = obj1.largura * escala1x
        altura1  = obj1.altura  * escala1y
        largura2 = obj2.largura * escala2x
        altura2  = obj2.altura  * escala2y

        # objetos são desenhados a partir do centro, então calcula as bordas
        esquerda1 = obj1.x - largura1 / 2
        direita1  = obj1.x + largura1 / 2
        topo1     = obj1.y - altura1  / 2
        baixo1    = obj1.y + altura1  / 2

        esquerda2 = obj2.x - largura2 / 2
        direita2  = obj2.x + largura2 / 2
        topo2     = obj2.y - altura2  / 2
        baixo2    = obj2.y + altura2  / 2

        # há colisão somente se todas as bordas se sobrepõem
        return (
            esquerda1 < direita2
            and direita1 > esquerda2
            and topo1   < baixo2
            and baixo1  > topo2
        )