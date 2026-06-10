from entidades.cowboy import *
from entidades.inimigos import Inimigos
from entidades.shooter import Shooter
from transformações import Transformacoes
from ui.cenario import *
import random


if __name__ == "__main__":
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITLE)

    fonte = pygame.font.SysFont(None, 36)

    # Configurações iniciais ==============================================

    # pontuação e estado do jogo
    record = 0
    score = 0
    vidas = 3
    game_over = False
    game_won = False

    clock = pygame.time.Clock()

    # cria o cowboy no centro da tela
    cowboy = Cowboy(400, 300)

    margem = MARGEM

    # controla o tempo entre spawns de inimigos
    intervalo_spawn = INTERVALO_SPAWN
    tempo_spawn = TEMPO_SPAWN

    # Inicialização dos inimigos: posição inicial ==========================

    # inimigos iniciais nas bordas da tela
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

    # shooters nos cantos da tela
    shooters = [
        Shooter(margem, ALTURA * 0.25),
        Shooter(margem, ALTURA * 0.75),
        Shooter(LARGURA - margem, ALTURA * 0.25),
        Shooter(LARGURA - margem, ALTURA * 0.75),
    ]

    # Loop principal do jogo ================================

    rodando = True

    while rodando:

        ''' Spawn de novos inimigos laranjas =================='''

        # dt para movimento independente de fps
        dt = clock.tick(FPS) / 1000

        # acumula tempo para spawn de novos inimigos
        tempo_spawn += dt

        # gera inimigos aleatoriamente a cada 2 segundos
        if tempo_spawn >= intervalo_spawn and game_over == False and game_won == False:

            # sorteia um dos 4 lados da tela
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

            # adiciona o novo inimigo na lista
            inimigos.append(Inimigos(x, y))

            tempo_spawn = 0

        """ Eventos ================================================"""

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                rodando = False

            # reiniciar jogo ao pressionar R na tela de game over
            if evento.type == pygame.KEYDOWN:

                if (game_over or game_won) and evento.key == pygame.K_r:

                    # reseta pontuação e estado
                    score = 0
                    vidas = 3
                    game_over = False
                    game_won = False

                    # reseta posição e estado do cowboy
                    cowboy.x = LARGURA / 2
                    cowboy.y = ALTURA / 2
                    cowboy.balas.clear()
                    cowboy.escala_x = 1
                    cowboy.escala_y = 1
                    cowboy.tomou_dano = False
                    cowboy.tempo_dano = 0

                    # recria inimigos nas posições iniciais
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

                    # recria shooters nos cantos
                    shooters = [
                        Shooter(margem, ALTURA * 0.25),
                        Shooter(margem, ALTURA * 0.75),
                        Shooter(LARGURA - margem, ALTURA * 0.25),
                        Shooter(LARGURA - margem, ALTURA * 0.75),
                    ]

        # desenha o fundo e elementos do cenário
        desenhar_cenario(tela)

        if not game_over:
            teclas = pygame.key.get_pressed()
            cowboy.mover(teclas, dt)

            """Colisões =========================================="""

            # verifica colisão das balas do cowboy com inimigos e shooters
            for bullet in cowboy.balas[:]:

                acertou = False

                # checa colisão com abóboras normais
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

                # checa colisão com shooters roxos
                for shooter in shooters[:]:

                    if Transformacoes.colisao(bullet, shooter):

                        if bullet in cowboy.balas:
                            cowboy.balas.remove(bullet)

                        shooters.remove(shooter)
                        score += 20
                        break

            # verifica colisão de inimigos com o cowboy (só se não tomou dano recentemente)
            if not cowboy.tomou_dano:

                # abóboras normais encostam no cowboy
                for enemy in inimigos:

                    if Transformacoes.colisao(enemy, cowboy):

                        vidas -= 1

                        # aplica efeito de dano
                        cowboy.tomou_dano = True
                        cowboy.tempo_dano = 0
                        cowboy.escala_x = 0.5
                        cowboy.escala_y = 0.5

                        if vidas <= 0:
                            game_over = True

                        break

                # shooters roxos encostam no cowboy
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

            """Tratamento de movimentação ==============="""

            # move as abóboras em direção ao cowboy
            for inimigo in inimigos:
                inimigo.mover(cowboy.x, cowboy.y, dt)

            # move os shooters, verifica colisão das balas deles com o cowboy
            for shooter in shooters:

                if not cowboy.tomou_dano:
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

                shooter.mover(cowboy.x, cowboy.y, dt)

        """Redesenhar entidades de acordo com nova posição =================="""

        # desenha todos os personagens na tela
        for inimigo in inimigos:
            inimigo.desenhar(tela)

        for shooter in shooters:
            shooter.desenhar(tela)

        cowboy.desenhar(tela)

        """ Score, vidas e record ==========================================="""

        # score, vidas e record no canto superior esquerdo
        texto_score = fonte.render(f"Score: {score}", True, COR_BRANCO)
        tela.blit(texto_score, (10, 10))

        texto_vidas = fonte.render(f"Vidas: {vidas}", True, COR_BRANCO)
        tela.blit(texto_vidas, (10, 45))

        texto_record = fonte.render(f"Record: {record}", True, (255, 255, 0))
        tela.blit(texto_record, (10, 80))

        """ Tela de game over ==============================================="""
        if game_over:

            # fundo preto
            tela.fill((0, 0, 0))

            # atualiza record se o score atual for maior
            if score > record:
                record = score

            # fontes maiores para a tela de game over
            fonte_gameover = pygame.font.SysFont(None, 120)
            fonte_texto = pygame.font.SysFont(None, 40)

            # título GAME OVER em roxo
            texto_gameover = fonte_gameover.render(
                "GAME OVER",
                True,
                (255, 0, 0)
            )

            # instrução para reiniciar
            texto_restart = fonte_texto.render(
                "Pressione R para reiniciar",
                True,
                (255, 255, 255)
            )

            # pontuação final em amarelo
            texto_score_final = fonte_texto.render(
                f"Score Final: {score}",
                True,
                (255, 220, 0)
            )

            # centraliza os textos na tela
            rect_gameover = texto_gameover.get_rect(
                center=(LARGURA / 2, ALTURA / 2 - 80)
            )

            rect_restart = texto_restart.get_rect(
                center=(LARGURA / 2, ALTURA / 2 + 20)
            )

            rect_score = texto_score_final.get_rect(
                center=(LARGURA / 2, ALTURA / 2 + 70)
            )

            # desenha os textos na tela
            tela.blit(texto_gameover, rect_gameover)
            tela.blit(texto_restart, rect_restart)
            tela.blit(texto_score_final, rect_score)

        # verificar se o jogo foi ganho
        if len(inimigos) == 0 and len(shooters) == 0:
            game_won = True

        """ Tela de game won ==============================================="""

        if game_won:
            # fundo preto
            tela.fill((0, 0, 0))

            # atualiza record se o score atual for maior
            if score > record:
                record = score

            # fontes maiores para a tela de game over
            fonte_gameover = pygame.font.SysFont(None, 120)
            fonte_texto = pygame.font.SysFont(None, 40)

            # título GAME OVER em roxo
            texto_gameover = fonte_gameover.render(
                "GAME WON",
                True,
                (180, 60, 255)
            )

            # instrução para reiniciar
            texto_restart = fonte_texto.render(
                "Pressione R para reiniciar",
                True,
                (255, 255, 255)
            )

            # pontuação final em amarelo
            texto_score_final = fonte_texto.render(
                f"Score Final: {score}",
                True,
                (255, 220, 0)
            )

            # centraliza os textos na tela
            rect_gameover = texto_gameover.get_rect(
                center=(LARGURA / 2, ALTURA / 2 - 80)
            )

            rect_restart = texto_restart.get_rect(
                center=(LARGURA / 2, ALTURA / 2 + 20)
            )

            rect_score = texto_score_final.get_rect(
                center=(LARGURA / 2, ALTURA / 2 + 70)
            )

            # desenha os textos na tela
            tela.blit(texto_gameover, rect_gameover)
            tela.blit(texto_restart, rect_restart)
            tela.blit(texto_score_final, rect_score)

        # atualiza a tela
        pygame.display.flip()