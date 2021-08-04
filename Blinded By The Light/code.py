import pygame
import sys, os, random
from pygame.locals import *
from pygame import mixer
from engine import *
import math

pygame.init()
clock = pygame.time.Clock()


################# SETTING UP THE SCREEN AND ALL OF THE IMAGES THAT ARE ON IT ####################
screen_width = 300
screen_height = 200 
over_screenWidth = 1200 
over_screenHeight = 800
over_screen = pygame.display.set_mode((over_screenWidth, over_screenHeight), 0, 32)
screen = pygame.Surface((screen_width, screen_height))
dirt_img = pygame.image.load('dirt.png')
grass_img = pygame.image.load('grass.png')
player = pygame.image.load('player.png')
player = pygame.transform.scale(player, (12, 32))
background = pygame.image.load('background.png')
chest_img = pygame.image.load('chest.png')
test_menu = pygame.image.load('test_menu.png')
crossair_image = pygame.image.load('crossair.png')
tilemap = pygame.image.load('C:\\Users\\Roman\\Desktop\\python\\Blinded By The Light\\assets\\tilemap.png')
tilemap.set_colorkey((255, 255, 255))
firstscene = load_map('C:\\Users\\Roman\\Desktop\\python\\Blinded By The Light\\tilemaps\\scene1.txt')
spritesheet_img = pygame.image.load('C:\\Users\\Roman\\Desktop\\python\\Blinded By the Light\\assets\\fire.png').convert()
spritesheet_img.set_colorkey((0,0,0))

##### Getting player spritesheet #####
player = pygame.image.load('C:\\Users\\Roman\\Desktop\\python\\Blinded By The Light\\assets\\player spritesheet.png')
player_scale = 2
player = pygame.transform.scale(player, (player.get_width()*player_scale, player.get_height()*player_scale))
player.set_colorkey((255, 255, 255))

##### Setting base map and render box #####
x_spawn, y_spawn = generate_player(firstscene)
player_rect = pygame.Rect(x_spawn, y_spawn, 12, 32)
print(x_spawn, y_spawn)
render_box = pygame.Rect(-32, -32, screen_width+32, screen_height+32)
scroll = [0, 0]

######### This list contains all of the separate object 'spawn points' e.g player, chests and also blank tiles ##########
non_tile_objects = ['0', 'P', 'C']
structures = ['a', 'b', 'c', 'd']

##### Fire animations stuff #####
anim_count = 0
xcount = 9
ycount = 24

########## MAP DATA WHICH DEFIES TYPES OF TILES ##########
map_data = {
	#### Single Blocks ####
	'1':(30, 0, 32, 32), # Top tile
	'2':(0, 0, 32, 32), # top left tile
	'3':(60, 0, 35, 32), # top right tile
	'4':(0, 30, 32, 32), # middle left tile
	'5':(0, 65, 32, 30), # bottom left tile
	'6':(30, 30, 32, 32), # middle tile
	'7':(60, 65, 35, 30), # bottom right tile
	'8':(60, 30, 35, 32), # middle right tile
	'9':(30, 66, 32, 30), # bottom tile


	#### standalone structures ###
 	'a':(0, 0, 96, 96), # small island three by three with grass on top
	'b':(95, 0, 33, 95), # small three block column
	'c':(95, 95, 34, 35), # singular tile
	'd':(0, 96, 96, 35) # three block wide platform
}

#####  map data for player tilemap #####
player_img_data = {
	'idle':(8*player_scale, 0*player_scale, 8*player_scale, 16*player_scale),
	'run1':(0*player_scale, 0*player_scale, 8*player_scale, 16*player_scale),
	'run2':(16*player_scale, 0*player_scale, 8*player_scale, 16*player_scale),
	'wallleft':(31*player_scale, 0*player_scale, 8*player_scale, 16*player_scale),
	'wallright':(25*player_scale, 0*player_scale, 8*player_scale, 16*player_scale)
}


########## SETTING GAME VARIABLES #####
draw_rects = []
bolts = []
bolt_timer = 0
direction = 'left'
player_direction = 1
rotate = False
moving_left = False
moving_right = False
vertical_momentum = 0
player_tick = 0 #tick for player run animation
run_img = 'idle'

while True:
	screen.blit(background, (0, 0))

	scroll[0] = player_rect.x-152
	scroll[1] = player_rect.y-106
	

	##### Fire animations tick #####
	if xcount == 90:
		xcount = 0 
		ycount += 24

	if ycount == 144:
		xcount = 0 
		ycount = 0

	##### setting object lists that are refreshed every frame #####
	tile_rects = []
	chests = []

	########## TILE BY TILE RENDERING ALGORITHM ##########
	y = 0
	for y, row in enumerate(firstscene):
		x = 0
		for x, tile in enumerate(row):
			if (x*32-scroll[0] < render_box.x+screen_width+32) and (x*32-scroll[0] > render_box.x-64) and (y*32-scroll[1] < render_box.y+screen_height+32) and (y*32-scroll[1] > render_box.y-64):
				if tile not in non_tile_objects:
					screen.blit(tilemap, (x*32-scroll[0], y*32-scroll[1]), (map_data[tile]))
					if tile not in structures:
						tile_rects.append(pygame.Rect(x*32, y*32, 32, 32))
					if tile in structures:
						if tile == 'a':
							tile_rects.append(pygame.Rect(x*32, y*32, 96, 96))
						if tile == 'b':
							tile_rects.append(pygame.Rect(x*32, y*32, 32, 96))
						if tile == 'c':
							tile_rects.append(pygame.Rect(x*32, y*32, 32, 32))
						if tile == 'd':
							tile_rects.append(pygame.Rect(x*32, y*32, 96, 32))
				if tile in non_tile_objects:
					if tile == 'C':
						screen.blit(chest_img, (x*32, y*32))
						chests.append(pygame.Rect(x*32, y*32, 32, 32))
			x += 1
		y += 1 


	print(len(chests))
	##### looping over each chest in the game #####
	for chest in chests:
		if player_rect.colliderect(chest):
			#screen.blit(test_menu, (100, 50))
			red_sprite_select = pygame.Rect(148, 147, 40, 40)
			elve_select = pygame.Rect(198, 147, 40, 40)
			ball_select = pygame.Rect(193, 206, 40, 40)
			bolt_select = pygame.Rect(148, 205, 40, 40)

	##### Looping over and moving each lightning bolt in the game #####
	for bolt in bolts:
		image = get_fire_anims(screen, anim_count, xcount, ycount, spritesheet_img)
		screen.blit(pygame.transform.rotate(pygame.transform.scale(image, (9, 24)), bolt[2]), (bolt[0].x-scroll[0], bolt[0].y-scroll[1]))
		bolt[0].x += bolt[1]
		try:
			for tile in tile_rects:
				if bolt[0].colliderect(tile):
					bolts.remove(bolt)
		except:
			pass 
	for bolt in bolts:
		if bolt[0].x < scroll[0]-300 or bolt[0].x > scroll[0]+500:
			bolts.remove(bolt)
	
	if moving_left == False and moving_right == False:
		player_tick = 0

	##### player movement #####
	player_movement = [0,0]
	if moving_right == True:
		player_movement[0] += 2
		player_direction = 1
		player_tick += 0.5 		# PLAYER ANIM TICK
	if moving_left == True:
		player_movement[0] -= 2
		player_direction = -1
		player_tick += 0.5 		# PLAYER ANIM TICK

	player_movement[1] += vertical_momentum
	vertical_momentum += 0.3
	if vertical_momentum > 3:
		vertical_momentum = 3

	####################### moving the player/checking for collisions and changing the direction of the player ##########################
	if player_tick%5==0 and player_tick%10!=0:
		run_img = 'run1'
	if player_tick%10==0:
		run_img = 'run2'

	if player_tick == 0:
		run_img ='idle'

	player_rect, collision_types = move(player_rect, player_movement, tile_rects)
	if collision_types['bottom'] == True:
		vertical_momentum = 0	

	#if collision_types['left']==True and collision_types['bottom'] == False:
	#	run_img = 'wallleft'
	#if collision_types['right']==True and collision_types['bottom'] == False:
	#	run_img = 'wallright'

	if player_direction == -1:
		screen.blit(pygame.transform.flip(player, True, False), (player_rect.x-scroll[0], player_rect.y-scroll[1]), player_img_data[run_img])
	if player_direction == 1:
		screen.blit(player, (player_rect.x-scroll[0] , player_rect.y-scroll[1]), player_img_data[run_img])

	######### Pygame events #########
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			draw_rects.append(pygame.Rect(pos[0], pos[1], 100, 100))

		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == K_SPACE:
				vertical_momentum = -5
			if event.key == K_a:
				moving_left = True
			if event.key == K_d:
				moving_right = True 
			if event.key == K_r: 
				rotate = True
			if event.key == K_UP:
				if bolt_timer >= 10:
					if player_direction == 1:
						bolts.append([pygame.Rect(player_rect.x, player_rect.y+5, 22, 9), 3*player_direction, 90*player_direction])
						bolt_timer = 0
					if player_direction == -1:
						bolts.append([pygame.Rect(player_rect.x, player_rect.y+5, 22, 9), 3*player_direction, 90*player_direction])
						bolt_timer = 0

		if event.type == KEYUP:
			if event.key == K_a:
				moving_left = False
			if event.key == K_d:
				moving_right = False

	##### Updating the fire anim xcount #####
	anim_count += 1
	if anim_count % 1 == 0:
		xcount += 9

	##### updating screen #####
	over_screen.blit(pygame.transform.scale(screen,(over_screenWidth, over_screenHeight)),(0,0))
	pygame.display.update()
	clock.tick(60)
	bolt_timer += 1
