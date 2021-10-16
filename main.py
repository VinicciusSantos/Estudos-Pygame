import pygame
import os
from pygame.locals import *
from sys import exit

# Definindo diretórios com a biblioteca OS
diretorio_principal = os.path.dirname(__file__)
diretorio_sprites = os.path.join(diretorio_principal, "assets", "sprites")
diretorio_sons = os.path.join(diretorio_principal, "assets", "sons")

# Iniciando o pygame e importando a folha de sprites do personagem principal
pygame.init()
sprite_sheet = pygame.image.load(os.path.join(diretorio_sprites, "Personagem.png"))

# Definindo as configurações da janela
largura, altura = 854, 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Perazzo Contra as Forças rWins")

# Algumas variaveis globais:
rgb_preto = (0, 0, 0)
rgb_vermelho = (255, 0, 0)
rgb_branco = (255, 255, 255)
font = pygame.font.SysFont(None, 20)
click = False
chao = altura * 2 / 3

# Criando a gravidade:
aceleracao_x = aceleracao_y = 0
tempo = pygame.time.Clock()
G = 10

# Função que escreve textos na tela
def draw_text(texto, fonte, cor, tela, x, y):
    text_obj = font.render(texto, 1, cor)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    tela.blit(text_obj, text_rect)


# Configurando o personagem principal
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []

        # Identificando as sprites na imagem
        for i in range(11):
            img = sprite_sheet.subsurface((i * 32, 0), (32, 32))
            self.sprites.append(img)

        self.atual, self.pular_call_se_impar = 0, 3
        self.image = self.sprites[self.atual]


        self.sequencia_correr = [4, 5, 4, 6, 7, 8, 7, 6]
        self.correr_anim_indx = 0

        # Definindo a posição inicial do personagem
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [200, 500]
        self.image = pygame.transform.scale(self.image, (32 * 5, 32 * 5))

        self.correr = self.pular = self.reverse = False
        self.forca_y = 0


    def pulo(self): # Função chamada quando apertamos "W" ou "Up"
        self.pular = True
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
            if self.descer == True:    
                self.atual = 10
            else:
                self.atual = 9
    
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
        
        if self.rect.y == chao: # Se o personagem estiver em colisão com o chão, ele não pode pular
            self.pular = self.descer = False
        self.correr = False
        self.image = pygame.transform.scale(self.image, (32 * 5, 32 * 5))


# Organizando as sprites
todas_as_sprites = pygame.sprite.Group()
personagem = Personagem()
todas_as_sprites.add(personagem)


# Menu Principal
def main_menu():
    while True:
        tela.fill(rgb_preto)
        draw_text("Menu Principal", font, rgb_vermelho, tela, 20, 20)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Botão de Iniciar
        button_start = pygame.Rect(largura/3, altura*3/5, largura/3, altura/9)
        if button_start.collidepoint((mouse_x, mouse_y)):
            if click:
                game()

        # Botão de quitar:
        button_quit = pygame.Rect(largura/3, altura*271/360, largura/3, altura/9)
        if button_quit.collidepoint((mouse_x, mouse_y)):
            if click:
                pygame.quit()
                exit()
        
        pygame.draw.rect(tela, rgb_vermelho, button_start)
        pygame.draw.rect(tela, rgb_vermelho, button_quit)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1: # Se clicar com o botão direitodo mouse
                click = True
        pygame.display.update()
        tempo.tick(30)


# Iniciando o Jogo, a função é chamada dentro da função main_menu() 
def game():
    running = True
    while running:
        tela.fill(rgb_preto)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        vel = 20

        # Pular
        if pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_UP]:
            personagem.pulo()
            if personagem.rect.y == chao:
                personagem.forca_y = 150

        # Ir para a esquerda:
        if pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_LEFT]:
            personagem.andar()
            personagem.rect.x -= vel
            personagem.image = pygame.transform.flip(personagem.image, True, False)

        # Ir para a Direita
        if pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_RIGHT]:
            personagem.andar()
            personagem.rect.x += vel

        # Se o personagem estiver pulando, descolar sua posição no eixo y de acordo
        if personagem.pular:
            desolocamento = (-personagem.forca_y)/10 
            personagem.forca_y -= G
            personagem.rect.y += desolocamento

        # Definindo a colisão com o chão
        if personagem.rect.y >= chao:
            personagem.rect.y = chao
            personagem.forca_y = 0

        # Desenhando o personagem e Atualizando a tela
        todas_as_sprites.draw(tela)
        todas_as_sprites.update()
        pygame.display.update()
        tempo.tick(30)


main_menu()
