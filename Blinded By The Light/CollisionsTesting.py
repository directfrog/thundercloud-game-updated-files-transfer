import pygame
import sys, os, random
from pygame.locals import *
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

screen_width = 500
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))

player_rect = pygame.Rect(screen_width/2, 100, 40, 80)
tiles = [pygame.Rect(200, 200, 32, 32), pygame.Rect(264, 200, 32, 32)]

def get_collisions(tiles, player_rect):
	hit_list = []
	for tile in tiles:
		if player_rect.colliderect(tile):
			hit_list.append(tile)
	return hit_list

def move_and_collide(rect, movement, tiles):
	rect.x += movement[0]
	hit_list = get_collisions(tiles, rect)
	for tile in hit_list:
		if movement[0] > 0:
			rect.right = tile.left 
		if movement[0] < 0:
			rect.left = tile.right 
	rect.y += movement[1]
	hit_list = get_collisions(tiles, rect)
	for tile in hit_list:
		if movement[1] > 0:
			rect.bottom = tile.top
		if movement[1] < 0:
			rect.top = tile.bottom
	return rect



moving_left = False
moving_right = False
moving_up = False
moving_down = False

while True:
	screen.fill((0, 0, 0))
	movement = [0, 0]

	if moving_left == True:
		movement[0] -= 5
	if moving_right == True:
		movement[0] +=  5
	if moving_up == True:
		movement[1] -= 5
	if moving_down == True:
		movement[1] += 5

	rect = move_and_collide(player_rect, movement, tiles)
	pygame.draw.rect(screen, (255, 255, 255), (player_rect.x, player_rect.y, 40, 80))


	for tile in tiles:
		pygame.draw.rect(screen, (255, 255, 255), (tile.x, tile.y, 32, 32))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == K_a:
				moving_left = True
			if event.key == K_d:
				moving_right = True
			if event.key == K_s:
				moving_down = True
			if event.key == K_w:
				moving_up = True
		if event.type == KEYUP:
			if event.key == K_a:
				moving_left = False
			if event.key == K_d:
				moving_right = False
			if event.key == K_s:
				moving_down = False
			if event.key == K_w:
				moving_up = False

	pygame.display.update()
	clock.tick(60)