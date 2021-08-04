import pygame
import sys, os, random
from pygame.locals import *
from pygame import mixer


def load_map(path):
	f = open(path)
	data = f.read()
	f.close()
	data = data.split('\n')
	game_map = []
	for row in data:
		game_map.append(row)
		#we append the row to control the y value of each point in the row
	return game_map 


def collision_test(rect,tiles):	
	hit_list = []
	for tile in tiles:
		if rect.colliderect(tile):
			hit_list.append(tile)
	return hit_list

def move(rect,movement,tiles):
	collision_types = {'top':False,'bottom':False,'right':False,'left':False}
	rect.x += movement[0]
	hit_list = collision_test(rect,tiles)
	for tile in hit_list:
		if movement[0] > 0:
			rect.right = tile.left
			collision_types['right'] = True
		elif movement[0] < 0:
			rect.left = tile.right
			collision_types['left'] = True

	rect.y += movement[1]
	hit_list = collision_test(rect,tiles)
	for tile in hit_list:
		if movement[1] > 0:
			rect.bottom = tile.top
			collision_types['bottom'] = True
		elif movement[1] < 0:
			rect.top = tile.bottom
			collision_types['top'] = True
	return rect, collision_types


def generate_player(game_map):
	y = 0
	for row in game_map:
		x = 0
		for tile in row:
			if tile == 'P':
				return [x*32, y*32]
			x += 1
		y += 1



def get_fire_anims(screen, anim_count, xcount, ycount, spritesheet_img):
	surf = pygame.Surface((9, 24))#.convert_alpha()
	surf.blit(spritesheet_img, (0, 0), (xcount, ycount, 9, 24))
	surf.set_colorkey((0, 0, 0))
	return surf
