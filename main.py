import pygame, sys
from pygame.locals import *
from random import randint
from debug import *
# Iniciando pygame
pygame.init()

# Janela
WIDTH  = 400
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Foooood Eater")
clock = pygame.time.Clock()

def draw_text(texto,color, surface, x, y):
	font = pygame.font.SysFont(None, 32)
	textobj = font.render(texto, True, color)
	textrect = textobj.get_rect()
	textrect.topleft = (x, y)
	surface.blit(textobj, textrect)

def main():
	# Jogador
	RIGHT     = False
	LEFT      = False
	UP    	  = False
	DOWN  	  = False
	MOVESPEED = 5

	PLAYER_LOCAL = [screen.get_size()[0]/2, screen.get_size()[1]/2]
	tamanho_player = 20
	player_img = pygame.image.load("Imagens/player.png").convert_alpha()
	pontos = 0

	# Comida
	comidas = []
	temporizador_comida_nova = 0
	comida_nova = 40
	tamanho_comida = 20
	food = pygame.image.load("Imagens/food.png")
	for i in range(20):
		comidas.append(pygame.Rect(randint(0, WIDTH - tamanho_comida), randint(0, HEIGHT - tamanho_comida), tamanho_comida, tamanho_comida))
	
	# Sons
	comer = pygame.mixer.Sound("Musica/comer.wav")
	tocar_comer = True


	while True:
		screen.fill((0, 0, 0))
		mouse = pygame.mouse.get_pos()
		# Movimento do jogador
		player_img_stretch = pygame.transform.scale(player_img, (tamanho_player, tamanho_player))
		player_img_stretch = pygame.transform.flip(player_img_stretch, True, False)
		
		player = pygame.Rect(PLAYER_LOCAL[0], PLAYER_LOCAL[1], tamanho_player, tamanho_player)
		if LEFT == True:
			RIGHT = False
			PLAYER_LOCAL[0] -= MOVESPEED
			player_img_stretch = pygame.transform.rotate(player_img_stretch, 90)
		if RIGHT == True:
			LEFT = False
			PLAYER_LOCAL[0] += MOVESPEED
			player_img_stretch = pygame.transform.rotate(player_img_stretch, 270)
		if UP == True:
			DOWN = False
			PLAYER_LOCAL[1] -= MOVESPEED
			player_img_stretch = pygame.transform.rotate(player_img_stretch, 0)
		if DOWN == True:
			UP = False
			PLAYER_LOCAL[1] += MOVESPEED
			player_img_stretch = pygame.transform.rotate(player_img_stretch, 180)

		# Checagem de colisão com a borda da tela
		if player.top <= 0:
			if UP == True:
				UP = False
				PLAYER_LOCAL[1] = 0
		if player.bottom >= HEIGHT:
			if DOWN == True:
				DOWN = False
				PLAYER_LOCAL[1] = HEIGHT - tamanho_player
		if player.left <= 0:
			if LEFT == True:
				LEFT = False
				PLAYER_LOCAL[0] = 0
		if player.right >= WIDTH:
			if RIGHT == True:
				RIGHT = False
				PLAYER_LOCAL[0] = WIDTH - tamanho_player

		if tamanho_player >= WIDTH and tamanho_player >= HEIGHT:
			tamanho_player = 400

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			# Caso o usuario aperte a tecla o player vai na direção desejada
			if event.type == KEYDOWN:
				if event.key == K_LEFT or event.key == K_a:
					LEFT = True
				if event.key == K_RIGHT or event.key == K_d:
					RIGHT = True
				if event.key == K_UP or event.key == K_w:
					UP = True
				if event.key == K_DOWN or event.key == K_s:
					DOWN = True

			# Caso o usuario deixe de apertar o botão ele se torna False impossibilitando o movimento
			if event.type == KEYUP:
				if event.key == K_LEFT or event.key == K_a:
					LEFT = False
				if event.key == K_RIGHT or event.key == K_d:
					RIGHT = False
				if event.key == K_UP or event.key == K_w:
					UP = False
				if event.key == K_DOWN or event.key == K_s:
					DOWN = False
				if event.key == K_x:
					PLAYER_LOCAL = [randint(0, WIDTH - tamanho_comida), randint(0, HEIGHT - tamanho_comida)]

			# Cria comida na posição do mouse
			if event.type == MOUSEBUTTONDOWN:
				comidas.append(pygame.Rect(mouse[0], mouse[1], tamanho_comida, tamanho_comida))

		# Temporizador para criar comida a cada x segundos
		temporizador_comida_nova += 1
		if temporizador_comida_nova >= comida_nova:
			temporizador_comida_nova = 0
			comidas.append(pygame.Rect(randint(0, WIDTH - tamanho_comida), randint(0, HEIGHT - tamanho_comida), tamanho_comida, tamanho_comida))
		
		# o : cria uma nova lista então isso permite que o python leia, intere e apague ao mesmo tempo
		for comida in comidas[:]:
			if player.colliderect(comida):
				comidas.remove(comida)
				tamanho_player += 1
				pontos += 1

				if tocar_comer:
					comer.play()

		screen.blit(player_img_stretch, player)
		for comida in comidas:
			screen.blit(food, comida)
		draw_text(str(pontos), (255, 255, 255), screen, 20, 20)
		#display_fps(clock)
		pygame.display.update()
		clock.tick(200)
main()