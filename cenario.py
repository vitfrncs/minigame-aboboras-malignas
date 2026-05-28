import pygame

from desenho import Desenho
from transformações import Transformacoes as T
from config import *

def _poligono(surface, cor, matriz, vertices, lw=0):
    mundo = T.aplicar_transformacoes(vertices, matriz)
    pygame.draw.polygon(surface, cor, mundo, lw)


def desenhar_fundo(surface):

    # grama
    surface.fill(COR_GRAMA)

    # manchas de areia
    manchas = [
        (120, 100, 40),
        (300, 220, 60),
        (600, 150, 50),
        (750, 400, 70),
        (250, 500, 55),
        (550, 550, 45)
    ]

    for x, y, r in manchas:
        Desenho._circulo(surface, COR_AREIA, (x, y), r)

def desenhar_cacto(surface, x, y):

    M = T.translacao(x, y)

    centro = [
        (-8, -8),
        (8, -8),
        (8, 8),
        (-8, 8)
    ]

    braco_cima = [
        (-4, -25),
        (4, -25),
        (4, -8),
        (-4, -8)
    ]

    braco_baixo = [
        (-4, 8),
        (4, 8),
        (4, 25),
        (-4, 25)
    ]

    braco_esq = [
        (-25, -4),
        (-8, -4),
        (-8, 4),
        (-25, 4)
    ]

    braco_dir = [
        (8, -4),
        (25, -4),
        (25, 4),
        (8, 4)
    ]

    _poligono(surface, COR_CACTO, M, centro)
    _poligono(surface, COR_CACTO, M, braco_cima)
    _poligono(surface, COR_CACTO, M, braco_baixo)
    _poligono(surface, COR_CACTO, M, braco_esq)
    _poligono(surface, COR_CACTO, M, braco_dir)

def desenhar_poca(surface, x, y):

    M = T.translacao(x, y)

    vertices = [
        (-40, -20),
        (-20, -35),
        (20, -35),
        (40, -15),
        (35, 15),
        (15, 30),
        (-20, 25),
        (-45, 5)
    ]

    _poligono(surface, COR_AGUA, M, vertices)

def desenhar_pedra(surface, x, y):

    M = T.translacao(x, y)

    pedra = [
        (-12, -6),
        (-5, -12),
        (8, -10),
        (14, 0),
        (8, 10),
        (-8, 8)
    ]

    _poligono(surface, COR_PEDRA, M, pedra)


def desenhar_arbusto(surface, x, y):

    Desenho._circulo(surface, COR_ARBUSTO, (x, y), 10)
    Desenho._circulo(surface, COR_ARBUSTO, (x - 8, y + 3), 8)
    Desenho._circulo(surface, COR_ARBUSTO, (x + 8, y + 3), 8)

def desenhar_cenario(surface):

    desenhar_fundo(surface)
    desenhar_poca(surface, 450, 300)

    # cactos
    cactos = [
        (120, 150),
        (300, 80),
        (650, 120),
        (700, 500),
        (250, 450),
        (500, 300)
    ]

    for x, y in cactos:
        desenhar_cacto(surface, x, y)

    # pedras
    pedras = [
        (180, 320),
        (400, 200),
        (750, 250),
        (600, 420)
    ]

    for x, y in pedras:
        desenhar_pedra(surface, x, y)

    # arbustos
    arbustos = [
        (100, 500),
        (350, 350),
        (520, 150),
        (820, 380)
    ]

    for x, y in arbustos:
        desenhar_arbusto(surface, x, y)