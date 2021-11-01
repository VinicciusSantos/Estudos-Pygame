import pygame
import os
import json

from pygame.locals import *
from sys import exit

from Player2 import Personagem


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
        tela.fill((20, 120, 120))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            # Se Apertar ESC:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        vel_x = 23
        # Pular
        if pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_UP]:
            personagem.pulo()

        # Ir para a esquerda:
        if pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_LEFT]:
            personagem.andar_e()
            personagem.rect.x -= vel_x

        # Ir para a Direita
        if pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_RIGHT]:
            personagem.andar_d()
            personagem.rect.x += vel_x

        # Desenhando o personagem
        todas_as_sprites.draw(tela)
        todas_as_sprites.update()

        # Desenhar arma e a mira:
        pos_arma = atualizar_pos(personagem.rect.x, personagem.rect.y)
        pygame.display.update()
        tempo.tick(40)


main_menu()
