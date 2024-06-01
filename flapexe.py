import pygame
import os
import random
import neat

ai_jogando = False 
geracao = 0

TELA_LAR = 500
TELA_ALT = 800
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


IMAGEM_CAN = pygame.transform.scale2x(pygame.image.load(os.path.join("Saved Pictures", "pipe.png")))
IMAGEM_CHA = pygame.transform.scale2x(pygame.image.load(os.path.join("Saved Pictures", "base.png")))
IMAGEM_BACK = pygame.transform.scale2x(pygame.image.load(os.path.join("Saved Pictures", "bg.png")))
IMAGENS_PAS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("Saved Pictures", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Saved Pictures", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("Saved Pictures", "bird3.png"))),

]

pygame.font.init()
FONTE_P = pygame.font.SysFont('arial', 50)
#FONTE_Menu =  pygame.font.SysFont('arial', 60)


class Passaro:
    IMGS = IMAGENS_PAS
    ROTACAO_MAX = 25
    VELOCIDADE_ROTA = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def jump(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAX:
                self.angulo = self.ROTACAO_MAX
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTA

    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_cen_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_cen_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DIS = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CAN, False, True)
        self.CANO_BASE = IMAGEM_CAN
        self.passou = False
        self.definir_altura()
        self.tempo = 0
        self.passaro = Passaro(230, 350)

    def definir_altura(self):
        self.altura = random.randrange(100, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DIS

    def mover(self):
        self.tempo += 1
        self.x -= self.VEL + self.tempo

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        return base_ponto or topo_ponto
            


class Chao:
    VEL = 5
    LAR = IMAGEM_CHA.get_width()
    IMAGEM = IMAGEM_CHA

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.LAR
        self.tempo = 0

    def mover(self):
        self.tempo += 1
        self.x0 -= self.VEL +self.tempo
        self.x1 -= self.VEL +self.tempo

        if self.x0 + self.LAR < 0:
            self.x0 = self.x1 + self.LAR
        if self.x1 + self.LAR < 0:
            self.x1 = self.x0 + self.LAR

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x0, self.y))
        tela.blit(self.IMAGEM, (self.x1, self.y))

class Button:
    def __init__(self, text,x, y,width,height,color, hover_color, action = None):
        self.text = text
        self.rect= pygame.Rect(x,y,width,height)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def desenhar(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(tela,self.hover_color,self.rect)
        else:
            pygame.draw.rect(tela,self.color,self.rect)
        
        font = pygame.font.Font(None,36)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center = self.rect.center)
        tela.blit(text_surf,text_rect)
    
    def check_click(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                return True
        return False           

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACK, (0, 0))

    for pas in passaros:
        pas.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
    texto = FONTE_P.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LAR - 10 - texto.get_width(), 10))

    if ai_jogando[1] == True:
        texto = FONTE_P.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))

    chao.desenhar(tela)
    pygame.display.update()


def main(genomas, config):  # fitness function

    global geracao
    geracao += 1
    chao = Chao(730)
    canos = [Cano(800)]
    tela = pygame.display.set_mode((TELA_LAR, TELA_ALT))
    pontos = 0
    relogio = pygame.time.Clock()
    ai_jogando = menu(tela)
    rodando = menu(tela)


    print()
    if ai_jogando[1] == True :
        redes = []
        lista_genomas = []
        passaros = []
        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            lista_genomas.append(genoma)
            passaros.append(Passaro(230, 350))
    else:
        passaros = [Passaro(230, 350)]
    


    while rodando:
        relogio.tick(30)

        # interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if not ai_jogando:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        for passaro in passaros:
                            passaro.jump()

        indice_cano = 0
        if len(passaros) > 0:
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO.get_width()):
                indice_cano = 1
        else:
            rodando = False
            break

        # mover as coisas
        for i, passaro in enumerate(passaros):
            passaro.mover()

            if ai_jogando[1] == True:
                lista_genomas[i].fitness += 0.1
                output = redes[i].activate((passaro.y,
                                            abs(passaro.y - canos[indice_cano].altura),
                                            abs(passaro.y - canos[indice_cano].pos_base)))
                # -1 e 1 -> se o output for > 0.5 então o passaro pula
                if output[0] > 0.5:
                        passaro.jump()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if ai_jogando[1] == True:
                        lista_genomas[i].fitness -= 1
                        lista_genomas.pop(i)
                        redes.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
            canos.append(Cano(900))
            for genoma in lista_genomas:
                genoma.fitness += 5
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

                if ai_jogando[1] == True:
                    lista_genomas.pop(i)
                    redes.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)

def menu(tela):
    global ai

    pygame.display.set_caption("Menu de Jogo")
    def set_ai_jogando():
        global ai
        ai = True

    def set_jogador():
        global ai
        ai = False

    def iniciar_jogo():
        nonlocal rodando
        rodando = False

    def sair_jogo():
        pygame.quit()
        quit()
    
    botao1= Button("Iniciar jogo", 150,300,200,50,RED,GREEN, iniciar_jogo)
    botao2 = Button("modo jogador",150, 375, 200,50, RED, GREEN, set_jogador)
    botao3 = Button("modo ia",150, 450, 200,50, RED, GREEN, set_ai_jogando)
    botao4= Button("sair",150, 550, 200,50, RED, GREEN, sair_jogo)
    rodando= True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()

            botao1.check_click(evento)
            botao2.check_click(evento)
            botao3.check_click(evento)
            botao4.check_click(evento)
                
        tela.blit(IMAGEM_BACK, (0,0))
        botao1.desenhar(tela)
        botao2.desenhar(tela)
        botao3.desenhar(tela)
        botao4.desenhar(tela)
        pygame.display.update()
    return True, ai             

def rodar(caminho_config):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                caminho_config)

    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())
    if ai_jogando:
        populacao.run(main, 50)
    else:
        main(None, None)


# Execução principal
if __name__ == '__main__':
    caminho = os.path.dirname(__file__)
    caminho_config = os.path.join(caminho, 'config.txt')
    rodar(caminho_config)