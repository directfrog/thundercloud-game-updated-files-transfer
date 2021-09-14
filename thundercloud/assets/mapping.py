import pygame, sys
from pygame.locals import *
import time
clock = pygame.time.Clock()
pygame.init()

screen = pygame.display.set_mode((800, 800), 0, 32)
guardian_walk = pygame.image.load('guardian/walk.png').convert()
guardian_walk.set_colorkey((255, 255, 255))
guardian_attack = pygame.image.load('guardian/attack1.png').convert()
guardian_attack.set_colorkey((0, 0, 0))
guardian_hit = pygame.image.load('guardian/hit.png').convert()
guardian_hit.set_colorkey((0, 0, 0))


scale = 1
guardian_walk = pygame.transform.scale(guardian_walk, (guardian_walk.get_width()*scale, guardian_walk.get_height()*scale))


tick = 0
attack_tick = 0
guardian_anim_count = 30

guardian_walking = True
guardian_attacking = False
guardian_taken_damage = False

frame_finished = False
hit_finished = False
guardian_flip = False
guardian_rect = pygame.Rect(300, 300, 30, 90)
guardian_rect_b = pygame.Rect(320, 300, 30, 90)
guardian_moving_left = False 
guardian_moving_right = False


player_rect = pygame.Rect(400, 325, 10, 10)
moving_left = False 
moving_right = False

player_color = (255, 255, 255) 

guardian_count_reset = []
collision = False

while True:
	screen.fill((50, 50, 50))
	
	if guardian_taken_damage:
		guardian_walking = False 
		guardian_attacking = False

	if guardian_walking:
		screen.blit(pygame.transform.flip(guardian_walk, guardian_flip, False), (guardian_rect.x, guardian_rect.y), (10, guardian_anim_count-30, 110, 100))
		current_frame = guardian_walk
	if guardian_attacking:
		screen.blit(pygame.transform.flip(guardian_attack, guardian_flip, False), (guardian_rect.x, guardian_rect.y), (10, guardian_anim_count-30, 110, 100))
		current_frame = guardian_attack
	if guardian_taken_damage:
		screen.blit(pygame.transform.flip(guardian_hit, guardian_flip, False), (guardian_rect.x, guardian_rect.y), (10, guardian_anim_count-30, 110, 100))
		current_frame = guardian_hit

	pygame.draw.rect(screen, player_color, player_rect)

	print(guardian_anim_count, current_frame.get_height())

	if moving_left == True:
		player_rect.x -= 6
	if moving_right==True:
		player_rect.x += 6

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
		if frame_finished:
			player_color = (255, 0, 0)
		if frame_finished == False:
			player_color = (255, 255, 255)
	else:
		player_color = (255, 255, 255)
		collision = False


	if player_rect.colliderect(guardian_rect)==0 and  player_rect.colliderect(guardian_rect_b)==0:
		guardian_attacking = False
		guardian_walking = True

	if collision:
		guardian_count_reset.append(0)
	else:
		guardian_count_reset.append(1)
	if len(guardian_count_reset) > 20:
		collision = [guardian_count_reset[-1]]

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
			if event.key == K_SPACE:
				guardian_taken_damage = True
		if event.type == KEYUP:
			if event.key == K_a:
				moving_left = False 
			if event.key == K_d:
				moving_right = False
			if event.key == K_SPACE:
				guardian_taken_damage = False 
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
	pygame.display.update()
	clock.tick(60)