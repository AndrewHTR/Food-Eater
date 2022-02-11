import pygame, sys
from pygame.locals import *
from random import randint
# Iniciando pygame
pygame.init()

# Janela
WIDTH  = 400
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Cat Foooood")
clock = pygame.time.Clock()

def main():
	# Jogador
	RIGHT     = False
	LEFT      = False
	UP    	  = False
	DOWN  	  = False
	MOVESPEED = 5

	PLAYER_LOCAL = [screen.get_size()[0]/2, screen.get_size()[1]/2]

	# Comida
	comidas = []
	temporizador_comida_nova = 0
	comida_nova = 40
	tamanho_comida = 20
	for i in range(20):
		comidas.append(pygame.Rect(randint(0, WIDTH - tamanho_comida), randint(0, HEIGHT - tamanho_comida), tamanho_comida, tamanho_comida))

	while True:
		screen.fill((0,0,0))
		mouse = pygame.mouse.get_pos()

		# Movimento do jogador
		player = pygame.Rect(PLAYER_LOCAL[0], PLAYER_LOCAL[1], 40, 40)
		if LEFT == True:
			PLAYER_LOCAL[0] -= MOVESPEED
		if RIGHT == True:
			PLAYER_LOCAL[0] += MOVESPEED
		if UP == True:
			PLAYER_LOCAL[1] -= MOVESPEED
		if DOWN == True:
			PLAYER_LOCAL[1] += MOVESPEED

		# Checagem de colisão com a borda da tela
		if player.top <= 0:
			if UP == True:
				UP = False
				PLAYER_LOCAL[1] = 0
		if player.bottom >= HEIGHT:
			if DOWN == True:
				DOWN = False
				PLAYER_LOCAL[1] = HEIGHT - 40
		if player.left <= 0:
			if LEFT == True:
				LEFT = False
				PLAYER_LOCAL[0] = 0
		if player.right >= WIDTH:
			if RIGHT == True:
				RIGHT = False
				PLAYER_LOCAL[0] = WIDTH - 40

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
			if event.type == MOUSEBUTTONUP:
				comidas.append(pygame.Rect(mouse[0], mouse[1], tamanho_comida, tamanho_comida))

		temporizador_comida_nova += 1
		if temporizador_comida_nova >= comida_nova:
			temporizador_comida_nova = 0
			comidas.append(pygame.Rect(randint(0, WIDTH - tamanho_comida), randint(0, HEIGHT - tamanho_comida), tamanho_comida, tamanho_comida))
		for comida in comidas[:]:
			if player.colliderect(comida):
				comidas.remove(comida)
		for i in range(len(comidas)):
			pygame.draw.rect(screen, (0, 255, 0), comidas[i])
		pygame.draw.rect(screen, (0, 0, 255), player)
		pygame.display.update()
		clock.tick(60)
main()