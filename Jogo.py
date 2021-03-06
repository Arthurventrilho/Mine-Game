import pygame
import random
import time
from os import path
from pygame.locals import *


#baseado em Kids Can Code
img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")
 
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
pink = (255,105,180)
brown = (139,69,19)
yellow = (200, 200, 0)

bright_yellow = (255, 255, 0)
bright_red = (255,0,0)
bright_green = (0, 255, 0)
block_color = (53,115,255)

#Momentos do Jogo 
ESTADO_CAPA = 0
ESTADO_INSTRUCAO = 1
ESTADO_COMANDO = 2
ESTADO_PREPARO = 3
ESTADO_JOGO = 4
ESTADO_TERMINA = 5
ESTADO_GAME_OVER = 6
ESTADO_SUCESSO = 7
ESTADO_CONTROLE = 8 
ESTADO_PAUSA = 9

#TIPOS DE BLOCO
TERRA = 0
DINAMITE_VISIVEL = 1
DINAMITE_INVISIVEL = 2
BANDEIRA = 3
GRANITO = 4
VIDA =5

#PARAMS DO MINERADOR
DANO = 1
SAUDE = 5
VELOCIDADE = 2

#tamnho da tile
TAMANHO_BLOCOS = 40
#numero de linhas
N_LINHAS = 18
#numero de colunas
N_COLUNAS = 35
#
LARGURA_T = TAMANHO_BLOCOS * N_COLUNAS
#
ALTURA_T = TAMANHO_BLOCOS * N_LINHAS

FPS = 30


class Tela():   
    def __init__(self, tamanhoBloco, linhas, colunas, largura, altura):
        self.tbloco = tamanhoBloco
        self.colunas = colunas
        self.linhas = linhas
        self.alturam = self.tbloco * self.linhas
        self.larguram = self.tbloco * self.colunas
        self.alturat = altura
        self.largurat = largura
        self.display = pygame.display.set_mode((self.largurat, self.alturat))
        pygame.display.set_caption('Campo Minado')

        
    def criando(self):
        all_sprites = pygame.sprite.Group()
        posJogador = random.randrange(4, self.linhas-2)
        posBandeira = random.randrange(4, self.linhas-2)
        # Cria minerador e adiciona em um grupo de Sprites.
        minerador = Minerador( 1 * 40, posJogador * 40 )
        minerador_group = pygame.sprite.Group()
        minerador_group.add(minerador)
        all_sprites.add(minerador)
        blocos = pygame.sprite.Group()
        explosoes = pygame.sprite.Group()
        for linha in range(self.linhas):
        
            for coluna in range(self.colunas):
                tipo = - 1
                if linha == 0 or linha == (self.linhas-1):
                    tipo = Bloco.GRANITO
                elif coluna == 0 or coluna == (self.colunas-1):
                    tipo = Bloco.GRANITO
                elif coluna == 1 and linha == posJogador:
                    tipo = -1
                elif coluna == self.colunas-2 and linha == posBandeira:
                    tipo = Bloco.BANDEIRA
                else:
                    chance = random.randrange(0, 1000)
                    if chance >= 0 and chance <=499:
                        tipo = Bloco.TERRA
                    elif chance >= 500 and chance <=849:
                        tipo = Bloco.DINAMITE_VISIVEL
                    elif chance >= 850 and chance <=959:
                        tipo = Bloco.GRANITO
                    elif chance >= 960 and chance <=989:
                        tipo = Bloco.VIDA
                    else:
                        tipo = Bloco.DINAMITE_INVISIVEL
        
                if tipo != -1:    
                    # Calcula a posição.
                    pos_x = coluna * self.tbloco
                    pos_y = linha * self.tbloco
                    
                    # Cria o bloco e adiciona no mapa e no grupo.
                    novo_bloco = Bloco(tipo, pos_x, pos_y)
                    all_sprites.add(novo_bloco)
                    blocos.add(novo_bloco)
                    
        self.minerador = minerador
        self.all =  all_sprites
        self.blocos = blocos
        self.explosoes = explosoes




pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()     
tela = Tela(TAMANHO_BLOCOS, N_LINHAS, N_COLUNAS, LARGURA_T, ALTURA_T)



font_name = pygame.font.match_font("arial")
#fonte canal do youtube Kids Can Code 
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
    
#http://usingpython.com/pygame/ 
def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(tela.display, color, [thingx, thingy, thingw, thingh])
 

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def text_objects1(text, font):
    textSurface1 = font.render(text, True, pink)
    return textSurface1, textSurface1.get_rect()
 
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((tela.largurat/2),(tela.alturat/2))
    tela.display.blit(TextSurf, TextRect)
 
    pygame.display.update()
 
    time.sleep(2)
 
    
    
# http://usingpython.com/pygame/
def button(msg, x, y, w, h, ic, ac):
    mouse = pygame.mouse.get_pos() 

    inside = False
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        inside = True
    
    if inside:
        pygame.draw.rect(tela.display, ac,(x,y,w,h))
    else:
        pygame.draw.rect(tela.display, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    tela.display.blit(textSurf, textRect)
    
    click = pygame.mouse.get_pressed()
    if inside and click[0] == 1:
        return True
    else:
        return False
        
def game_intro():
    
    capa = pygame.image.load(path.join(img_dir, "capa.png")).convert()
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        tela.display.blit(capa, (0,0))

        largeText = pygame.font.Font('freesansbold.ttf',105)
        TextSurf, TextRect = text_objects1("CAMPO MINADO", largeText)
        TextRect.center = ((tela.largurat/2),(tela.alturat/3))
        tela.display.blit(TextSurf, TextRect)
        
        button("JOGAR", 150,450,100,50, green, bright_green,"play")
        button("SAIR", 550,450,100,50, red, bright_red,"quit")
            
        pygame.display.update()
        clock.tick(15)

    
def instrucao():

    gameExit = False
 
    while not gameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 

        tela.display.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("Sobre o jogo:", largeText)
        TextRect.center = ((tela.largurat/2),(tela.alturat/5))
        tela.display.blit(TextSurf, TextRect)
        largeText = pygame.font.Font('freesansbold.ttf',20)
        TextSurf1, TextRect = text_objects("Mine game consite em um jogo onde o objetivo é parmenecer", largeText)
        TextRect.center = ((tela.largurat/2),(tela.alturat/2.4))
        tela.display.blit(TextSurf1, TextRect)
        TextSurf2, TextRect = text_objects("vivo pelo máximo de tempo possível, mas tome cuidado", largeText)
        TextRect.center = ((tela.largurat/2),(tela.alturat/2))
        tela.display.blit(TextSurf2, TextRect)
        TextSurf3, TextRect = text_objects("se sua estamia acabar será GAME OVER", largeText)
        TextRect.center = ((tela.largurat/2),(tela.alturat/1.7))
        tela.display.blit(TextSurf3, TextRect)
        
        button("Jogar", 350,450,100,50, green, bright_green,"Inst")
        
        pygame.display.update()
        clock.tick(60)
        
        
def configuration():

    GameExit = False
 
    while not GameExit:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 

        tela.display.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("Comando:", largeText)
        TextRect.center = ((tela.largurat/2),(tela.alturat/5))
        tela.display.blit(TextSurf, TextRect)
        largeText = pygame.font.Font('freesansbold.ttf',20)
        TextSurf1, TextRect = text_objects("E - pega escada", largeText)
        TextRect.center = ((tela.largurat/2),(tela.alturat/2.4))
        tela.display.blit(TextSurf1, TextRect)
        TextSurf2, TextRect = text_objects("L - entra na loja", largeText)
        TextRect.center = ((tela.largurat/2),(tela.alturat/2))
        tela.display.blit(TextSurf2, TextRect)
        TextSurf3, TextRect = text_objects("S - entrar na casa para dormir", largeText)
        TextRect.center = ((tela.largurat/2),(tela.alturat/1.7))
        tela.display.blit(TextSurf3, TextRect)
        
        button("Jogar", 350,450,100,50, green, bright_green,"bb")
        
        pygame.display.update()
        clock.tick(120)   
        
def game_over():
    
    tela_morreu = pygame.image.load("game_over.png")

    ge = False

    while ge:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        tela.display.blit(tela_morreu, (0,0))

        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects1("GAME OVER", largeText)
        TextRect.center = ((tela.largurat/2),(tela.alturat/3))
        tela.display.blit(TextSurf, TextRect)
        
        button("JOGAR", 150,450,100,50, green, bright_green,"play")
        button("SAIR", 550,450,100,50, red, bright_red,"quit")
            
        pygame.display.update()
        clock.tick(180)

def sucess():
    
    boa = pygame.image.load("sucess.png")

    GE = False

    while GE:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        tela.display.blit(boa, (0,0))

        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects1("PARABÉSN, VOCÊ GANHOU!", largeText)
        TextRect.center = ((tela.largurat/2),(tela.alturat/3))
        tela.display.blit(TextSurf, TextRect)
        
        button("JOGAR", 150,450,100,50, green, bright_green,"play")
        button("SAIR", 550,450,100,50, red, bright_red,"quit")
            
        pygame.display.update()
        clock.tick(15)        


# ===============      CLASSES      =============== 

        
class MineradorParams():
    def __init__(self, direita, esquerda, animacaoD, animacaoE, damage, speed, life):
        self.direita = pygame.image.load(path.join(img_dir, direita)).convert()
        self.direita.set_colorkey(black)
        self.esquerda = pygame.image.load(path.join(img_dir, esquerda)).convert()
        self.esquerda.set_colorkey(black)
        self.animD = pygame.image.load(path.join(img_dir, animacaoD)).convert()
        self.animD.set_colorkey(white)
        self.animE = pygame.image.load(path.join(img_dir, animacaoE)).convert()
        self.animE.set_colorkey(white)
        self.damage = damage
        self.speed = speed
        self.life = life
    

class Minerador(pygame.sprite.Sprite):
    
    params = MineradorParams("mineradorD.png", "mineradorE.png", "animD.png", "animE.png", DANO, VELOCIDADE, SAUDE)
    
    
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = Minerador.params.direita
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.damage = Minerador.params.damage
        self.speed = Minerador.params.speed
        self.life = Minerador.params.life
        self.lastclock = pygame.time.get_ticks()
        self.cooldown = 300
        self.win = False


    def move(self):
        
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.image = Minerador.params.esquerda
            self.velocidadex = -self.speed
            self.velocidadey = 0
        elif pressed_keys[K_RIGHT]:
            self.image = Minerador.params.direita
            self.velocidadex = +self.speed
            self.velocidadey = 0
        elif pressed_keys[K_DOWN]:
            self.image = self.lastimage
            self.velocidadex = 0
            self.velocidadey = +self.speed
        elif pressed_keys[K_UP]:
            self.image = self.lastimage
            self.velocidadex = 0
            self.velocidadey = -self.speed 

        else:
            self.velocidadex = 0
            self.velocidadey = 0
        self.rect.x += self.velocidadex
        self.rect.y += self.velocidadey
        

        

                
    """Baseado em https://github.com/mchr3k/bounce-game/blob/master/bounce.py"""                       
    def colisao_blocos(self, listaSprites, explosoes):
        
        #Se o minerador bate nos blocos 
        for bloco in pygame.sprite.spritecollide(self, listaSprites, False):        
            self.now = pygame.time.get_ticks()
            #se o personagem  estiver se movendo em x
            if (self.velocidadex != 0):
                #se ele estiver indo para a direita
                if (self.velocidadex > 0):
                    self.rect.right = bloco.rect.left
                    
                #se ele estiver indo para a esquerda
                elif (self.velocidadex < 0):
                    self.rect.left = bloco.rect.right
                    
                #ele para de na parede do bloco
                self.velocidadex = 0
                    
                
            #se estiver se movendo em y
            elif (self.velocidadey != 0):
                #se ele estiver indo para baixo
                if (self.velocidadey > 0):
                    self.rect.bottom = bloco.rect.top
                    
                #se ele estiver indo para cima
                elif (self.velocidadey < 0):
                    self.rect.top = bloco.rect.bottom
                
                #ele para de na parede do bloco
                self.velocidadey = 0
                
            self.hit(bloco)
            
        
    
    def hit(self, bloco):
        
        if self.now - self.lastclock >= self.cooldown:
            self.lastclock = self.now
            
            #animacao e som
            self.animacao()
            pica_sound.play()

    
            #blocos de graniso sao indestrutiveis
            if bloco.tipo != GRANITO:    
                bloco.life -= self.damage
            
            #se os blocos forem destruidos
            if bloco.life <=0:
                bloco.kill()
                #TNT
                if bloco.tipo == DINAMITE_VISIVEL:  
                    random.choice(expl_snd).play()
                    expl = Explosion(bloco.rect.center)
                    tela.all.add(expl)
                    tela.explosoes.add(expl)
                    self.life -= 1
                #TNT escondida - morte
                if bloco.tipo == DINAMITE_INVISIVEL:  
                    random.choice(expl_snd).play()
                    expl = Explosion(bloco.rect.center)
                    tela.all.add(expl)
                    tela.explosoes.add(expl)
                    self.life -= 1
                #pega vida
                if bloco.tipo == VIDA:  
                    life_sound.play()
                    self.life += 1
                #ganha
                if bloco.tipo == BANDEIRA:  
                    win_sound.play()
                    self.win = True
                    
    def animacao(self):

        click = self.now
        if self.lastimage == Minerador.params.direita:
            self.image = Minerador.params.animD

                
            
        elif self.lastimage == Minerador.params.esquerda:
            self.image = Minerador.params.animE


    def update(self):
        volta = ESTADO_JOGO
        if tela.minerador.life <= 0:
            volta = ESTADO_GAME_OVER
     
        # Move o minerador pela tela.
        
        
        if self.image == Minerador.params.direita or self.image == Minerador.params.esquerda:
            self.lastimage = self.image
            
        if self.image == Minerador.params.animD or self.image == Minerador.params.animE:
            self.image = self.lastimage
            
        return volta
            
class BlocoParams:
    def __init__(self, image, vida):
        self.image = pygame.image.load(path.join(img_dir, image)).convert()
        self.life = vida

class Bloco(pygame.sprite.Sprite):
    
    TERRA = TERRA
    DINAMITE_VISIVEL = DINAMITE_VISIVEL
    DINAMITE_INVISIVEL = DINAMITE_INVISIVEL
    BANDEIRA = BANDEIRA
    GRANITO = GRANITO
    VIDA = VIDA

    
    tipos = {
        TERRA: BlocoParams("terra.png", 3),
        DINAMITE_VISIVEL: BlocoParams("TNT.png", 1),
        DINAMITE_INVISIVEL: BlocoParams("terra.png", 1),
        BANDEIRA: BlocoParams("bandeira.png", 1),
        GRANITO: BlocoParams("granito.png", 1),
        VIDA: BlocoParams("vida.png", 1)

    }
        
    def __init__(self, tipo, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)

        self.tipo = tipo
        self.image = Bloco.tipos[tipo].image
        self.image.set_colorkey(black)
        self.life = Bloco.tipos[tipo].life
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        
 
#inpirado em canal do youtube Kids Can Code 
class ExplosionParams:
    def __init__(self, img):
        image = pygame.image.load(path.join(img_dir, img)).convert()
        self.image = pygame.transform.scale(image, (50, 50))
        self.image.set_colorkey(black)


class Explosion(pygame.sprite.Sprite):
    
    params = {
            'explo00': ExplosionParams('regularExplosion00.png'),
            'explo01': ExplosionParams('regularExplosion01.png'),
            'explo02': ExplosionParams('regularExplosion02.png'),
            'explo03': ExplosionParams('regularExplosion03.png'),
            'explo04': ExplosionParams('regularExplosion04.png'),
            'explo05': ExplosionParams('regularExplosion05.png'),
            'explo06': ExplosionParams('regularExplosion06.png'),
            'explo07': ExplosionParams('regularExplosion07.png'),
            'explo08': ExplosionParams('regularExplosion08.png'),
            }
    
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.params['explo00'].image
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.params):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.params['explo0{}'.format(self.frame)].image
                self.rect = self.image.get_rect()
                self.rect.center = center
        
 

#som de explosao  - Kids Can Code e https://www.bfxr.net/
expl_snd = []
for snd in ["explosion1.wav", "explosion2.wav", "explosion3.wav"]:
    expl_snd.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
    
for snd in expl_snd:
    snd.set_volume(0.5)
    
#https://www.bfxr.net/    
life_sound = pygame.mixer.Sound(path.join(snd_dir, "life.wav"))
life_sound.set_volume(1)
pica_sound = pygame.mixer.Sound(path.join(snd_dir, "pica.wav"))
pica_sound.set_volume(0.2)
win_sound = pygame.mixer.Sound(path.join(snd_dir, "win.wav"))
win_sound.set_volume(1)

pygame.mixer.music.load(path.join(snd_dir, "musica.wav"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops = -1)


        
ESTADO = ESTADO_CAPA
while ESTADO != ESTADO_TERMINA:
    
    #CAPA
    if ESTADO == ESTADO_CAPA:
    
        capa = pygame.image.load(path.join(img_dir, "capa.png")).convert()
        
        intro = True
    
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
    
            tela.display.blit(capa, (0,0))
    
            largeText = pygame.font.Font('3Dumb.ttf',110)
            TextSurf, TextRect = text_objects1("CAMPO MINADO", largeText,)
            TextRect.center = ((tela.largurat/2),(tela.alturat/3))
            tela.display.blit(TextSurf, TextRect)
            
            clicou_jogar = button("COMEÇAR", 450,450,150,75, green, bright_green)

            clicou_tutorial = button("TUTORIAL", 850,450,150,75, yellow, bright_yellow)

            
            if clicou_jogar:
                intro = False
                ESTADO = ESTADO_PREPARO
                
            if clicou_tutorial:
                intro = False
                ESTADO = ESTADO_INSTRUCAO
                
            pygame.display.update()
            clock.tick(FPS)
   
    #Instruções
    elif ESTADO == ESTADO_INSTRUCAO:
        
        gameExit = False
        configurar_was_pressed = False
        
        while not gameExit:
     
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
    
            tela.display.fill(white)
            largeText = pygame.font.Font('3Dumb.ttf',50)
            TextSurf, TextRect = text_objects("Sobre o jogo:", largeText)
            TextRect.center = ((tela.largurat/2),(tela.alturat/5))
            tela.display.blit(TextSurf, TextRect)
            
            largeText = pygame.font.Font('freesansbold.ttf',20)
            TextSurf1, TextRect = text_objects("CAMPO MINADO é um jogo onde o objetivo é atravesar o mapa", largeText)
            TextRect.center = ((tela.largurat/2),(tela.alturat/2.4))
            tela.display.blit(TextSurf1, TextRect)
            
            TextSurf2, TextRect = text_objects("sem morrer, mas tome cuidado, o caminho ate la é perigoso,  ", largeText)
            TextRect.center = ((tela.largurat/2),(tela.alturat/2))
            tela.display.blit(TextSurf2, TextRect)
            
            TextSurf3, TextRect = text_objects("basta um passo em falso e sera GAME OVER ", largeText)
            TextRect.center = ((tela.largurat/2),(tela.alturat/1.7))
            tela.display.blit(TextSurf3, TextRect)
            
            vai_para_controle = button("PROXIMO", 450,500,150,75, green, bright_green)
            if vai_para_controle:
                gameExit = True
                ESTADO = ESTADO_CONTROLE
            
            pygame.display.update()
            clock.tick(FPS)
            
    elif ESTADO == ESTADO_CONTROLE:
        gamExit = False
        configurar_was_presseds = False
        
        while not gamExit:
     
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
    
            tela.display.fill(white)
            largeText = pygame.font.Font('3Dumb.ttf',50)
            TextSurf, TextRect = text_objects("INFORMAÇÕES:", largeText)
            TextRect.center = ((tela.largurat/2),(tela.alturat/5))
            tela.display.blit(TextSurf, TextRect)
            
            largeText = pygame.font.Font('freesansbold.ttf',20)
            TextSurf1, TextRect = text_objects("OBJETIVO : Pegar a bandeira;", largeText)
            TextRect.center = ((tela.largurat/2),(tela.alturat/2.4))
            tela.display.blit(TextSurf1, TextRect)
            
            TextSurf2, TextRect = text_objects("CONTROLES: Setas direcionais;  ", largeText)
            TextRect.center = ((tela.largurat/2),(tela.alturat/2.1))
            tela.display.blit(TextSurf2, TextRect)
            
            TextSurf3, TextRect = text_objects("PERIGO: TNT visível e invisível'.", largeText)
            TextRect.center = ((tela.largurat/2),(tela.alturat/1.8))
            tela.display.blit(TextSurf3, TextRect)
            
            TextSurf4, TextRect = text_objects("VOLTAR MENU: Botão ESC'.", largeText)
            TextRect.center = ((tela.largurat/2),(tela.alturat/1.6))
            tela.display.blit(TextSurf4, TextRect)
            
            vai_para_configuration = button("PROXIMO", 625,500,150,75, green, bright_green)
            if vai_para_configuration:
                gamExit = True
                ESTADO = ESTADO_COMANDO
            
            pygame.display.update()
            clock.tick(FPS)
        
    
    #Comando
    elif ESTADO == ESTADO_COMANDO:
        GameExit = False
        
        while not GameExit:
     
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
     
            
            fotoComando = pygame.image.load(path.join(img_dir, "fotoComando.png")).convert()
            
            tela.display.blit(fotoComando, (0,0))
            largeText = pygame.font.Font('freesansbold.ttf',80)
            TextSurf, TextRect = text_objects1("TUDO PRONTO!", largeText)
            TextRect.center = ((tela.largurat/2),(tela.alturat/4.5))
            tela.display.blit(TextSurf, TextRect)
            
            largeText = pygame.font.Font('freesansbold.ttf',50)
            TextSurf1, TextRect = text_objects1("QUE A SORTE  ", largeText)
            TextRect.center = ((tela.largurat/2),(tela.alturat/2.2))
            tela.display.blit(TextSurf1, TextRect)
            
            TextSurf2, TextRect = text_objects1("ESTEJA COM VOCE", largeText)
            TextRect.center = ((tela.largurat/2),(tela.alturat/1.8))
            tela.display.blit(TextSurf2, TextRect)
            

            vai_para_jogo = button("JOGAR", 840,500,150,75, green, bright_green)            
            if vai_para_jogo:
                GameExit = True
                print('')
                ESTADO = ESTADO_PREPARO
            
            pygame.display.update()
            clock.tick(FPS)  
            
    elif ESTADO == ESTADO_PREPARO:
        

        
        
        tempo = clock.tick(FPS)
        

        
        fundo = pygame.Surface((tela.largurat, tela.alturat))
        fundo.fill(brown)
        
 

        
        # Criando os blocos de minerio.       
        tela.criando()
        
        ESTADO = ESTADO_JOGO

        
    elif ESTADO == ESTADO_JOGO:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            
                
        chave = pygame.key.get_pressed()
        
        ESTADO = tela.minerador.update()    
        tela.minerador.move()
        tela.explosoes.update()
        
        if chave[K_ESCAPE]:
            ESTADO = ESTADO_CAPA
    
        tela.minerador.colisao_blocos(tela.blocos, tela.explosoes)
        if tela.minerador.win:
            ESTADO = ESTADO_SUCESSO
    
        tela.display.blit(fundo, (0, 0))    
    
        tela.all.draw(tela.display)
        
        draw_text(tela.display, str(tela.minerador.life), 60, tela.largurat/2, 10)
        
        pygame.display.update()

        
    elif ESTADO == ESTADO_TERMINA:
        
        pygame.quit()
        quit()
        
       
    elif ESTADO == ESTADO_GAME_OVER:
        
        tela_morreu = pygame.image.load(path.join(img_dir, "game_over.png")).convert()
    
        ge = False
        
        while not ge:
     
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
    
                tela.display.blit(tela_morreu, (0,0))
        
                largeText = pygame.font.Font('freesansbold.ttf',115)
                TextSurf, TextRect = text_objects1("GAME OVER", largeText)
                TextRect.center = ((tela.largurat/2),(tela.alturat/3))
                tela.display.blit(TextSurf, TextRect)
                
                clicou_jogar_novamente = button("RECOMEÇAR", 450,450,150,75, green, bright_green)
                clicou_desistir = button("SAIR", 850,450,150,75, red, bright_red)
                
                if clicou_jogar_novamente:
                    ge = True
                    ESTADO = ESTADO_PREPARO
                    
                if clicou_desistir:
                    ge = True
                    pygame.quit()
                    quit()
                    
                pygame.display.update()
                clock.tick(FPS)
          
        
    elif ESTADO == ESTADO_SUCESSO:
        
        boa = pygame.image.load(path.join(img_dir, "sucess.png")).convert()
    
        GE = False
        
        while not GE:
     
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
    
                tela.display.blit(boa, (0,0))
        
                largeText = pygame.font.Font('freesansbold.ttf',80)
                TextSurf, TextRect = text_objects1("PARABENS,", largeText)
                TextRect.center = ((tela.largurat/2),(tela.alturat/3))
                tela.display.blit(TextSurf, TextRect)
                
                largeText = pygame.font.Font('freesansbold.ttf',50)
                TextSurf1, TextRect = text_objects1("VOCÊ GANHOU!!", largeText)
                TextRect.center = ((tela.largurat/2),(tela.alturat/2.4))
                tela.display.blit(TextSurf1, TextRect)
                
                clicou_sucesso = button("JOGAR", 450,450,100,50, green, bright_green)
                clicou_quit = button("SAIR", 850,450,100,50, red, bright_red)
                
                if clicou_sucesso:
                    GE = True
                    ESTADO = ESTADO_PREPARO
                    
                if clicou_quit:
                    GE = True
                    pygame.quit()
                    quit()
                    
                pygame.display.update()
                clock.tick(FPS)
  