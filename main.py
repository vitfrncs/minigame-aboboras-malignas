from cowboy import *
from inimigos import Inimigos
from shooter import Shooter
from transformações import Transformacoes
from cenario import *
import random


if __name__ == "__main__":
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITLE)

    fonte = pygame.font.SysFont(None, 36)

    record = 0
    score = 0
    vidas = 3
    game_over = False

    clock = pygame.time.Clock()

    cowboy = Cowboy(400, 300)

    margem = 40

    intervalo_spawn = 1
    tempo_spawn = 0

    inimigos = [

        # topo
        Inimigos(LARGURA * 0.25, margem),
        Inimigos(LARGURA * 0.50, margem),
        Inimigos(LARGURA * 0.75, margem),

        # baixo
        Inimigos(LARGURA * 0.25, ALTURA - margem),
        Inimigos(LARGURA * 0.50, ALTURA - margem),
        Inimigos(LARGURA * 0.75, ALTURA - margem),

        # esquerda
        Inimigos(margem, ALTURA * 0.50),

        # direita
        Inimigos(LARGURA - margem, ALTURA * 0.50),
    ]

    shooters = [
        Shooter(margem, ALTURA * 0.25),
        Shooter(margem, ALTURA * 0.75),
        Shooter(LARGURA - margem, ALTURA * 0.25),
        Shooter(LARGURA - margem, ALTURA * 0.75),
    ]

    rodando = True

    while rodando:

        dt = clock.tick(FPS) / 1000

        tempo_spawn += dt
        # gera inimigos aleatoriamente a cada 2 segundos
        if tempo_spawn >= intervalo_spawn:

            lado = random.randint(0, 3)

            if lado == 0:  # topo
                x = random.randint(margem, LARGURA - margem)
                y = margem

            elif lado == 1:  # baixo
                x = random.randint(margem, LARGURA - margem)
                y = ALTURA - margem

            elif lado == 2:  # esquerda
                x = margem
                y = random.randint(margem, ALTURA - margem)

            else:  # direita
                x = LARGURA - margem
                y = random.randint(margem, ALTURA - margem)

            inimigos.append(Inimigos(x, y))

            tempo_spawn = 0

        # eventos
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                rodando = False

            # reiniciar
            if evento.type == pygame.KEYDOWN:

                if game_over and evento.key == pygame.K_r:
                    score = 0
                    vidas = 3
                    game_over = False

                    cowboy.x = LARGURA / 2
                    cowboy.y = ALTURA / 2

                    cowboy.balas.clear()

                    cowboy.escala_x = 1
                    cowboy.escala_y = 1

                    cowboy.tomou_dano = False
                    cowboy.tempo_dano = 0
                    inimigos = [

                        Inimigos(LARGURA * 0.25, margem),
                        Inimigos(LARGURA * 0.50, margem),
                        Inimigos(LARGURA * 0.75, margem),

                        Inimigos(LARGURA * 0.25, ALTURA - margem),
                        Inimigos(LARGURA * 0.50, ALTURA - margem),
                        Inimigos(LARGURA * 0.75, ALTURA - margem),

                        Inimigos(margem, ALTURA * 0.50),
                        Inimigos(LARGURA - margem, ALTURA * 0.50),
                    ]

                    shooters = [
                        Shooter(margem, ALTURA * 0.25),
                        Shooter(margem, ALTURA * 0.75),
                        Shooter(LARGURA - margem, ALTURA * 0.25),
                        Shooter(LARGURA - margem, ALTURA * 0.75),
                    ]

        # desenhar cenario
        desenhar_cenario(tela)


        if not game_over:
            teclas = pygame.key.get_pressed()
            cowboy.move(teclas, dt)

            # Lógica de colisões de balas do cowboy
            # tiros do cowboy
            for bullet in cowboy.balas[:]:

                acertou = False

                # inimigos normais
                for enemy in inimigos[:]:

                    if Transformacoes.colisao(bullet, enemy):

                        if bullet in cowboy.balas:
                            cowboy.balas.remove(bullet)

                        inimigos.remove(enemy)

                        score += 10

                        acertou = True

                        break

                if acertou:
                    continue

                # shooters
                for shooter in shooters[:]:

                    if Transformacoes.colisao(bullet, shooter):

                        if bullet in cowboy.balas:
                            cowboy.balas.remove(bullet)

                        shooters.remove(shooter)

                        score += 20

                        break

            # =========================
            # COLISÃO INIMIGOS x COWBOY
            # =========================

            if not cowboy.tomou_dano:

                # abóboras normais
                for enemy in inimigos:

                    if Transformacoes.colisao(enemy, cowboy):

                        vidas -= 1

                        cowboy.tomou_dano = True
                        cowboy.tempo_dano = 0

                        cowboy.escala_x = 0.5
                        cowboy.escala_y = 0.5

                        if vidas <= 0:
                            game_over = True

                        break

                # shooters roxos
                for shooter in shooters:

                    if Transformacoes.colisao(shooter, cowboy):

                        vidas -= 1

                        cowboy.tomou_dano = True
                        cowboy.tempo_dano = 0

                        cowboy.escala_x = 0.5
                        cowboy.escala_y = 0.5

                        if vidas <= 0:
                            game_over = True

                        break

            # BALAS DOS SHOOTERS
            if not cowboy.tomou_dano:

                for shooter in shooters:

                    for bullet in shooter.balas[:]:

                        if Transformacoes.colisao(bullet, cowboy):

                            shooter.balas.remove(bullet)

                            vidas -= 1

                            cowboy.tomou_dano = True
                            cowboy.tempo_dano = 0

                            cowboy.escala_x = 0.5
                            cowboy.escala_y = 0.5

                            if vidas <= 0:
                                game_over = True

                            break

            # Atualiza e desenha Inimigos comuns
            for inimigo in inimigos:
                inimigo.mover(cowboy.x, cowboy.y, dt)

            # Atualiza Shooters e suas balas
            for shooter in shooters:
                for bullet in shooter.balas[:]:

                    if Transformacoes.colisao(bullet, cowboy):

                        shooter.balas.remove(bullet)

                        vidas -= 1

                        # efeito dano
                        cowboy.tomou_dano = True
                        cowboy.tempo_dano = 0

                        cowboy.escala_x = 0.5
                        cowboy.escala_y = 0.5

                        if vidas <= 0:
                            game_over = True
                shooter.mover(cowboy.x, cowboy.y, dt)

        for inimigo in inimigos:
            inimigo.desenhar(tela)

        for shooter in shooters:
            shooter.desenhar(tela)

        cowboy.desenhar(tela)


        texto_score = fonte.render(f"Score: {score}", True, COR_BRANCO)
        tela.blit(texto_score, (10, 10))

        texto_vidas = fonte.render(f"Vidas: {vidas}", True, COR_BRANCO)
        tela.blit(texto_vidas, (10, 45))

        texto_record = fonte.render(f"Record: {record}", True, (255, 255, 0))
        tela.blit(texto_record, (10, 80))

        if game_over:

            # fundo preto
            tela.fill((0, 0, 0))

            # atualiza record
            if score > record:
                record = score

            # fontes
            fonte_gameover = pygame.font.SysFont(None, 120)
            fonte_texto = pygame.font.SysFont(None, 40)

            # GAME OVER roxo
            texto_gameover = fonte_gameover.render(
                "GAME OVER",
                True,
                (180, 60, 255)
            )

            # texto reiniciar
            texto_restart = fonte_texto.render(
                "Pressione R para reiniciar",
                True,
                (255, 255, 255)
            )

            # score final
            texto_score_final = fonte_texto.render(
                f"Score Final: {score}",
                True,
                (255, 220, 0)
            )

            # posições
            rect_gameover = texto_gameover.get_rect(
                center=(LARGURA / 2, ALTURA / 2 - 80)
            )

            rect_restart = texto_restart.get_rect(
                center=(LARGURA / 2, ALTURA / 2 + 20)
            )

            rect_score = texto_score_final.get_rect(
                center=(LARGURA / 2, ALTURA / 2 + 70)
            )

            # desenha
            tela.blit(texto_gameover, rect_gameover)
            tela.blit(texto_restart, rect_restart)
            tela.blit(texto_score_final, rect_score)
        pygame.display.flip()