from ui.config import *
from entidades.bala import Bala
import pygame
from transformações import Transformacoes


class Cowboy:

    def __init__(self, x, y):
        self.balas = None
        self.inicial_x = float(x)
        self.inicial_y = float(y)
        self.reset()
        self.speed = COWBOY_VELOCIDADE
        self.largura = 40.0
        self.altura = 60.0
        self.tempo_stun = 1.5  # segundos invulnerável após tomar dano

        # vértices locais de cada parte do cowboy (x, y, largura, altura, cor)
        self.partes = [
            (-24, -34, 48,  8, COR_CHAPEU_1),  # aba do chapéu
            (-14, -46, 28, 14, COR_CHAPEU_2),  # topo do chapéu
            (-12, -24, 24, 24, COR_PELE),       # cabeça
            ( -8, -16,  4,  8, (40, 40, 80)),   # olho esquerdo
            (  4, -16,  4,  8, (40, 40, 80)),   # olho direito
            (-12,   0, 24,  6, (200, 30, 30)),  # lenço
            (-16,   6, 32, 34, COR_BLUSA),      # blusa
            (-12,  40, 10, 16, (70, 40, 20)),   # perna esquerda
            (  2,  40, 10, 16, (70, 40, 20)),   # perna direita
        ]

    def mover(self, keys, dt):
        """Processa o movimento, o stun e o disparo do cowboy a cada frame."""

        # conta o tempo de stun e remove o efeito de dano ao fim dele
        if self.tomou_dano:
            self.tempo_dano += dt
            if self.tempo_dano >= self.tempo_stun:
                self.tomou_dano = False
                self.tempo_dano = 0
                self.escala_x = 1
                self.escala_y = 1

        # movimentação com WASD
        if keys[pygame.K_w]: self.y -= self.speed * dt
        if keys[pygame.K_s]: self.y += self.speed * dt
        if keys[pygame.K_a]: self.x -= self.speed * dt
        if keys[pygame.K_d]: self.x += self.speed * dt

        # define a direção do tiro pela seta pressionada
        atirando = False
        if keys[pygame.K_UP]:
            self.shoot_direction = pygame.Vector2(0, -1)
            atirando = True
        elif keys[pygame.K_DOWN]:
            self.shoot_direction = pygame.Vector2(0, 1)
            atirando = True
        elif keys[pygame.K_LEFT]:
            self.shoot_direction = pygame.Vector2(-1, 0)
            atirando = True
        elif keys[pygame.K_RIGHT]:
            self.shoot_direction = pygame.Vector2(1, 0)
            atirando = True

        # dispara se o cooldown foi cumprido e o cowboy não está stunado
        self.shoot_timer += dt
        if atirando and not self.tomou_dano:
            if self.shoot_timer >= COWBOY_COOLDOWN:
                self.shoot_timer = 0.0
                self.balas.append(
                    Bala(self.x, self.y, self.shoot_direction, "cowboy")
                )

        # remove balas fora da tela e atualiza as restantes
        self.balas = [b for b in self.balas if not b.fora_da_tela()]
        for b in self.balas:
            b.atualizar(dt)

        return self.x, self.y

    def desenhar(self, screen):
        """Desenha o cowboy e suas balas na tela aplicando as transformações atuais"""
        matriz = Transformacoes.matriz_mundo(self.x, self.y, 0, self.escala_x, self.escala_y)

        # transforma e desenha cada parte do cowboy
        for px, py, w, h, cor in self.partes:
            vertices = [
                (px,     py),
                (px + w, py),
                (px + w, py + h),
                (px,     py + h)
            ]
            vertices_transformados = Transformacoes.aplicar_transformacoes(vertices, matriz)
            pygame.draw.polygon(screen, cor, vertices_transformados)

        # desenha as balas do cowboy
        for b in self.balas:
            b.desenhar(screen)

    def reset(self):
        """reseta o cowboy para o estado inicial"""
        self.x = self.inicial_x
        self.y = self.inicial_y
        self.escala_x = 1.0
        self.escala_y = 1.0
        self.shoot_direction = pygame.Vector2(1, 0)
        self.shoot_timer = 0.0
        self.balas = []
        self.tomou_dano = False
        self.tempo_dano = 0.0