import pygame
import sys, os, random
from pygame.locals import *
import math

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 400), 0, 32) 


#img = pygame.image.load('test_ligntning.png')

ran_x = random.randint(0, 500)
rects = [[pygame.Rect(ran_x, 0, 5, 15 ), [ran_x, 0]]]
collide_point = [300, 300]
x_dif = 0 
y_dif = 0
collision_rect = pygame.Rect(300, 300, 10, 10)

def get_joint(a, b):
    if a[1] < b[1]:
        return a[0], b[1]
    if a[1] > b[1]:
        return b[0], a[1]

def get_degree(a, b):
    x, y = get_joint(a, b)
    hypotenuse = math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    agacent = math.sqrt((a[0]-x)**2 + (a[1]-y)**2)
    angle = math.acos(agacent/hypotenuse)
    return angle




while True:
	screen.fill((0, 0, 0))


	mouse_x, mouse_y = pygame.mouse.get_pos()
	pygame.draw.rect(screen, (0, 0, 255), collision_rect)


	for rect in rects:
		pygame.draw.rect(screen, (255, 255, 255), rect[0])
		x_diff = rect[1][0]-collide_point[0]
		y_diff = rect[1][1]-collide_point[1]
		true_x_dif = rect[0].x-collide_point[0]
		true_y_dif = rect[0].y-collide_point[1]

		print(true_x_dif, true_y_dif)

		rect[0].x -= x_diff/30
		rect[0].y -= y_diff/30

		if rect[0].colliderect(collision_rect):
			rects.remove(rect)


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

