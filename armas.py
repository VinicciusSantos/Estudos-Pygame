import pygame, json
from pygame.locals import *

# Abrir arquivp com as configs
config_f = open("./config.json")
config = json.load(config_f)

pygame.init()

# Configurações para a bazuca de tux
class Bazuca(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        bazuca_direita = pygame.image.load("assets/sprites/pixel_art_arma.png")
        bazuca_esquerda = pygame.image.load("assets/sprites/pixel_art_arma.png")
        self.sprites = [bazuca_direita, bazuca_esquerda]
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.rect = self.image.get_rect()

    def update(self):
        self.atual = 0
        self.imagem = self.sprites[self.atual]


