import pygame
from config import *
from transformações import Transformacoes


class Inimigos:

    def __init__(self, x, y):

        self.x = float(x)
        self.y = float(y)

        self.speed = INIMIGOS_VELOCIDADE

        self.largura = 40
        self.altura = 40

        self.escala_x = 1
        self.escala_y = 1

        # abóbora pixel art
        # x, y, largura, altura, cor
        self.partes = [

            # caule
            (-4, -26, 8, 8, (50, 120, 40)),

            # topo
            (-18, -18, 36, 10, (255, 140, 0)),

            # meio
            (-22, -8, 44, 18, (255, 120, 0)),

            # baixo
            (-18, 10, 36, 12, (230, 100, 0)),

            # olhos
            (-12, -2, 6, 6, (0, 0, 0)),
            (6, -2, 6, 6, (0, 0, 0)),

            # boca
            (-10, 10, 20, 4, (0, 0, 0)),
        ]

        # sobrancelhas malignas
        self.sobrancelhas = [

            # esquerda
            [
                (-16, -10),
                (-6, -6),
                (-6, -4),
                (-16, -8)
            ],

            # direita
            [
                (16, -10),
                (6, -6),
                (6, -4),
                (16, -8)
            ]
        ]

    def mover(self, cowboy_x, cowboy_y, dt):

        pos = pygame.Vector2(
            self.x,
            self.y
        )

        alvo = pygame.Vector2(
            cowboy_x,
            cowboy_y
        )

        direcao = alvo - pos

        if direcao.length() > 0:

            direcao = direcao.normalize()

            self.x += direcao.x * self.speed * dt
            self.y += direcao.y * self.speed * dt

    def desenhar(self, screen):

        # matriz com escala + translação
        matriz = Transformacoes.composicao(

            Transformacoes.escala(
                self.escala_x,
                self.escala_y
            ),

            Transformacoes.translacao(
                self.x,
                self.y
            )
        )

        # corpo da abóbora
        for px, py, w, h, cor in self.partes:

            vertices = [
                (px, py),
                (px + w, py),
                (px + w, py + h),
                (px, py + h)
            ]

            vertices_transformados = (
                Transformacoes.aplicar_transformacoes(
                    vertices,
                    matriz
                )
            )

            pygame.draw.polygon(
                screen,
                cor,
                vertices_transformados
            )

        # sobrancelhas
        for sobrancelha in self.sobrancelhas:

            vertices_transformados = (
                Transformacoes.aplicar_transformacoes(
                    sobrancelha,
                    matriz
                )
            )

            pygame.draw.polygon(
                screen,
                (0, 0, 0),
                vertices_transformados
            )