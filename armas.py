import math
import pygame, json
from pygame.locals import *
from Player import Personagem
personagem = Personagem()

# Abrir arquivp com as configs
config_f = open("./config.json")
config = json.load(config_f)

sprite_sheet = pygame.image.load("assets/sprites/pixel_art_arma.png")

pygame.init()

# Configurações para a bazuca de tux
class Bazuca(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = list()
        linhas, colunas = 2, 1
        try:
            for c in range(colunas+1):
                for i in range(linhas-1):
                    img = sprite_sheet.subsurface((i * 128, c * 40), (128, 40))
                    self.sprites.append(img)
        except ValueError:
            print(c, i)

        self.atual = 0
        self.image = self.sprites[self.atual]
        self.rect = self.image.get_rect()

    def update(self):
        if personagem.atual == 17:
            self.atual= 0
        else:
            self.image = pygame.transform.flip(self.image, False, True)


bazuca = Bazuca()


# Criando as munições (TUX):
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/sprites/tux_bullet.png")
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
        self.image = pygame.transform.rotate(self.image, angle)
        self.angle = math.radians(angle)


    def update(self):
        self.rect.x += 30 * math.cos(self.angle)
        self.rect.y += 30 * math.sin(self.angle) * -1

        if self.rect.x <=0 or self.rect.x >= config["Tela"][0] or self.rect.y <= 0 or self.rect.y  >= config["Tela"][1]:
            self.kill()


def pos():
    return (Bullet.update())
        
        
