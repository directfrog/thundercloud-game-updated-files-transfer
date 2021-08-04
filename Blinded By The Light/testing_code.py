import pygame
import sys, os, random
from pygame.locals import *
import math

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 400), 0, 32) 

player = pygame.image.load('C:\\Users\\Roman\\Desktop\\python\\Blinded By The Light\\assets\\player spritesheet.png')
player_scale = 6
player = pygame.transform.scale(player, (player.get_width()*player_scale, player.get_height()*player_scale))
player.set_colorkey((255, 255, 255))


run_img = 'idle'

while True:
	screen.fill((100, 100, 100))

	screen.blit(player, (0, 0))
	screen.blit(player, (200, 100),(31*player_scale, 0*player_scale, 8*player_scale, 16*player_scale))
	screen.blit(player, (200, 200), (25*player_scale, 0*player_scale, 8*player_scale, 16*player_scale))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()

	pygame.display.update()
	clock.tick(60)
	
