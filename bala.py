from config import *
from transformações import Transformacoes
import pygame
import math


class Bala:

    def __init__(self, x, y, direcao: pygame.Vector2, tipo="cowboy"):

        self.pos = pygame.Vector2(x, y)
        self.dir = direcao.normalize()

        self.tipo = tipo

        self.largura = BALA_COWBOY_LARGURA
        self.altura = BALA_COWBOY_ALTURA

        # configura aparência da bala de acordo com o atirador
        if self.tipo == "cowboy":

            self.cor = BALA_COWBOY_COR

            self.vertices_locais = [

                (0, -6),
                (3, 0),
                (0, 6),
                (-3, 0),
            ]

        # configura a aparência da semente lançada pelas abóboras
        else:

            self.cor = SEMENTE_COR

            self.vertices_locais = [

                (0, -5),
                (2, -2),
                (2, 2),
                (0, 5),
                (-2, 2),
                (-2, -2),
            ]

    def atualizar(self, dt):

        # move a bala na direção definida
        self.pos += (self.dir * BALA_VELOCIDADE * dt)

    def fora_da_tela(self):

        # verifica se a bala saiu dos limites da janela
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

        # calcula a rotação necessária para alinhar
        # o desenho da bala com sua direção de movimento
        angulo = math.degrees(

            math.atan2(
                self.dir.y,
                self.dir.x
            )

        ) + 90

        # cria a transformação final da bala no mundo
        return Transformacoes.matriz_mundo(

            self.pos.x,
            self.pos.y,
            angulo
        )

    def desenhar(self, screen):

        # aplica rotação e translação aos vértices locais
        vertices_mundo = (
            Transformacoes.aplicar_transformacoes(
                self.vertices_locais,
                self._matriz_mundo()
            )
        )

        # desenha o corpo da bala
        pygame.draw.polygon(
            screen,
            self.cor,
            vertices_mundo
        )

        # desenha o contorno para melhorar a visualização
        pygame.draw.polygon(
            screen,
            COR_PRETO,
            vertices_mundo,
            2
        )