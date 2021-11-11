import math
import pygame, os, json

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
        linhas, colunas = 5, 4
        try:
            for c in range(colunas+1):
                for i in range(linhas-1):
                    img = sprite_sheet.subsurface((i * 42, c * 42), (42, 42))
                    self.sprites.append(img)
        except ValueError:
            print(c, i)

        self.atual, self.pular_call_se_impar = 0, 0
        self.sequencia_correr_d = [6, 4, 5, 5, 4, 6, 7, 8, 8, 7, 6]
        self.sequencia_correr_e = [11, 9, 10, 10, 9, 11, 12, 13, 13, 12, 11]
        self.sequencia_respirar = [0, 0, 0, 0, 0, 0, 1, 2, 3]
        self.correr_anim_indx = self.resp_indx = 0
        self.image = self.sprites[self.atual]

        # Definindo a posição inicial do personagem
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [200, 500]

        self.correr_d = self.correr_e = self.pular = self.reverse = self.descer = self.mira = self.tiro = self.nochao = False
        self.forca_y = self.forca_x = 0

    def mirar(self, trueorfalse=False):
        self.mira = trueorfalse

    def pulo(self): # Função chamada quando apertamos "W" ou "Up"
        self.pular = True
        if self.rect.y == config["Chao"]:
            self.forca_y = config["Forca_pulo"]
        self.reset_idx()

    def andar_d(self): # Função chamada quando apertamos "A", "D", "Left" ou "Right"
        self.correr_d = True

    def andar_e(self): # Função chamada quando apertamos "A", "D", "Left" ou "Right"
        self.correr_e = True

    def reset_idx(self):
        self.correr_anim_indx = self.resp_indx = 0
    
    def recoil(self, angle):
        cosseno = math.cos(math.radians(angle))
        sinal_invertido_coss = (-cosseno)/abs(cosseno)
        self.forca_x = config["Forca_recoil"] * sinal_invertido_coss

    def update(self): 
        # Configurando o pulo:
        self.nochao = False
        if self.forca_x != 0:
            self.rect.x += self.forca_x
            if self.forca_x > 0:
                self.forca_x -= config["Atrito"]
            else:
                self.forca_x += config["Atrito"]

        if self.pular:
            if self.forca_y < 0: 
                self.descer = True
            if self.descer:    
                self.atual = 15
            else:
                self.atual = 14
            desolocamento = -self.forca_y
            self.forca_y -= config["Gravidade"]
            self.rect.y += desolocamento
    
        # Personagem parado e respirando (alternando entre as sprites 0, 1, 2 e 3. O primeiro sprite é mais demorado)
        if not self.pular:
            if self.resp_indx >= len(self.sequencia_respirar):
                self.reset_idx()
            self.atual = self.sequencia_respirar[int(self.resp_indx)]
            self.resp_indx += 0.2

        if self.correr_d:
            if self.correr_anim_indx >= len(self.sequencia_correr_d):
                self.reset_idx()
            self.atual = self.sequencia_correr_d[int(self.correr_anim_indx)]
            self.correr_anim_indx += 0.7

        elif self.correr_e:
            if self.correr_anim_indx >= len(self.sequencia_correr_e):
                self.reset_idx()
            self.atual = self.sequencia_correr_e[int(self.correr_anim_indx)]
            self.correr_anim_indx += 0.7

        self.pular_call_se_impar += 1
        
        if self.rect.y == config["Chao"]: # Se o personagem estiver em colisão com o chão, ele não pode pular
            self.pular = self.descer = False
        self.correr_d = self.correr_e = False

        # Configurando a mira
        if self.mira:
            mouse_x = pygame.mouse.get_pos()[0]
            if mouse_x > self.rect.center[0]+40:
                self.atual = 16
            else:
                self.atual = 17

        # Definindo a colisão com o chão
        elif self.rect.y >= config["Chao"]:
            self.nochao = True
            self.rect.y = config["Chao"]
            self.forca_y = 0
        elif self.descer:    
            self.atual = 15
        else:
            self.atual = 14

        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image, (42 * 2.8, 42 * 2.8))
