import pygame
import os
import json

from pygame.locals import *
from sys import exit

from Player import Personagem, Arma, Mira


# Abrir arquivp com as configs
config_f = open("./config.json")
config = json.load(config_f)

# Definindo diretórios com a biblioteca OS
diretorio_principal = os.path.dirname(__file__)
diretorio_sons = os.path.join(diretorio_principal, "assets", "sons")

# Iniciando o pygame e importando a folha de sprites do personagem principal
pygame.init()

# Definindo as configurações da janela
tela = config["Tela"]
largura, altura = tela[0], tela[1]
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Perazzo Contra as Forças rWins")

# Algumas variaveis globais:
rgb_preto = (0, 0, 0)
rgb_vermelho = (255, 0, 0)
rgb_branco = (255, 255, 255)
font = pygame.font.SysFont(None, 20)
click = False

tempo = pygame.time.Clock()

# Função que escreve textos na tela
def draw_text(texto, fonte, cor, tela, x, y):
    text_obj = font.render(texto, 1, cor)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    tela.blit(text_obj, text_rect)


# Função que pega a coordenada do personagem para desenhar a arma:
def atualizar_pos(player_x, player_y):
    posicao_arma = [player_x + 20, player_y + 55]
    return posicao_arma


# Organizando as sprites
todas_as_sprites = pygame.sprite.Group()
sprite_arma = pygame.sprite.Group()
personagem = Personagem()
arma = Arma()
mira = Mira()
todas_as_sprites.add(personagem)
sprite_arma.add(arma)
sprite_arma.add(mira)


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
        tela.fill((20, 120, 120))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            # Programando o ataque (Botão direito do mouse mira, esquerda atira, tipo GTA):
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    personagem.mirar(True)
                if event.button == 1:
                    personagem.atirar()
            if event.type == MOUSEBUTTONUP and event.button == 3:
                personagem.mirar(False)

            # Se Apertar ESC:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
        
        # Se estiver mirando ou atirando, ele fica mais devagar:
        
        # Pular
        if pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_UP]:
            personagem.pulo()

        # Ir para a esquerda:
        if pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_LEFT]:
            personagem.andar()
            personagem.rect.x -= config["Vel_x"]
            
            # Se ele não estiver mirando, a sprite será invertida quando o personagem virar para esquerda
            # Quando ele está mirando, ele tem uma configuração para seguir o x do mouse para virar
            if personagem.mira == personagem.tiro == False:
                personagem.image = pygame.transform.flip(personagem.image, True, False)

        # Ir para a Direita
        if pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_RIGHT]:
            personagem.andar()
            personagem.rect.x += config["Vel_x"]

        # Desenhando o personagem
        todas_as_sprites.draw(tela)
        todas_as_sprites.update()

        # Desenhar arma e a mira:
        pos_arma = atualizar_pos(personagem.rect.x, personagem.rect.y)
        if personagem.tiro or personagem.mira:
            arma.rect = pos_arma
            sprite_arma.draw(tela)
            sprite_arma.update()

        pygame.display.update()
        tempo.tick(40)


main_menu()
