import pygame
import os

from pygame.locals import *
from sys import exit


diretorio_principal = os.path.dirname(__file__)
diretorio_sprites = os.path.join(diretorio_principal, "assets", "sprites")
diretorio_sons = os.path.join(diretorio_principal, "assets", "sons")

# Iniciando o pygame e importando a folha de sprites do personagem principal
pygame.init()
sprite_sheet = pygame.image.load(os.path.join(diretorio_sprites, "Personagem.png"))


rgb_preto = (0, 0, 0)

# Definindo as configurações da janela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Perazzo Contra as Forças rWins")

# Criando a gravidade:
aceleracao_x = aceleracao_y = 0
tempo = pygame.time.Clock()
G = 40


# Configurando o personagem principal
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []

        # Identificando as sprites na imagem
        for i in range(11):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            self.sprites.append(img)

        self.atual, self.indice = 0, 3
        self.image = self.sprites[self.atual]

        # Definindo a posição inicial do personagem
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [200, 500]
        self.image = pygame.transform.scale(self.image, (32 * 5, 32 * 5))

        self.correr = False
        self.pular = False
        self.reverse = False


    def pulo(self): # Função chamada quando apertamos "W" ou "Up"
        self.pular = True

    def andar(self): # Função chamada quando apertamos "A", "D", "Left" ou "Right"
        self.correr = True

    def update(self): 
        # Configurando o pulo:
        if self.pular:
            if self.rect.y == chao - 150: # Quando chegar em 150 pixels acima do chão (altura máxima) a animação é a de descer
                self.descer = True
            if self.descer == True:    
                self.atual = 10
            else:
                self.atual = 9

        # Personagem parado e respirando (alternando entre as sprites 0, 1, 2 e 3. O primeiro sprite é mais demorado )
        elif self.correr == False and self.pular == False:
            if int(self.atual) == 0: # Se o sprite for 0, ele vai demorar mais pra alternar
                self.atual += 0.05 
            else:
                self.atual += 0.3
            if self.atual >= 4: # A posição 4 é quando começa a correr. Então voltamos ao inicio
                self.atual = 0

        elif self.correr and self.indice % 2 == 0:
            self.atual = self.reverse and self.atual - 1 or self.atual + 1

            # se o index da animacao for maior ou igual a 8, reverter a animacao
            # se for menor que 4, ir no fluxo normal,
            # se nao for nenhum dos dois, nao mudar, continuar sendo True ou False
            self.reverse = self.atual >= 8 or (False if self.atual <= 4 else self.reverse)

        self.indice += 1
        #if self.atual != 0:
            #print(self.atual)
        self.image = self.sprites[int(self.atual)]
        
        if self.rect.y == chao:
            self.pular = self.descer = False
        self.correr = False
        self.image = pygame.transform.scale(self.image, (32 * 5, 32 * 5))


# Organizando as sprites
todas_as_sprites = pygame.sprite.Group()
personagem = Personagem()
todas_as_sprites.add(personagem)

# Iniciando o Jogo
while True:
    tela.fill(rgb_preto)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    vel = 20

    # Pular
    if pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_UP]:
        personagem.pulo()
        if personagem.rect.y == chao:
            aceleracao_y = -20

    # Ir para a esquerda:
    if pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_LEFT]:
        personagem.andar()
        personagem.rect.x -= vel
        personagem.image = pygame.transform.flip(personagem.image, True, False)

    # Ir para a Direita
    if pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_RIGHT]:
        personagem.andar()
        personagem.rect.x += vel

    # Aplicando a gravidade
    T = tempo.get_time() / 1000
    F = G * T
    aceleracao_y += F
    personagem.rect.y += aceleracao_y

    # Definindo a colisão com o chão
    chao = 400
    if personagem.rect.y >= chao:
        personagem.rect.y = chao

    # Desenhando o personagem e Atualizando a tela
    todas_as_sprites.draw(tela)
    todas_as_sprites.update()
    pygame.display.update()
    tempo.tick(30)
