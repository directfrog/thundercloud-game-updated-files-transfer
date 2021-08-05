import pygame
import sys, os, random
from pygame.locals import *
import math

pygame.init()
clock = pygame.time.Clock()
screen_width = 600 
screen_height = 400
screen = pygame.display.set_mode((600, 400), 0, 32) 


wind_particles = []

wind_tick = 0
while True:
	screen.fill((0, 0, 0))

	if len(wind_particles) < 3:
		if random.randint(1, 4) == 3:
			wind_particles.append([pygame.Rect(screen_width+10, random.randint(0, screen_height/2), 10, 10), random.randint(16, 20), random.choice([-1, 1])])

	for wind_particle in wind_particles:
		pygame.draw.rect(screen, (255, 255, 255), wind_particle[0])
		wind_particle[0].x -= wind_particle[1]
		wind_particle[0].y -= wind_particle[2] 
		if wind_particle[0].x < 0:
			wind_particles.remove(wind_particle)


	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()


	wind_tick += 1
	pygame.display.update()
	clock.tick(60)

