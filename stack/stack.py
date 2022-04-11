import pygame
import random
import sys
from pygame import mixer

pygame.init()
clock = pygame.time.Clock()

win = pygame.display.set_mode((800, 600))

text_font = pygame.font.Font(None,30)
def def_score(x):
	ply_score_surf =  text_font.render("Score"+" "+str(x),False,"black")
	ply_score_surf_rect = ply_score_surf.get_rect(center=(40,30))
	win.blit(ply_score_surf,ply_score_surf_rect)

click = mixer.Sound("click.mp3")
click.set_volume(0.1)


class Tile():
	def __init__(self,x,y,color,w,facing):
		self.x = x 
		self.y = y
		self.can_run = True
		self.color = color
		self.w = w
		self.h = 10
		self.vel = 5 * facing
		self.face = facing

	def draw(self,window):
		self.img =  pygame.Rect(self.x,self.y,self.w,self.h)
		pygame.draw.rect(window,self.color,self.img)
		if self.can_run:
			self.x -= self.vel
		if self.x > 900 :
			self.x = -20 
		if self.x < -100 :
			self.x = 900  

index = 580
tile_w = 200
tiles_set = []
new_tile = True

#last tile 
last_x = 0
last_y = 0

loop = 1

color  = [(6, 97, 99),(205, 190, 120),(56, 56, 56),(255, 24, 24),(255, 195, 0),(84, 99, 255),(25, 40, 47),(179, 48, 48),(211, 236, 167)]
score = 0
runs = True
face =[1,-1]

set_pos = 800

while True:
	color_pick = random.choice(color)
	face_p = random.choice(face)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit(0)

		if runs :
			if event.type == pygame.MOUSEBUTTONDOWN:
					for tile in tiles_set:
						if loop >=2:
							if tile.x < last_x : # For left
								tile.w = tile.w - (last_x  - tile.x)
								tile.x  = last_x
								tile_w = tile.w
							else: #for right
								tile.w = tile.w - (tile.x  - last_x )
								tile.x  = last_x
								tile_w = tile.w
							if tile.w <= 0 :
								runs = False
								
						last_x = tile.x
						tile.can_run = False
						new_tile = True
						loop += 1
						click.play()
					else:
						score += 1	
		else :
			keys = pygame.key.get_pressed()
			if keys[pygame.K_p]:
				runs = True
				last_x = 0
				last_y = 0
				loop = 1
			index = 580
			tile_w = 200
			tiles_set.clear()
			score = 0


	if runs:
		if new_tile:
			if face_p == 1 :
				set_pos = 800
			else :
				set_pos = 0
			tiles_set.append(Tile(set_pos,index,color_pick,tile_w,face_p))
			index -= 10
			new_tile =  False 
			
		
		win.fill((242, 242, 242))
		def_score(score)
		for tile in tiles_set:
			tile.draw(win)

	else :
		win.fill((0,0,0))
		lost =  text_font.render("Press P to play again",False,"green")
		lost_r = lost.get_rect(center=(400,200))
		win.blit(lost,lost_r)

			


	pygame.display.update()
	clock.tick(60)