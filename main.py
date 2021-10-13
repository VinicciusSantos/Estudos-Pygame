import pygame
from pygame.locals import *
from sys import exit
import os

# definindo diretórios
diretorio_principal = os.path.dirname(__file__)
diretorio_sprites = os.path.join(diretorio_principal, "sprites")
diretorio_sons = os.path.join(diretorio_principal, "sons")

pygame.init()
sprite_sheet = pygame.image.load(os.path.join(diretorio_sprites, "Personagem.png"))

# Definindo Cores
rgb_preto = (0, 0, 0)

# Definindo as configurações da janela
largura, altura = 1280, 720
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Perazzo Contra as Forças rWins")

# Criando a gravidade:
aceleracao_x = aceleracao_y = 0
tempo = pygame.time.Clock()
G = 40


class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = list()
        for i in range(7):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            self.sprites.append(img)

        self.atual, self.indice = 0, 3
        self.image = self.sprites[self.atual]

        self.rect = self.image.get_rect()
        self.rect.bottomleft = [200, 500]
        self.image = pygame.transform.scale(self.image, (32 * 5, 32 * 5))

        self.correr = False
        self.pular = False

    def pulo(self):
        self.pular = True

    def andar(self):
        self.correr = True

    def update(self):
        if self.correr:
            if self.indice == 3 or self.indice == 6:
                self.atual = 2
            if self.indice == 4 or self.indice == 5:
                self.atual = 3
            if self.indice == 7 or self.indice == 12:
                self.atual = 4
            if self.indice == 8 or self.indice == 11:
                self.atual = 5
            if self.indice == 9 or self.indice == 10:
                self.atual = 6
            self.indice += 0.5
            self.correr = False
        else:
            personagem.atual = 0

        if self.indice > 12:
            self.indice = 3

        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (32 * 5, 32 * 5))


# Organizando as sprites
todas_as_sprites = pygame.sprite.Group()
personagem = Personagem()
todas_as_sprites.add(personagem)

while True:
    tela.fill(rgb_preto)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        # Pular
        if event.type == KEYDOWN:
            if event.key == K_w or event.key == K_SPACE or event.key == K_UP:
                aceleracao_y = -20

    vel = 20
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
    if personagem.rect.y >= 500:
        personagem.rect.y = 500

    # Desenhando o personagem
    todas_as_sprites.draw(tela)
    todas_as_sprites.update()

    # Atualizando a tela
    pygame.display.update()
    tempo.tick(30)
