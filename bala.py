from config import *
from transformações import Transformacoes
import pygame
import math


class Bala:

    def __init__(self, x, y, direcao: pygame.Vector2, tipo="cowboy"):

        self.pos = pygame.Vector2(x, y)

        self.dir = direcao.normalize()

        self.tipo = tipo

        self.largura = 8
        self.altura = 8

        # =========================
        # BALA DO COWBOY
        # =========================
        if self.tipo == "cowboy":

            self.cor = (255, 220, 120)

            self.vertices_locais = [

                (0, -6),
                (3, 0),
                (0, 6),
                (-3, 0),
            ]

        # =========================
        # SEMENTE DAS ABÓBORAS
        # =========================
        else:

            self.cor = (230, 240, 200)

            self.vertices_locais = [

                (0, -5),
                (2, -2),
                (2, 2),
                (0, 5),
                (-2, 2),
                (-2, -2),
            ]

    def atualizar(self, dt):

        self.pos += (self.dir * BALA_VELOCIDADE * dt)

    def fora_da_tela(self):

        return not (
                0 <= self.pos.x <= LARGURA
                and
                0 <= self.pos.y <= ALTURA
        )

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    def _matriz_mundo(self):

        angulo = math.degrees(

            math.atan2(
                self.dir.y,
                self.dir.x
            )

        ) + 90

        return Transformacoes.matriz_mundo(

            self.pos.x,
            self.pos.y,
            angulo
        )

    def desenhar(self, screen):

        vertices_mundo = (
            Transformacoes.aplicar_transformacoes(
                self.vertices_locais,
                self._matriz_mundo()
            )
        )

        # preenchimento
        pygame.draw.polygon(
            screen,
            self.cor,
            vertices_mundo
        )

        # contorno
        pygame.draw.polygon(
            screen,
            (0, 0, 0),
            vertices_mundo,
            2
        )