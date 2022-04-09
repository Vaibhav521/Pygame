import pygame
import sys
from pygame import mixer
import random

pygame.init()

clock = pygame.time.Clock()
win_w = 800
win_h = 500
text_font = pygame.font.Font(None,30)

pygame.display.set_caption('PONG')

def display_score():
	opp_score_surf =  text_font.render("Score"+ " "+ str(opponent_score),False,"red")
	opp_score_surf_rect = opp_score_surf.get_rect(center=(80,20))

	ply_score_surf =  text_font.render("Score" + " "+ str(player_score),False,"green")
	ply_score_surf_rect = ply_score_surf.get_rect(center=(700,20))

	window.blit(opp_score_surf,opp_score_surf_rect)
	window.blit(ply_score_surf,ply_score_surf_rect)

# text surfs

lost_surf = text_font.render(" YOU LOST ",False,"green")
lost_surf_rect = lost_surf.get_rect(center=(win_w/2,win_h/2))

win_surf = text_font.render("YOU WON",False,"green")
win_surf_rect = win_surf.get_rect(center=(win_w/2,win_h/2))

play_again = text_font.render("PRESS P TO PLAY AGAIN ",False,"green")
play_again_rect = play_again.get_rect(center=(win_w/2,(win_h/2)+30))


#muic 
jump = mixer.Sound("music/ball_bounce.wav")
jump.set_volume(0.3)

ball_out = mixer.Sound("music/ball_out.mp3")
ball_out.set_volume(0.2)

ball_hit = mixer.Sound("music/ball_hit.wav")
ball_hit.set_volume(0.4)


window = pygame.display.set_mode((win_w,win_h)) 

# shapes
ball = pygame.Rect(win_w / 2 - 15, win_h / 2 - 15, 30, 30) #posx,posy,shape_size_x,shape_size_y
player = pygame.Rect(win_w-20,win_h/2,10,100)
opponent = pygame.Rect(10,win_h/2-70,10,100)


bgcolor = pygame.Color((255,255,255))
shape_color = (251,126,20)
ball_color = (41,41,41)

ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0


opponent_speed = 12

player_score = 0
opponent_score = 0	

def ball_rest():
	global ball_speed_y , ball_speed_x
	ball.center = (win_w / 2 , win_h / 2 )
	ball_speed_y *= random.choice((1,-1))
	ball_speed_x *= random.choice((1,-1))


runs = True

while True :
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				player_speed -= 7
			if event.key == pygame.K_DOWN:
				player_speed += 7

		# when key is released then speed == 0 
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				player_speed += 7
			if event.key == pygame.K_DOWN:
				player_speed -= 7

	keys = pygame.key.get_pressed()
	if keys[pygame.K_p] and not runs:
		runs = True
		ball_speed_x = 7 * random.choice((1,-1))
		ball_speed_y = 7 * random.choice((1,-1))
		player_score = 0
		opponent_score = 0

	  
	if runs :
		#screen
		window.fill(bgcolor)
		#draw shapes
		pygame.draw.aaline(window,shape_color,(win_w/2,0),(win_w/2,win_h))
		pygame.draw.rect(window,shape_color,player)
		pygame.draw.rect(window,shape_color,opponent)
		pygame.draw.rect(window,ball_color,ball)
		display_score()

		if opponent_score == 5 or player_score == 5 :
			runs = False

		#player
		player.y += player_speed
		#stops the payer form going out of screen
		if player.top <=0:
			player.top = 0
		if player.bottom >= win_h :
			player.bottom = win_h

		#ball 
		ball.y += ball_speed_y
		ball.x += ball_speed_x
		if ball.top <=0 or ball.bottom >= win_h:
			ball_speed_y *= -1 
			jump.play()
		#if ball hits left or right 
		if ball.left <=0 :
			player_score += 1
			ball_rest() 
			ball_out.play()
			
		if ball.right >= win_w :
			opponent_score += 1 
			ball_rest()
			ball_out.play()

		#opponent
		#ball track
		if opponent.top < ball.y:
			opponent.top += opponent_speed
		if opponent.bottom > ball.y:
			opponent.bottom -= opponent_speed
		#to keep opp in screen 
		if opponent.top <=0:
			opponent.top = 0
		if opponent.bottom >= win_h :
			opponent.bottom = win_h

		# ball collide with player and opp
		if ball.colliderect(player) or ball.colliderect(opponent):
			ball_speed_x *= -1
			ball_hit.play()

	else :
		# win / lose screen
		window.fill((0,0,0))
		if opponent_score == 5:
			runs = False
			window.blit(lost_surf,lost_surf_rect)

		if player_score == 5 :
			runs = False
			window.blit(win_surf,win_surf_rect)

		window.blit(play_again,play_again_rect)

	pygame.display.update()
	clock.tick(60)


