import pygame
import os
import json

# Abrir arquivp com as configs
config_f = open("./config.json")
config = json.load(config_f)

# Abrir o diretorio com o sprite do personagem
diretorio_principal = os.path.dirname(__file__)
diretorio_sprites = os.path.join(diretorio_principal, "assets", "sprites")
sprite_sheet = pygame.image.load(os.path.join(diretorio_sprites, "Personagem.png"))

pygame.init()

# Configurando o personagem principal
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []

        # Identificando as sprites na imagem
        for i in range(13):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            self.sprites.append(img)

        # Para usar na animacao de correr
        self.atual, self.pular_call_se_impar = 0, 0
        self.sequencia_correr = [6, 4, 5, 5, 4, 6, 7, 8, 8, 7, 6]
        self.correr_anim_indx = 0

        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (32 * 5, 32 * 5))

        # Definindo a posição inicial do personagem
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [200, 500]


        self.correr = self.pular = self.reverse = self.descer = self.mira = self.tiro = False
        self.forca_y = 0


    def pulo(self): # Função chamada quando apertamos "W" ou "Up"
        self.pular = True
        if self.rect.y == config["Chao"]:
            self.forca_y = config["Forca_pulo"]
        self.reset_correr_idx()

    def andar(self): # Função chamada quando apertamos "A", "D", "Left" ou "Right"
        self.correr = True

    def reset_correr_idx(self):
        self.correr_anim_indx= 0

    def mirar(self, true_or_false=True): # Função Chamada quando clicamos o botão direito do Mouse
        self.mira = true_or_false

    def atirar(self): # Função Chamada quando clicamos o botão esquerdo do Mouse
        self.tiro = True

    def pos(self):
        return self.rect.center

    def update(self): 
        # Configurando o pulo:
        if self.pular:
            if self.forca_y < 0: 
                self.descer = True

            if self.descer:    
                self.atual = 10
            else:
                self.atual = 9
            desolocamento = -self.forca_y
            self.forca_y -= config["Gravidade"]
            self.rect.y += desolocamento
    
        # Personagem parado e respirando (alternando entre as sprites 0, 1, 2 e 3. O primeiro sprite é mais demorado)
        elif not self.correr:
            if int(self.atual) == 0: # Se o sprite for 0, ele vai demorar mais pra alternar
                self.atual += 0.03
            else:
                self.atual += 0.2
            if self.atual >= 4: # A posição 4 é quando começa a correr. Então voltamos ao inicio
                self.atual = 0
            self.reset_correr_idx()

        elif self.correr and self.pular_call_se_impar % 2 == 0:
            if self.correr_anim_indx >= len(self.sequencia_correr):
                self.reset_correr_idx()
            self.atual = self.sequencia_correr[self.correr_anim_indx]
            self.correr_anim_indx += 1

        self.pular_call_se_impar += 1
        
        if self.rect.y == config["Chao"]: # Se o personagem estiver em colisão com o chão, ele não pode pular
            self.pular = self.descer = False
        self.correr = False

         # Definindo a colisão com o chão
        if self.rect.y >= config["Chao"]:
            self.rect.y = config["Chao"]
            self.forca_y = 0

        # Configurando a mira
        if self.mira:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x < self.rect.centerx:
                self.atual = 12
            else:
                self.atual = 11

        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image, (32 * 5, 32 * 5))
        self.tiro = False 


personagem = Personagem()


class Arma(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load("assets/sprites/pixel_art_arma.png"))
        self.sprites.append(pygame.image.load("assets/sprites/pixel_art_arma2.png"))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (900 / 7, 306 / 7))
        self.rect = self.image.get_rect()


    def update(self):
        mouse_x = pygame.mouse.get_pos()[0]
        if mouse_x < personagem.rect.centerx:
            self.atual = 1
        else:
            self.atual = 0     
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (900 / 7, 306 / 7))


class Mira(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load("assets/sprites/mira.png"))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
