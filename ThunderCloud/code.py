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

bg = pygame.image.load('assets/bg.png')

level1 = False
level2 = True


def main_game():

	global level1, level2

	background = pygame.image.load('assets/background.png')
	background2 = pygame.image.load('assets/background2.png')
	background3 = pygame.image.load('assets/background3.png')
	chest_img = pygame.image.load('assets/chest.png')
	chest_img = pygame.transform.scale(chest_img, (20, 20))
	test_menu = pygame.image.load('assets/test_menu.png')
	shrub_img = pygame.image.load('assets/shrub.png')
	crossair_image = pygame.image.load('crossair.png')

	earth_tilemap = pygame.image.load('assets/earth_tilemap.png')
	earth_tilemap.set_colorkey((255, 255, 255))

	tilemap = pygame.image.load('assets/tilemap.png')
	tilemap.set_colorkey((255, 255, 255))

	ladder_img = pygame.image.load('assets/ladder.png')
	farmer = pygame.image.load('assets/farmer.png')
	spritesheet_img = pygame.image.load('assets/fire.png').convert()
	spritesheet_img.set_colorkey((0,0,0))
	small_house = pygame.image.load('assets/small house.png')
	small_house = pygame.transform.scale(small_house, (int(small_house.get_width()/1.5), int(small_house.get_height()/1.5)))
	big_house = pygame.image.load('assets/big house.png')
	big_house = pygame.transform.scale(big_house, (int(big_house.get_width()/2), int(big_house.get_height()/2)))

	##### Sad lookin stuff #####
	skeleton_img = pygame.image.load('assets/skeleton.png')
	dead_tree_1 = pygame.image.load('assets/dead_tree_1.png')
	dead_tree_2 = pygame.image.load('assets/dead_tree_2.png')

	##### Getting the scenes #####
	firstscene = load_map('tilemaps/scene1.txt')
	secondscene = load_map('tilemaps/scene2.txt')

	##### TASKS #####
	task2 = pygame.image.load('assets/task2.png')

	map_data = {
		#### Single Blocks ####
		'1':(30, 0, 32, 32), # Top tile`	
		'2':(0, 0, 32, 32), # top left tile
		'3':(60, 0, 35, 32), # top right tile
		'4':(0, 30, 32, 32), # 	middle left tile
		'5':(0, 65, 32, 30), # bottom left tile
		'6':(30, 30, 32, 32), # middle tile
		'7':(60, 65, 35, 30), # bottom right tile
		'8':(60, 30, 35, 32), # middle right tile
		'9':(30, 66, 32, 30), # bottom tile
		#### standalone tile_structures ###
	 	'a':(0, 0, 96, 96), # small island three by three with grass on top
		'b':(95, 0, 33, 95), # small three block column
		'c':(95, 95, 34, 35), # singular tile
		'd':(0, 96, 96, 35), # three block wide platform
	}


	earth_tilemap_data = {
		'1':(34, 8, 32, 32), # Top tile`	
		'2':(1, 8, 32, 32), # top left tile
		'3':(62, 8, 32, 32), # top right tile
		'4':(1, 40, 32, 34), # middle left tile
		'5':(1, 63, 32, 32), # bottom left tile
		'6':(20, 20, 32, 32), # middle tile
		'7':(63, 63, 32, 32), # bottom right tile
		'8':(62, 30, 32, 32), # middle right tile
		'9':(30, 63, 32, 32), # bottom tile
	}


	#####  map data for player tilemap #####
	player_scale = 2
	player_img_data = {
		'idle':(8*player_scale, 0*player_scale, 8*player_scale, 16*player_scale),
		'run1':(0*player_scale, 0*player_scale, 8*player_scale, 16*player_scale),
		'run2':(16*player_scale, 0*player_scale, 8*player_scale, 16*player_scale),
		'wallleft':(31*player_scale, 0*player_scale, 8*player_scale, 16*player_scale),
		'wallright':(25*player_scale, 0*player_scale, 8*player_scale, 16*player_scale)
	}

	##### Getting player spritesheet #####
	player = pygame.image.load('assets/player spritesheet.png')
	player_scale = 2
	player = pygame.transform.scale(player, (player.get_width()*player_scale, player.get_height()*player_scale))
	player.set_colorkey((255, 255, 255))
	interact = False

	##### Getting the scenes #####
	firstscene = load_map('tilemaps/scene1.txt')
	secondscene = load_map('tilemaps/scene2.txt')


	##### Setting base map and render box #####
	if level1 == True:
		x_spawn, y_spawn = generate_player(firstscene)
	if level2 == True:
		x_spawn, y_spawn = generate_player(secondscene)

	player_rect = pygame.Rect(x_spawn, y_spawn, 12, 32)
	render_box = pygame.Rect(-32, -32, screen_width+32, screen_height+32)
	scroll = [0, 0]


	##### Fire animations stuff #####
	fire_anim_count = 0
	xcount = 9
	ycount = 24

	plant1 = pygame.image.load('assets/crops/plant1.jpg').convert_alpha()
	plant1 = pygame.transform.scale(plant1, (32, 32))
	plant1.set_colorkey((255, 252, 253))
	plant2 = pygame.image.load('assets/crops/plant2.png').convert_alpha()
	plant2 = pygame.transform.scale(plant2, (32, 32))
	plant2.set_colorkey((255, 255, 255))
	plant3 = pygame.image.load('assets/crops/plant3.png').convert_alpha()
	plant3 = pygame.transform.scale(plant3, (32, 32))
	plant3.set_colorkey((255, 255, 255))

	label = pygame.image.load('assets/label 1 frames/1.png')
	label_count = 0 

	plants = [plant2, plant3]

	

	##### Map data for the trees ####
	tree_scale = 3
	trees = pygame.image.load('assets/trees.png')
	trees = pygame.transform.scale(trees, (trees.get_width()*tree_scale, trees.get_height()*tree_scale))
	trees_dict = {
		':':(0, 0, 47*tree_scale, 48*tree_scale),
		';':(208, 0, 47*tree_scale, 48*tree_scale),
		'@':(435, 0, 47*tree_scale, 48*tree_scale),
		'?':(600, 0, 47*tree_scale, 48*tree_scale)
	}


	##### SCENE INDICATOR #####
	scene = firstscene

	##### Guardian #####
	guardian_walking = True
	guardian_attacking = False
	guardian_taken_damage = False
	guardian_idling = False
	tick = 0
	attack_tick = 0
	guardian_anim_count = 30
	guardian_scale = 1
	guardian_walk = pygame.image.load('assets/guardian/walk.png').convert()
	guardian_walk.set_colorkey((255, 255, 255))
	guardian_walk = pygame.transform.scale(guardian_walk, (guardian_walk.get_width()*guardian_scale, guardian_walk.get_height()*guardian_scale))
	guardian_attack = pygame.image.load('assets/guardian/attack1.png').convert()
	guardian_attack.set_colorkey((0, 0, 0))
	guardian_idle = pygame.image.load('assets/guardian/idle.png').convert()
	guardian_idle = pygame.transform.scale(guardian_idle, (guardian_idle.get_width()*guardian_scale, guardian_idle.get_height()*guardian_scale))
	guardian_idle.set_colorkey((0, 0, 0))

	blocker_collision = False # self explanatory - this is a blocker collision LoL
	
	if level2:
		guardian = get_guardians(secondscene)
	current_frame = guardian_walk
	
	frame_finished = False
	hit_finished = False
	guardian_flip = False  
	guardian_rect = pygame.Rect(310, 40, 30, 90)
	guardian_rect_b = pygame.Rect(310, 40, 30, 90)
	guardian_moving_left = False 
	guardian_moving_right = False
	guardian_count_reset = []
	collision = False

	blockers = get_blockers(secondscene)

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
	moving_up = False
	frame_count = 0 #self explanatory <--- only an idiot would not understand what that variable is 
	air_timer = 0
	jumping = False
	plant_order = GetPlantOrder(firstscene, len(plants))

	wd = pygame.image.load('assets/witch doctor/1.png')
	wd = pygame.transform.scale(wd, (wd.get_width()*2, wd.get_height()*2))
	witch_doctor_count = 0
	wd_interact_rect = get_interact_rect(firstscene)

	##### Updated list of player positions #####
	position_cache = []
	wind_particles = []
	wind_tick = 0

	######### This list contains all of the separate object 'spawn points' e.g player, chests and also blank tiles ##########
	non_tile_objects = ['0', 'P', 'C', 'S', 'T', '?', '@', ';', ':', 'K', 'N', 'M', 'R', 'G', 'B']
	tiles_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
	tree_items = ['?', '@', ';', ':']
	tile_structures = ['a', 'b', 'c', 'd', 's']
	structures = ['e', 'f', 'l', 'x', 'y', 'p', 'g', 'W']
	entities = ['F']
	farmers = get_farmers(firstscene)

	while True:
		guardian_walking = False
		if level1 == True:
			screen.blit(background, (0, -70))
		if level2 == True:
			screen.blit(background2, (0, -70))

		pygame.draw.rect(screen, (255, 0, 0), wd_interact_rect)
		scroll[0] = player_rect.x-152
		scroll[1] = player_rect.y-106

		if level1 == True:
			scene = firstscene 
		if level2 == True:
			scene = secondscene

		##### Fire animations tick #####
		if xcount == 90:
			xcount = 0 
			ycount += 24

		if ycount == 144:
			xcount = 0 
			ycount = 0

		##### setting up variables that are reset every frame #####
		tile_rects = []
		chests = []
		ladders = []
		on_ladder = False
		clouds = get_clouds(firstscene)

		########## TILE BY TILE RENDERING ALGORITHM ##########
		y = 0
		for y, row in enumerate(scene):
			x = 0
			for x, tile in enumerate(row):
				if tile not in structures:
					if tile == '+' or tile == '-' or (x*32-scroll[0] < render_box.x+screen_width+32) and (x*32-scroll[0] > render_box.x-64) and (y*32-scroll[1] < render_box.y+screen_height+32) and (y*32-scroll[1] > render_box.y-64):
						if tile not in non_tile_objects and tile not in structures and tile not in entities:
							#print(row)
							#sys.exit()
							if tile != '+' and tile != '-':
								if tile in map_data:
									if '+' in list(row):
										screen.blit(tilemap, (x*32-scroll[0], y*32-scroll[1]), (map_data[tile]))
									if '-' in list(row):
										screen.blit(earth_tilemap, (x*32-scroll[0], y*32-scroll[1]), (earth_tilemap_data[tile]))
									else:
										screen.blit(tilemap, (x*32-scroll[0], y*32-scroll[1]), (map_data[tile]))

							if tile not in tile_structures:
								tile_rects.append(pygame.Rect(x*32, y*32, 32, 32))
							if tile in tile_structures:
								if tile == 'a':
									tile_rects.append(pygame.Rect(x*32, y*32, 96, 96))
								if tile == 'b':
									tile_rects.append(pygame.Rect(x*32, y*32, 32, 96))
								if tile == 'c':
									tile_rects.append(pygame.Rect(x*32, y*32, 32, 32))
								if tile == 'd':
									tile_rects.append(pygame.Rect(x*32, y*32, 96, 32))
								if tile == 'e':
									screen.blit(small_house, (x*32-scroll[0], y*32-scroll[1]))
						if tile in non_tile_objects:
							if tile == 'C':
								screen.blit(chest_img, (x*32-scroll[0], y*32-scroll[1]))
								chests.append(pygame.Rect(x*32, y*32, 32, 32))
				if tile == 'N':
					if (x*32-scroll[0] < render_box.x+screen_width+64) and (x*32-scroll[0] > render_box.x-100) and (y*32-scroll[1] < render_box.y+screen_height+120) and (y*32-scroll[1] > render_box.y-120):
						screen.blit(dead_tree_1, (x*32-scroll[0], y*32-scroll[1]-80))

				if tile == 'S':
					if (x*32-scroll[0] < render_box.x+screen_width+32) and (x*32-scroll[0] > render_box.x-80) and (y*32-scroll[1] < render_box.y+screen_height+64) and (y*32-scroll[1] > render_box.y-120):
						screen.blit(skeleton_img, (x*32-scroll[0], y*32-scroll[1]-90))

				if tile in tree_items:
					if (x*32-scroll[0] < render_box.x+screen_width+64) and (x*32-scroll[0] > render_box.x-130) and (y*32-scroll[1] < render_box.y+screen_height+160) and (y*32-scroll[1] > render_box.y-64):
						screen.blit(trees, (x*32-scroll[0], y*32-scroll[1]-90), (trees_dict[tile]))

				if tile == 'W':
					screen.blit(wd, (x*32-scroll[0], y*32-scroll[1]-168))

				if tile in structures:
					if (x*32-scroll[0] < render_box.x+screen_width+64) and (x*32-scroll[0] > render_box.x-130) and (y*32-scroll[1] < render_box.y+screen_height+160) and (y*32-scroll[1] > render_box.y-64):
						if tile == 'e':
							screen.blit(small_house, (x*32-scroll[0]-32, y*32-scroll[1]-86)) 
						if tile == 'f':
							screen.blit(big_house, (x*32-scroll[0]-32, y*32-scroll[1]-100))
						if tile == 'l' or tile == 'x' or tile == 'y':
							screen.blit(ladder_img, (x*32-scroll[0], y*32-scroll[1]))
							ladders.append([pygame.Rect(x*32, y*32, 32, 32), tile])
						if tile == 'p' or tile == 'F':
							for plant in plant_order:
								if [x*32, y*32] == plant[0]:
									screen.blit(pygame.transform.flip(plants[plant[1]], plant[2], False), (x*32-scroll[0], y*32-scroll[1]+2))
						if tile == 'g':
							screen.blit(shrub_img, (x*32-scroll[0], y*32-scroll[1]+5))
				x += 1
			y += 1 


		##### looping over each chest in the game #####
		for chest in chests:
			if player_rect.colliderect(chest):
				red_sprite_select = pygame.Rect(148, 147, 40, 40)
				elve_select = pygame.Rect(198, 147, 40, 40)
				ball_select = pygame.Rect(193, 206, 40, 40)
				bolt_select = pygame.Rect(148, 205, 40, 40)


		##### Looping over and moving each lightning bolt in the game #####
		if not level1:
			for bolt in bolts:
				image = get_fire_anims(screen, fire_anim_count, xcount, ycount, spritesheet_img)
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

		for ladder in ladders:
			if player_rect.colliderect(ladder[0]):
				on_ladder = True
				if ladder[1] == 'x':
					if player_rect.y < ladder[0].y and player_rect.y < position_cache[frame_count-1][1]:
						vertical_momentum -= 0.4
					
				if ladder[1] == 'y':
					if player_rect.y < ladder[0].y and player_rect.y < position_cache[frame_count-1][1]:
						vertical_momentum -= 0.4

		##### Guardian Functionality #####
		for blocker in blockers:
			pygame.draw.rect(screen, (255, 255, 255), (blocker.x-scroll[0], blocker.y-scroll[1], blocker.width, blocker.height))
			if guardian_rect.colliderect(blocker) or guardian_rect_b.colliderect(blocker):
				guaridan_walking = False
				guardian_idle = True
				blocker_collision = True
			if player_rect.colliderect(guardian_rect)==0 and player_rect.colliderect(guardian_rect_b)==0:
				guardian_attacking = False
				guardian_walking = True


		print(player_rect.colliderect(blocker))

		if level2:
			if abs(guardian[0]-player_rect.x) < 3000:
				if guardian_walking:
					screen.blit(pygame.transform.flip(guardian_walk, guardian_flip, False), (guardian_rect.x-scroll[0], guardian_rect.y-scroll[1]), (10, guardian_anim_count-30, 110, 100))
					current_frame = guardian_walk
				if guardian_attacking:
					screen.blit(pygame.transform.flip(guardian_attack, guardian_flip, False), (guardian_rect.x-scroll[0], guardian_rect.y-scroll[1]), (10, guardian_anim_count-30, 110, 100))
					current_frame = guardian_attack
				if guardian_taken_damage:
					screen.blit(pygame.transform.flip(guardian_hit, guardian_flip, False), (guardian_rect.x-scroll[0], guardian_rect.y-scroll[1]), (10, guardian_anim_count-30, 110, 100))
					current_frame = guardian_hit
				if guardian_idling:
					screen.blit(pygame.transform.flip(guardian_hit, guardian_flip, False), (guardian_rect.x-scroll[0], guardian_rect.y-scroll[1]), (10, guardian_anim_count-30, 110, 100))
					current_frame = guardian_idle
					guardian_walking = False 
					guardian_attacking = False
				
				if guardian_walking or guardian_attacking:
					if player_rect.x > guardian_rect.x:
						guardian_flip = False 
						guardian_moving_left = False 
						guardian_moving_right = True
					if player_rect.x < guardian_rect.x:
						guardian_flip = True
						guardian_moving_right = False
						guardian_moving_left = True 
					elif guardian_attacking:
						guardian_moving_left = False 
						guardian_moving_right = False	
				if guardian_walking:
					if guardian_moving_left == True:
						guardian_rect.x -= 1
					if guardian_moving_right == True:
						guardian_rect.x += 1

				guardian_rect_b.x = guardian_rect.x + 50
			if player_rect.colliderect(guardian_rect_b):
				guardian_flip = False
			if player_rect.colliderect(guardian_rect):
				guardian_flip = True
			if player_rect.colliderect(guardian_rect_b) or player_rect.colliderect(guardian_rect):
				collision = True	
				if guardian_count_reset[-1] == 1:
					guardian_anim_count = 30
				guardian_walking = False
				guardian_attacking = True
			else:
				collision = False 


			if collision:
				guardian_count_reset.append(0)
			else:
				guardian_count_reset.append(1)
			if len(guardian_count_reset) > 20:
				collision = [guardian_count_reset[-1]]	


		pygame.draw.rect(screen, (255, 255, 255), (guardian_rect.x-scroll[0], guardian_rect.y-scroll[1], 30, 90))

		##### Wind Particles #####
		if level1:
			if len(wind_particles) < 10:
				if random.randint(1, 4) == 3:
					for _ in range(1): ##### This number will affect the amount of wind
						wind_particles.append([pygame.Rect(screen_width+10, random.randint(0, screen_height), 3, 3), random.randint(8, 12), random.choice([-1, 1])])

			for wind_particle in wind_particles:
				pygame.draw.rect(screen, (100, 110, 100), wind_particle[0])
				wind_particle[0].x -= wind_particle[1]
				wind_particle[0].y -= wind_particle[2] 
				if wind_particle[0].x < 0:
					wind_particles.remove(wind_particle)



		##### Checking for player collision with wd_hitbox #####
		if player_rect.colliderect(wd_interact_rect):
			screen.blit(pygame.image.load('assets/interact.png'), (5, 150))
			if interact == True:
				level1 = False 
				level2 = True
				dialouge_1()


		##### Resets the position cache #####
		if len(position_cache) > 20:
			position_cache = [position_cache[-1]] # we leave the last one just for peace of mind
		
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
		if on_ladder == False:
			vertical_momentum += 0.3
		if vertical_momentum > 3:
			vertical_momentum = 3

		if on_ladder == True:
			jumping = False 
			if moving_up == False:
				vertical_momentum = 1
			if moving_up == True:
				vertical_momentum = -1.5


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
			jumping = False


		blit_surface = pygame.Surface((8*player_scale, 18*player_scale))
		blit_surface.fill((255, 0, 4))
		blit_surface.blit(player, (0, 0), player_img_data[run_img])
		blit_surface.set_colorkey((255, 0, 4))
		if player_direction == -1:
			screen.blit(pygame.transform.flip(blit_surface, True, False), (player_rect.x-scroll[0], player_rect.y-scroll[1]))
		if player_direction == 1:
			screen.blit(blit_surface, (player_rect.x-scroll[0] , player_rect.y-scroll[1]))



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
					if on_ladder == False:
						#if air_timer > 60:
						vertical_momentum = -7
						air_timer =  0
						jumping = True
				if event.key == K_a:
					moving_left = True
				if event.key == K_d:
					moving_right = True 
				if event.key == K_r: 
					rotate = True
				if event.key == K_w:
					moving_up = True 
				if event.key == K_UP:
					if bolt_timer >= 40:
						if player_direction == 1:
							bolts.append([pygame.Rect(player_rect.x, player_rect.y+5, 22, 9), 3*player_direction, 90*player_direction])
							bolt_timer = 0
						if player_direction == -1:
							bolts.append([pygame.Rect(player_rect.x, player_rect.y+5, 22, 9), 3*player_direction, 90*player_direction])
							bolt_timer = 0
				if event.key == K_e:
					interact = True


			if event.type == KEYUP:
				if event.key == K_a:
					moving_left = False
				if event.key == K_d:
					moving_right = False
				if event.key == K_w:
					moving_up = False
				if event.key == K_e:
					interact = False

		##### Updating the fire anim xcount #####
		fire_anim_count += 1
		if fire_anim_count % 1 == 0:
			xcount += 9

		if witch_doctor_count % 50 == 0:
			wd = pygame.image.load('assets/witch doctor/1.png')
			wd = pygame.transform.scale(wd, (wd.get_width()*2, wd.get_height()*2))
		if witch_doctor_count % 100 == 0:
			wd = pygame.image.load('assets/witch doctor/2.png')
			wd = pygame.transform.scale(wd, (wd.get_width()*2, wd.get_height()*2))


		position_cache.append([player_rect.x, player_rect.y])

		#### blitting lables ####
		if level1:
			if label_count < 440:
				screen.blit(label, (5, 5))
			label_count += 1
		if level2:
			if label_count < 440:
				screen.blit(task2, (5, 5))
			label_count += 1


		##### updating screen #####
		over_screen.blit(pygame.transform.scale(screen,(over_screenWidth, over_screenHeight)),(0,0))
		pygame.display.update()

		##### Counts that are used for shtuff #####
		bolt_timer += 1
		air_timer += 1
		wind_tick += 1
		frame_count = len(position_cache)-1
		witch_doctor_count += 1
		fire_anim_count += 1
		
		##### Guardian anims updating #####
		if level2:
			tick += 1
			if guardian_attacking:
				attack_tick += 1
			if tick % 10 == 0:
				guardian_anim_count += 120
				frame_finished = False
			if guardian_anim_count > current_frame.get_height()-400:
				frame_finished = True
			if guardian_anim_count > current_frame.get_height()-90:
				guardian_anim_count = 30

		clock.tick(60)


def pre_game():
	while True:
		screen.blit(bg, (0, 0))
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == K_SPACE:
					running = False
					main_game()
		over_screen.blit(pygame.transform.scale(screen,(over_screenWidth, over_screenHeight)),(0,0))
		pygame.display.update()
		clock.tick(60)


def dialouge_1():
	dialouges = [pygame.image.load('assets/dialouge frames/1.png'),
				 pygame.image.load('assets/dialouge frames/2.png'),
				 pygame.image.load('assets/dialouge frames/3.png')]

	current_dialouge = 0 
	while True:
		screen.blit(dialouges[current_dialouge], (0, 0))
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == K_SPACE:
					current_dialouge += 1
					if current_dialouge	== 3:
						level2_introduction()

		over_screen.blit(pygame.transform.scale(screen,(over_screenWidth, over_screenHeight)),(0,0))
		pygame.display.update()
		clock.tick(60)

def level2_introduction():
	intro_frame = pygame.image.load('assets/intro frame.png')

	while True:
		screen.blit(intro_frame, (0, 0))
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == K_SPACE:
					main_game()

		over_screen.blit(pygame.transform.scale(screen,(over_screenWidth, over_screenHeight)),(0,0))
		pygame.display.update()
		clock.tick(60)

		
pre_game()

