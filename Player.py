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
        linhas, colunas, cont = 5, 4, 0
        for c in range(colunas):
            for i in range(linhas-1):
                cont += 1
                img = sprite_sheet.subsurface((i * 32, c * 32), (32, 32))
                self.sprites.append(img)

        self.atual, self.pular_call_se_impar = 0, 0
        self.sequencia_correr_d = [6, 4, 5, 5, 4, 6, 7, 8, 8, 7, 6]
        self.sequencia_correr_e = [11, 9, 10, 10, 9, 11, 12, 13, 13, 12, 11]
        self.sequencia_respirar = [0, 0, 0, 0, 0, 0, 1, 2, 3]
        self.correr_anim_indx = self.resp_indx = 0

        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (32 * 5, 32 * 5))

        # Definindo a posição inicial do personagem
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [200, 500]


        self.correr_d = self.correr_e = self.pular = self.reverse = self.descer = self.mira = self.tiro = False
        self.forca_y = 0

    def pos(self):
        return self.image.get_rect()

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

    def update(self): 
        # Configurando o pulo:
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

         # Definindo a colisão com o chão
        if self.rect.y >= config["Chao"]:
            self.rect.y = config["Chao"]
            self.forca_y = 0
        elif self.descer:    
            self.atual = 15
        else:
            self.atual = 14

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