import pygame
from ui.config import *
from transformações import Transformacoes


class Inimigos:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.speed = INIMIGOS_VELOCIDADE
        self.largura = INIMIGO_LARGURA
        self.altura = INIMIGO_ALTURA
        self.escala_x = 1
        self.escala_y = 1

        # partes da abóbora (x, y, largura, altura, cor)
        self.partes = [
            (-4,  -26,  8,  8, COR_CAULE),    # caule
            (-18, -18, 36, 10, COR_ABOBORA_1), # topo
            (-22,  -8, 44, 18, COR_ABOBORA_2), # meio
            (-18,  10, 36, 12, COR_ABOBORA_3), # baixo
            (-12,  -2,  6,  6, COR_PRETO),     # olho esquerdo
            (  6,  -2,  6,  6, COR_PRETO),     # olho direito
            (-10,  10, 20,  4, COR_PRETO),     # boca
        ]

        # sobrancelhas malignas
        self.sobrancelhas = [
            # esquerda
            [(-16, -10), (-6, -6), (-6, -4), (-16, -8)],
            # direita
            [(16, -10), (6, -6), (6, -4), (16, -8)],
        ]

    def mover(self, cowboy_x, cowboy_y, dt):
        """Move o inimigo em direção ao cowboy a cada frame."""
        pos   = pygame.Vector2(self.x, self.y)
        alvo  = pygame.Vector2(cowboy_x, cowboy_y)
        direcao = alvo - pos

        # normaliza para manter velocidade constante em qualquer direção
        if direcao.length() > 0:
            direcao = direcao.normalize()
            self.x += direcao.x * self.speed * dt
            self.y += direcao.y * self.speed * dt

    def desenhar(self, screen):
        """Desenha a abóbora na tela aplicando escala e translação."""

        # matriz mundo: escala → translação
        matriz = Transformacoes.composicao(
            Transformacoes.escala(self.escala_x, self.escala_y),
            Transformacoes.translacao(self.x, self.y)
        )

        # desenha o corpo da abóbora
        for px, py, w, h, cor in self.partes:
            vertices = [
                (px,     py),
                (px + w, py),
                (px + w, py + h),
                (px,     py + h)
            ]
            vertices_transformados = Transformacoes.aplicar_transformacoes(vertices, matriz)
            pygame.draw.polygon(screen, cor, vertices_transformados)

        # desenha as sobrancelhas do mal
        for sobrancelha in self.sobrancelhas:
            vertices_transformados = Transformacoes.aplicar_transformacoes(sobrancelha, matriz)
            pygame.draw.polygon(screen, COR_PRETO, vertices_transformados)