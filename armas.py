import pygame, json
from pygame.locals import *
from Player import Personagem
personagem = Personagem()

# Abrir arquivp com as configs
config_f = open("./config.json")
config = json.load(config_f)

pygame.init()

# Configurações para a bazuca de tux
class Bazuca(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        bazuca_direita = pygame.image.load("assets/sprites/pixel_art_arma.png")
        self.atual = 0
        self.image = bazuca_direita
        self.rect = self.image.get_rect()

    def update(self):
        if personagem.atual == 17:
            self.atual=0
        else:
            self.image = pygame.transform.flip(self.image, False, True)

