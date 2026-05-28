import pygame

class Desenho:
    @staticmethod
    def _circulo(screen, cor, posicao, angulo):
        return pygame.draw.circle(screen, cor, posicao, angulo)

    @staticmethod
    def _retangulo(screen, cor, posicao):
        return pygame.draw.rect(screen, cor, posicao)

    @staticmethod
    def _linha(screen, cor, inicio, fim, largura):
        return pygame.draw.line(screen, cor, inicio, fim, largura)