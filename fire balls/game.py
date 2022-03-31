import pygame
from sys import exit 
from pygame import mixer
import random


pygame.init()
window = pygame.display.set_mode((800,400)) # window set W x H
clock = pygame.time.Clock()
pygame.display.set_caption('FIRE BALLS')
Icon = pygame.image.load('img/ship.png')
pygame.display.set_icon(Icon)

def display_score():
	current_time = pygame.time.get_ticks()- start_time
	score_surf =  text_font.render("Score - "+str(current_time//1000),False,"white") 
	score_rect = score_surf.get_rect(center=(60,20))
	window.blit(score_surf,score_rect)
	return current_time //1000
#bullet
bul_surf  = pygame.image.load("img/attack.png")
bul_surf = pygame.transform.scale(bul_surf,(20,20))
bul_rect = bul_surf.get_rect(midbottom = (0,0))


text_font = pygame.font.Font(None,30)
start_time = 0
#music
mixer.music.load("sounds/background_music.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.3)
bomb = mixer.Sound("sounds/explosion-sound.mp3")
bomb.set_volume(0.1)
gun_sound = mixer.Sound("sounds/laser.wav")
gun_sound.set_volume(0.3)
fire_y = 100 # v point of all the fire balls are same
#fire
fire_1 = pygame.image.load("img/fire_2.png")
fire_1 = pygame.transform.scale(fire_1,(80,80))
fire_1_rect = fire_1.get_rect( midbottom = (100,fire_y) )

fire_2 = pygame.image.load("img/fire_2.png")
fire_2 = pygame.transform.scale(fire_2,(80,80))
fire_2_rect = fire_2.get_rect( midbottom = (300,fire_y) )

fire_3 = pygame.image.load("img/fire_2.png")
fire_3 = pygame.transform.scale(fire_3,(80,80))
fire_3_rect = fire_3.get_rect( midbottom = (600,fire_y ) )

fire_right = pygame.image.load("img/fire_right.png")
fire_right = pygame.transform.scale(fire_right,(80,80))
fire_right_rect = fire_right.get_rect( midbottom = (780,200 ))


#player
player = pygame.image.load("img/ship.png")
player = pygame.transform.scale(player,(80,80))
player_rect = player.get_rect( midbottom = (400,300))

#sapce
space = pygame.image.load("img/sapce.png")
space = pygame.transform.scale( space ,(800,400))

#loading screen 
load_srcn = pygame.image.load("img/bg.png")

runs = False
give_direct = True
fire  = False

while True :
	for events in pygame.event.get():
		if events.type == pygame.QUIT:
			pygame.quit()
			exit()
	
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT] and player_rect.left  > 0 :
		player_rect.x -= 5
	if keys[pygame.K_RIGHT] and player_rect.right  < 800 :
		player_rect.x += 5
	if keys[pygame.K_UP] and player_rect.top  > 0 :
		player_rect.y -= 5 
	if keys[pygame.K_DOWN] and player_rect.bottom < 400 :
		player_rect.y += 5
	if keys[pygame.K_SPACE] and not fire and runs:
		fire = True
		gun_sound.play()
	
	if keys[pygame.K_p] and not runs:
		fire_1_rect.bottom  = 0
		fire_2_rect.bottom  = 0
		fire_3_rect.bottom  = 0
		start_time =  pygame.time.get_ticks() #dono how this works (kekw)
		player_rect.x = 400
		player_rect.y = 300
		fire_right_rect.right = 0
	
		runs = True

	#read hight score
	with open("game file\score.txt","r") as file :
			high_score  = int(file.read())
	
	if runs :

		
		#right fire ball
		fire_right_rect.x -=2.5
		if fire_right_rect.x < 0:
			fire_right_rect.x = 780
			fire_right_rect.y =  random.randint(50,350)

		#normal fire balls	
		fire_1_rect.bottom += 3
		fire_2_rect.bottom += 3
		fire_3_rect.bottom += 3
		if fire_1_rect.bottom >350 or fire_2_rect.bottom >350 or fire_3_rect.bottom >350 :
			fire_1_rect.bottom ,fire_2_rect.bottom ,fire_3_rect.bottom = 0,0,0
			fire_1_rect.left  = random.randint(50,200)
			fire_2_rect.left  = random.randint(200,450)
			fire_3_rect.left  = random.randint(450,700)
		#player	
		window.blit(space,(0,0))
		display_score()
		window.blit(fire_1,fire_1_rect)
		window.blit(fire_2,fire_2_rect)
		window.blit(fire_3,fire_3_rect)
		window.blit(fire_right,fire_right_rect)
		window.blit(player,player_rect)
		
		# clown fest starts here
		if not fire :
				bul_rect.y = player_rect.y

		#when space bar is pressed fire is True
		if fire:
			bul_rect.y -= 4
		#bullet
			window.blit(bul_surf,bul_rect)
			if give_direct :
				bul_rect.x = player_rect.x + 30 # so x of bullter and player are same
				give_direct = False			
		if bul_rect.y < 0 or not fire :
			bul_rect.x = player_rect.x + 30
			bul_rect.y = player_rect.y
			#when bullet is out of screen then fire == False
			fire = False
		
		#collision
		if player_rect.colliderect(fire_1_rect) or player_rect.colliderect(fire_2_rect) or player_rect.colliderect(fire_3_rect) or player_rect.colliderect(fire_right_rect):
			runs = False
			#write high score after the player is dead
			if display_score() > high_score :
				with open("game file\score.txt","w") as file :
					file.write(str(display_score()))
			
		if fire_right_rect.colliderect(fire_1_rect): 
			fire_1_rect.bottom  = 0
			bomb.play()
		if fire_right_rect.colliderect(fire_2_rect): 
			fire_2_rect.bottom  = 0
			bomb.play()
		if fire_right_rect.colliderect(fire_3_rect): 
			fire_3_rect.bottom  = 0
			bomb.play()

		if bul_rect.colliderect(fire_1_rect)  :
			fire_1_rect.bottom  = 0
			bul_rect.x = player_rect.x + 30
			bul_rect.y = player_rect.y
			fire = False
		if bul_rect.colliderect(fire_2_rect)  :
			fire_2_rect.bottom  = 0
			bul_rect.x = player_rect.x + 30
			bul_rect.y = player_rect.y
			fire = False
		if bul_rect.colliderect(fire_3_rect)  :
			fire_3_rect.bottom  = 0
			bul_rect.x = player_rect.x + 30
			bul_rect.y = player_rect.y
			fire = False
		if bul_rect.colliderect(fire_right_rect)  :
			fire_right_rect.x = 780
			bul_rect.x = player_rect.x + 30
			bul_rect.y = player_rect.y
			fire = False
		

	else :
		#start / end window 
		window.fill((0,0,0))
		window.blit(load_srcn,(-10,-10)) # to fix img pos
		high_sc_sruf = text_font.render("High Score : " + str(high_score),False,"white")
		window.blit(high_sc_sruf ,(50,0))
	pygame.display.update()
	clock.tick(60) #fps


