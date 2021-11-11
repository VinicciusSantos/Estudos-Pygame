import pygame, json, math

from random import randint
from pygame.locals import *
from sys import exit

from Player import Personagem
from armas import *


# Abrir arquivp com as configs
config_f = open("./config.json")
config = json.load(config_f)

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

tempo = pygame.time.Clock()
particles = []

# Função que escreve textos na tela
def draw_text(texto, fonte, cor, tela, x, y):
    text_obj = font.render(texto, 1, cor)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    tela.blit(text_obj, text_rect)

# Organizando as sprites
todas_as_sprites = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
personagem = Personagem()
bazuca = Bazuca()
mira = Mira()
todas_as_sprites.add(personagem)

angle = 0

# Menu Principal
def main_menu():
    while True:
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1: # Se clicar com o botão direitodo mouse
                click = True

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

        pygame.display.update()
        tempo.tick(30)


# Iniciando o Jogo, a função é chamada dentro da função main_menu() 
def game():
    cool_down = 0
    running = True
    atirar = False
    while running:
        tela.fill((20, 120, 120))

        # Nas particulas temos: [[posição_x, posição_y], [velocidade], [tempo]]
        # A velocidade e o tempo são dados pelo randint, que faz as partículas ficarem mais animadas e variadas.
        def particulas(pos_x, pos_y):
            particles.append([[pos_x, pos_y], [randint(0,20) / 10 - 1, -2], randint(4, 6)])
        for particle in particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.5
            particle[1][1] += 0.01 # Gravidade
            pygame.draw.circle(tela, (rgb_branco), particle[0], int(particle[2]))
            if particle[2] <=0:
                particles.remove(particle)
                
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    atirar = True
                if event.button == 3:
                    personagem.mirar(True)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    atirar = False
                if event.button == 3:
                    personagem.mirar(False)
            # Se Apertar ESC:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
        

        # Configurando o cooldown, criando a arma e o recoil
        if atirar == True and personagem.mira and cool_down <= 0:
            cool_down = 15
            bullet_group.add(create_bullet())
            personagem.recoil(angle)   

        vel_x = 23
        if personagem.mira:
            vel_x = 3
        
        # Pular
        if pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_UP]:
            personagem.pulo()

        # Ir para a esquerda:
        if pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_LEFT]:
            personagem.andar_e()
            if personagem.nochao:
                particulas(personagem.rect.bottomright[0], personagem.rect.bottomright[1] + 64)
            personagem.rect.x -= vel_x

        # Ir para a Direita
        if pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_RIGHT]:
            personagem.andar_d()
            if personagem.nochao:
                particulas(personagem.rect.bottomleft[0]+60, personagem.rect.bottomleft[1] + 64)
            personagem.rect.x += vel_x
            
        # Desenhando o personagem
        todas_as_sprites.draw(tela)
        todas_as_sprites.update()

        # Configurando as coisas que acontecem quando o personagem está mirando ou atirando
        if personagem.mira:
            # Se a arma estiver com cooldown, aparecerá a sprite sem a munição na ponta
            if cool_down > 4:
                bazuca.image = bazuca.sprites[1]
            else:
                bazuca.image = bazuca.sprites[0]

            # Calculando o ângulo de Rotação da Arma:
            gunpos = (personagem.rect.x+57, personagem.rect.y+68)
            position = pygame.mouse.get_pos()
            angle = -math.atan2(position[1] - (gunpos[1]), position[0] - (gunpos[0]))*57.29
            radius = math.sqrt(60**2 + 68**2)
            bala_pos = (gunpos[0] + radius*(math.cos(math.radians(angle*-1))), 
            gunpos[1] + radius*math.sin(math.radians(angle*-1)))

            # Rotação da Arma conforme a direção que o personagem está indo
            gunrot = pygame.transform.rotate(bazuca.image, angle)
            if personagem.atual == 17:
                gunrot = pygame.transform.rotate(bazuca.image, -angle)
            gunpos1 = (gunpos[0]-gunrot.get_rect().width/2, gunpos[1]-gunrot.get_rect().height/2)
            if personagem.atual == 17:
                gunrot = pygame.transform.flip(gunrot, False, True)

            # Criando a bala:
            cool_down -= 1
            def create_bullet():
                particulas(bala_pos[0], bala_pos[1])
                return Bullet(bala_pos[0], bala_pos[1], angle)  
                
            # desenhando a arma e a mira
            tela.blit(gunrot, gunpos1)
            tela.blit(mira.image, (position[0]-20, position[1]-20))

        bullet_group.draw(tela)
        bullet_group.update()
        pygame.display.update()
        tempo.tick(40)


main_menu()
