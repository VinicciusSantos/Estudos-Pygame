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


# Configurando o personagem principal
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []

        # Identificando as sprites na imagem
        for i in range(11):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            self.sprites.append(img)


        # Para usar na animacao de correr
        self.atual, self.pular_call_se_impar = 0, 0
        self.sequencia_correr = [4, 5, 4, 6, 7, 8, 7, 6]
        self.correr_anim_indx = 0

        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (32 * 5, 32 * 5))

        # Definindo a posição inicial do personagem
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [200, 500]


        self.correr = self.pular = self.reverse = self.descer= False
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
        elif  not self.correr:
            if int(self.atual) == 0: # Se o sprite for 0, ele vai demorar mais pra alternar
                self.atual += 0.05 
            else:
                self.atual += 0.3
            if self.atual >= 4: # A posição 4 é quando começa a correr. Então voltamos ao inicio
                self.atual = 0
            self.reset_correr_idx()

        elif self.correr and self.pular_call_se_impar % 2 == 0:

            if self.correr_anim_indx >= len(self.sequencia_correr):
                self.reset_correr_idx()
            self.atual = self.sequencia_correr[self.correr_anim_indx]
            self.correr_anim_indx += 1

        self.pular_call_se_impar += 1

        self.image = self.sprites[int(self.atual)]
        
        if self.rect.y == config["Chao"]: # Se o personagem estiver em colisão com o chão, ele não pode pular
            self.pular = self.descer = False
        self.correr = False
        self.image = pygame.transform.scale(self.image, (32 * 5, 32 * 5))

         # Definindo a colisão com o chão
        if self.rect.y >= config["Chao"]:
            self.rect.y = config["Chao"]
            self.forca_y = 0