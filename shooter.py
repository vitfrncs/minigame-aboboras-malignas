import pygame
from config import *
from bala import Bala
from transformações import Transformacoes


class Shooter:

    def __init__(self, x, y):

        self.x = float(x)
        self.y = float(y)

        self.speed = INIMIGOS_VELOCIDADE

        self.largura = 40
        self.altura = 40

        self.escala_x = 1
        self.escala_y = 1

        self.shoot_direction = pygame.Vector2(0, 0)

        self.shoot_timer = 0.0

        self.balas = []

        ## abobora roxa
        self.partes = [

            # caule
            (-4, -26, 8, 8, (120, 70, 140)),

            # topo
            (-18, -18, 36, 10, (170, 90, 220)),

            # meio
            (-22, -8, 44, 18, (140, 60, 200)),

            # baixo
            (-18, 10, 36, 12, (100, 40, 160)),

            # olhos vermelhos
            (-12, -2, 6, 6, (255, 0, 0)),
            (6, -2, 6, 6, (255, 0, 0)),

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

        # direção do shooter até o cowboy
        direcao = alvo - pos

        if direcao.length() > 0:

            direcao = direcao.normalize()

            self.shoot_direction = direcao

        # contador
        self.shoot_timer += dt

        # atira
        if self.shoot_timer >= 1.2:

            self.shoot_timer = 0.0

            self.balas.append(

                Bala(
                    self.x,
                    self.y,
                    self.shoot_direction,
                    "semente"
                )
            )

        # remove balas fora
        self.balas = [
            b for b in self.balas
            if not b.fora_da_tela()
        ]

        # atualiza balas
        for b in self.balas:
            b.atualizar(dt)

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

        # desenha corpo
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

        # balas
        for b in self.balas:
            b.desenhar(screen)