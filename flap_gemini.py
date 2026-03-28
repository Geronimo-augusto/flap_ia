import pygame
import os
import random
import neat
import sys

# --- CONFIGURAÇÕES E CONSTANTES ---
CONFIG = {
    "TELA": {"LARGURA": 500, "ALTURA": 800},
    "CORES": {"BRANCO": (255, 255, 255), "PRETO": (0, 0, 0), "BOTAO": (200, 0, 0), "HOVER": (0, 200, 0)},
    "FISICA": {"GRAVIDADE": 1.5, "PULO": -10.5, "VELOCIDADE_MAX": 16},
    "ASSETS": "Saved Pictures"
}

def carregar_imagem(nome, scale=2):
    caminho = os.path.join(CONFIG["ASSETS"], nome)
    try:
        img = pygame.image.load(caminho)
        return pygame.transform.scale2x(img) if scale == 2 else img
    except pygame.error:
        print(f"Erro: Não foi possível carregar {caminho}. Verifique a pasta '{CONFIG['ASSETS']}'.")
        sys.exit()

# --- CLASSES DE ENTIDADE ---

class Passaro:
    ROTACAO_MAX = 25
    VEL_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y, imgs):
        self.x, self.y = x, y
        self.imgs = imgs
        self.angulo = 0
        self.velocidade = 0
        self.tempo = 0
        self.altura = y
        self.img_idx = 0
        self.imagem = self.imgs[0]

    def pular(self):
        self.velocidade = CONFIG["FISICA"]["PULO"]
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        # Equação de deslocamento vertical
        deslocamento = CONFIG["FISICA"]["GRAVIDADE"] * (self.tempo**2) + self.velocidade * self.tempo
        
        if deslocamento > CONFIG["FISICA"]["VELOCIDADE_MAX"]:
            deslocamento = CONFIG["FISICA"]["VELOCIDADE_MAX"]
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # Lógica de inclinação (Smooth Rotation)
        if deslocamento < 0 or self.y < self.altura + 50:
            self.angulo = self.ROTACAO_MAX
        else:
            if self.angulo > -90:
                self.angulo -= self.VEL_ROTACAO

    def desenhar(self, tela):
        # Animação simplificada com módulo
        self.img_idx = (pygame.time.get_ticks() // (self.TEMPO_ANIMACAO * 20)) % len(self.imgs)
        self.imagem = self.imgs[self.img_idx]

        if self.angulo <= -80:
            self.imagem = self.imgs[1]

        img_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        centro = self.imagem.get_rect(topleft=(self.x, self.y)).center
        rect = img_rotacionada.get_rect(center=centro)
        tela.blit(img_rotacionada, rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x, img):
        self.x = x
        self.img_base = img
        self.img_topo = pygame.transform.flip(img, False, True)
        self.passou = False
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.img_topo.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.img_topo, (self.x, self.pos_topo))
        tela.blit(self.img_base, (self.x, self.pos_base))

    def colidir(self, passaro):
        p_mask = passaro.get_mask()
        t_mask = pygame.mask.from_surface(self.img_topo)
        b_mask = pygame.mask.from_surface(self.img_base)
        
        dist_t = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        dist_b = (self.x - passaro.x, self.pos_base - round(passaro.y))
        
        return p_mask.overlap(t_mask, dist_t) or p_mask.overlap(b_mask, dist_b)

class Chao:
    VELOCIDADE = 5
    def __init__(self, y, img):
        self.y = y
        self.img = img
        self.largura = img.get_width()
        self.x1, self.x2 = 0, self.largura

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE
        if self.x1 + self.largura < 0: self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0: self.x2 = self.x1 + self.largura

    def desenhar(self, tela):
        tela.blit(self.img, (self.x1, self.y))
        tela.blit(self.img, (self.x2, self.y))

# --- CONTROLADOR DO JOGO (ORQUESTRADOR) ---

class FlappyEngine:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((CONFIG["TELA"]["LARGURA"], CONFIG["TELA"]["ALTURA"]))
        pygame.display.set_caption("Flappy Bird AI - Senior Edition")
        
        # Assets
        self.img_bg = carregar_imagem("bg.png")
        self.img_chao = carregar_imagem("base.png")
        self.img_cano = carregar_imagem("pipe.png")
        self.imgs_passaro = [carregar_imagem(f"bird{i}.png") for i in range(1, 4)]
        self.fonte = pygame.font.SysFont('arial', 30, bold=True)
        
        self.geracao = 0

    def desenhar_layout(self, passaros, canos, chao, pontos, ai_ativa):
        self.tela.blit(self.img_bg, (0, 0))
        for c in canos: c.desenhar(self.tela)
        chao.desenhar(self.tela)
        for p in passaros: p.desenhar(self.tela)
        
        # UI
        txt_pontos = self.fonte.render(f"Score: {pontos}", True, CONFIG["CORES"]["BRANCO"])
        self.tela.blit(txt_pontos, (CONFIG["TELA"]["LARGURA"] - txt_pontos.get_width() - 15, 10))
        
        if ai_ativa:
            txt_gen = self.fonte.render(f"Geração: {self.geracao}", True, CONFIG["CORES"]["BRANCO"])
            txt_vivos = self.fonte.render(f"Vivos: {len(passaros)}", True, CONFIG["CORES"]["BRANCO"])
            self.tela.blit(txt_gen, (15, 10))
            self.tela.blit(txt_vivos, (15, 45))
            
        pygame.display.flip()

    def menu_inicial(self):
        while True:
            self.tela.blit(self.img_bg, (0, 0))
            mouse = pygame.mouse.get_pos()
            
            # Botões simples (Lógica de Retângulo)
            btn_player = pygame.Rect(100, 300, 300, 50)
            btn_ai = pygame.Rect(100, 400, 300, 50)
            
            for btn, txt, color in [(btn_player, "MODO JOGADOR", CONFIG["CORES"]["BOTAO"]), 
                                    (btn_ai, "TREINAR IA", CONFIG["CORES"]["BOTAO"])]:
                c = CONFIG["CORES"]["HOVER"] if btn.collidepoint(mouse) else color
                pygame.draw.rect(self.tela, c, btn, border_radius=8)
                t_surf = self.fonte.render(txt, True, CONFIG["CORES"]["BRANCO"])
                self.tela.blit(t_surf, t_surf.get_rect(center=btn.center))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_player.collidepoint(event.pos): return False
                    if btn_ai.collidepoint(event.pos): return True
            
            pygame.display.update()

    def main(self, genomas=None, config=None):
        self.geracao += 1
        ai_ativa = genomas is not None
        
        redes, lista_genomas, passaros = [], [], []
        
        if ai_ativa:
            for _, genoma in genomas:
                redes.append(neat.nn.FeedForwardNetwork.create(genoma, config))
                genoma.fitness = 0
                lista_genomas.append(genoma)
                passaros.append(Passaro(230, 350, self.imgs_passaro))
        else:
            passaros = [Passaro(230, 350, self.imgs_passaro)]

        chao = Chao(730, self.img_chao)
        canos = [Cano(700, self.img_cano)]
        pontos = 0
        relogio = pygame.time.Clock()
        
        rodando = True
        while rodando and len(passaros) > 0:
            relogio.tick(30)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if not ai_ativa and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE: passaros[0].pular()

            # Qual cano olhar?
            idx_cano = 0
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].img_topo.get_width()):
                idx_cano = 1

            # Movimentação e IA
            for i, p in enumerate(passaros):
                p.mover()
                if ai_ativa:
                    lista_genomas[i].fitness += 0.1
                    # Inputs normalizados ajudam a IA
                    output = redes[i].activate((p.y, 
                                               abs(p.y - canos[idx_cano].altura), 
                                               abs(p.y - canos[idx_cano].pos_base)))
                    if output[0] > 0.5: p.pular()

            chao.mover()
            
            # Lógica de Canos e Colisão
            add_cano = False
            remover_canos = []
            for cano in canos:
                for i, p in enumerate(passaros):
                    if cano.colidir(p) or p.y + p.imagem.get_height() > chao.y or p.y < 0:
                        passaros.pop(i)
                        if ai_ativa:
                            lista_genomas[i].fitness -= 1
                            lista_genomas.pop(i)
                            redes.pop(i)
                    
                    if not cano.passou and p.x > cano.x:
                        cano.passou = True
                        add_cano = True
                
                cano.mover()
                if cano.x + cano.img_topo.get_width() < 0: remover_canos.append(cano)

            if add_cano:
                pontos += 1
                canos.append(Cano(600, self.img_cano))
                if ai_ativa:
                    for g in lista_genomas: g.fitness += 5
            
            for r in remover_canos: canos.remove(r)
            self.desenhar_layout(passaros, canos, chao, pontos, ai_ativa)

    def treinar_ai(self):
        caminho_config = os.path.join(os.path.dirname(__file__), 'config.txt')
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    caminho_config)
        populacao = neat.Population(config)
        populacao.add_reporter(neat.StdOutReporter(True))
        populacao.run(self.main, 50)

if __name__ == '__main__':
    engine = FlappyEngine()
    if engine.menu_inicial():
        engine.treinar_ai()
    else:
        engine.main()