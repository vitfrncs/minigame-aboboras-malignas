import pygame
from ui.config import *
from entidades.bala import Bala
from transformações import Transformacoes


class Shooter:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.speed = INIMIGOS_VELOCIDADE
        self.largura = SHOOTER_LARGURA
        self.altura = SHOOTER_ALTURA
        self.escala_x = 1
        self.escala_y = 1
        self.shoot_direction = pygame.Vector2(0, 0)
        self.shoot_timer = 0.0
        self.balas = []

        # partes da abóbora roxa (x, y, largura, altura, cor)
        self.partes = [
            ( -4, -26,  8,  8, COR_SHOOTER_CAULE),  # caule
            (-18, -18, 36, 10, COR_SHOOTER_1),       # topo
            (-22,  -8, 44, 18, COR_SHOOTER_2),       # meio
            (-18,  10, 36, 12, COR_SHOOTER_3),       # baixo
            (-12,  -2,  6,  6, COR_OLHO_SHOOTER),   # olho esquerdo
            (  6,  -2,  6,  6, COR_OLHO_SHOOTER),   # olho direito
            (-10,  10, 20,  4, COR_PRETO),           # boca
        ]

        # sobrancelhas malignas (polígonos separados)
        self.sobrancelhas = [
            # esquerda
            [(-16, -10), (-6, -6), (-6, -4), (-16, -8)],
            # direita
            [(16, -10), (6, -6), (6, -4), (16, -8)],
        ]

    def mover(self, cowboy_x, cowboy_y, dt):
        """Move o shooter em direção ao cowboy e dispara periodicamente."""
        pos    = pygame.Vector2(self.x, self.y)
        alvo   = pygame.Vector2(cowboy_x, cowboy_y)
        direcao = alvo - pos

        # normaliza para manter velocidade constante e salva direção do tiro
        if direcao.length() > 0:
            direcao = direcao.normalize()
            self.shoot_direction = direcao

        # acumula tempo e atira ao atingir o cooldown
        self.shoot_timer += dt
        if self.shoot_timer >= SHOOTER_COOLDOWN:
            self.shoot_timer = 0.0
            self.balas.append(
                Bala(self.x, self.y, self.shoot_direction, "semente")
            )

        # remove balas fora da tela e atualiza as restantes
        self.balas = [b for b in self.balas if not b.fora_da_tela()]
        for b in self.balas:
            b.atualizar(dt)

    def desenhar(self, screen):
        """Desenha o shooter e suas balas na tela aplicando escala e translação."""
        # matriz mundo: escala → translação
        matriz = Transformacoes.composicao(
            Transformacoes.escala(self.escala_x, self.escala_y),
            Transformacoes.translacao(self.x, self.y)
        )

        # desenha o corpo da abóbora roxa
        for px, py, w, h, cor in self.partes:
            vertices = [
                (px,     py),
                (px + w, py),
                (px + w, py + h),
                (px,     py + h)
            ]
            vertices_transformados = Transformacoes.aplicar_transformacoes(vertices, matriz)
            pygame.draw.polygon(screen, cor, vertices_transformados)

        # desenha as sobrancelhas malignas
        for sobrancelha in self.sobrancelhas:
            vertices_transformados = Transformacoes.aplicar_transformacoes(sobrancelha, matriz)
            pygame.draw.polygon(screen, COR_PRETO, vertices_transformados)

        # desenha as balas disparadas
        for b in self.balas:
            b.desenhar(screen)