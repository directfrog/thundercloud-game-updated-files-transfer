from code import * 
import pygame 


################# SETTING UP THE SCREEN AND ALL OF THE IMAGES THAT ARE ON IT ####################
background = pygame.image.load('background.png')
chest_img = pygame.image.load('chest.png')
test_menu = pygame.image.load('test_menu.png')
crossair_image = pygame.image.load('crossair.png')
tilemap = pygame.image.load('assets/tilemap.png')
tilemap.set_colorkey((255, 255, 255))
firstscene = load_map('tilemaps/scene1.txt')
spritesheet_img = pygame.image.load('assets/fire.png').convert()
spritesheet_img.set_colorkey((0,0,0))
small_house = pygame.image.load('assets/small house.png')
small_house = pygame.transform.scale(small_house, (int(small_house.get_width()/1.5), int(small_house.get_height()/1.5)))
big_house = pygame.image.load('assets/big house.png')
big_house = pygame.transform.scale(big_house, (int(big_house.get_width()/1.5), int(big_house.get_height()/1.5)))


##### Getting player spritesheet #####
player = pygame.image.load('assets/player spritesheet.png')
player_scale = 2
player = pygame.transform.scale(player, (player.get_width()*player_scale, player.get_height()*player_scale))
player.set_colorkey((255, 255, 255))

##### Setting base map and render box #####
x_spawn, y_spawn = generate_player(firstscene)
player_rect = pygame.Rect(x_spawn, y_spawn, 12, 32)
render_box = pygame.Rect(-32, -32, screen_width+32, screen_height+32)
scroll = [0, 0]

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


	#### standalone tile_structures ###
 	'a':(0, 0, 96, 96), # small island three by three with grass on top
	'b':(95, 0, 33, 95), # small three block column
	'c':(95, 95, 34, 35), # singular tile
	'd':(0, 96, 96, 35), # three block wide platform
}

#####  map data for player tilemap #####
player_img_data = {
	'idle':(8*player_scale, 0*player_scale, 8*player_scale, 16*player_scale),
	'run1':(0*player_scale, 0*player_scale, 8*player_scale, 16*player_scale),
	'run2':(16*player_scale, 0*player_scale, 8*player_scale, 16*player_scale),
	'wallleft':(31*player_scale, 0*player_scale, 8*player_scale, 16*player_scale),
	'wallright':(25*player_scale, 0*player_scale, 8*player_scale, 16*player_scale)
}
