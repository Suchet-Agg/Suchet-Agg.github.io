#IP Home Assignment 5
#Suchet Aggarwal
#2018105
#CSE
#Section A Group 1

import pygame
from pygame.locals import *
from numpy import loadtxt
import time

#Constants for the game
WIDTH, HEIGHT = (32, 32)
COIN_SIZE = 3
PACMAN_SIZE = 15
WALL_COLOR = pygame.Color(0, 0, 255, 255) # BLUE
COIN_COLOR = pygame.Color(255, 255, 0, 255) # WHITE
PACMAN_COLOR = pygame.Color(255, 255, 0, 255) # YELLOW
ENEMY_COLOR = pygame.Color(250, 80, 10, 0) 
DOWN = (0,1)
RIGHT = (1,0)
TOP = (0,-1)
LEFT = (-1,0)


#Draws a rectangle for the wall
def draw_wall(screen, pos):
	pixels = pixels_from_points(pos)
	pygame.draw.rect(screen, WALL_COLOR, [pixels, (WIDTH, HEIGHT)])

#Draws a rectangle for the player
def draw_pacman(screen, pos,p): 
	pixels = pixels_from_points(pos)
	pac = ["up.png","left.png","right.png","down.png"]
	pacman = pygame.image.load(pac[p])
	pacman_mini = pygame.transform.scale(pacman, (32, 32))
	screen.blit(pacman_mini, pixels)

#Draws a rectangle for the coin
def draw_coin(screen, pos):
	pixels = pixels_from_points(pos)
	a=pixels[0]+16
	b=pixels[1]+16
	pixels=(a,b)
	pygame.draw.circle(screen, COIN_COLOR,pixels,COIN_SIZE)

#Draws a rectangle for the enemy
def draw_enemy(screen, pos,no): 
	pixels = pixels_from_points(pos)
	enem = ["e1.png","e2.png","e3.png"]
	ene = pygame.image.load(enem[no%3])
	ene_mini = pygame.transform.scale(ene, (25, 19))
	screen.blit(ene_mini, pixels)

#Draws lives remaining for the player
def draw_lives(screen, x, y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x + 30 * i
		img_rect.y = y
		screen.blit(img, img_rect)

#Uitlity functions
def add_to_pos(pos, pos2):
	return (pos[0]+pos2[0], pos[1]+pos2[1])
def pixels_from_points(pos):
	return (pos[0]*WIDTH, pos[1]*HEIGHT)

#Initializing pygame
pygame.init()
screen = pygame.display.set_mode((640,640), 0, 32)
background = pygame.surface.Surface((640,640)).convert()


#Initializing variables
layout = loadtxt('layout.txt', dtype=str)
rows, cols = layout.shape
score = 0
pacman_position = (1,1)
background.fill((0,0,0))
#stores no of enemies in the game
NoOfEne =0
MaxScore = 0
for col in range(cols):
		for row in range(rows):
			value = layout[row][col]
			pos = (col, row)
			if value == 'e':
				NoOfEne +=1
			elif value == 'c':
				MaxScore +=1
#list storing values of the layout corresponfing to the next position of the enemy
temp = []
for i in range(NoOfEne):
	temp.append('.')
#5 lives for the player
life =5
p=2
# Main game loop 
while True:
	#lists sotring the positions for coins,enemies,and wall
	coinPos=[]
	wallPos=[]
	enePos=[]
	k=1
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

	screen.blit(background, (0,0))

	#Draw board from the 2d layout array.
	#In the board, '.' denote the empty space, 'w' are the walls, 'c' are the coins, and 'e' are the enemies
	for col in range(cols):
		for row in range(rows):
			value = layout[row][col]
			pos = (col, row)
			if value == 'w':
				draw_wall(screen, pos)
				wallPos.append(pos)
			elif value == 'c':
				draw_coin(screen, pos)
				coinPos.append(pos)
			elif value == 'e' :
				draw_enemy(screen, pos,k)
				enePos.append(pos)
				k+=1

	#Draw the player
	draw_pacman(screen, pacman_position,p)
	
	#Display score
	myfont = pygame.font.SysFont("monospace", 16)
	scoretext = myfont.render("Score = "+str(score), 1, (255,255,255))
	screen.blit(scoretext, (5, 10))
	
	#display lives
	lives = pygame.image.load("life.png")
	lives_mini = pygame.transform.scale(lives, (25, 19))
	draw_lives(screen, 480, 5, life,lives_mini)

	#Move the Player
	move_direction = (0,0)
	#Move the enemies
	enemy_direction = []

	#input from the user
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN :
			if event.key == ord('w') :
				move_direction = TOP
				p=0
			elif event.key == ord('a') :
				move_direction = LEFT
				p=1
			elif event.key == ord('d') :
				move_direction = RIGHT
				p=2
			elif event.key == ord('s') :
				move_direction = DOWN	
				p=3

	prevPos = pacman_position
	#Update player position based on movement.
	if add_to_pos(pacman_position, move_direction) not in wallPos:
		pacman_position = add_to_pos(pacman_position, move_direction)
	else:
		pacman_position = prevPos
	
	# coin should dissapear when eating, i.e update the layout array and score
	if pacman_position in coinPos:
		layout[pacman_position[1]][pacman_position[0]]= '.'
		score+=1
	else:
		pass

	#Move the enemy according to the current position of pacman
	for i in range(len(enePos)):
		if abs(enePos[i][0] - pacman_position[0]) > abs(enePos[i][1] - pacman_position[1]) :
			if enePos[i][0] > pacman_position[0]:
				enemy_direction.append(LEFT)
			else:
				enemy_direction.append(RIGHT)
		else:
			if enePos[i][1] > pacman_position[1]:
				enemy_direction.append(TOP)
			else:
				enemy_direction.append(DOWN)
	
	#Updating positions of enemy
	for i in range(len(enePos)):
		x = add_to_pos(enePos[i], enemy_direction[i])
		if x not in wallPos and x not in enePos:
			layout[enePos[i][1]][enePos[i][0]] = temp[i]
			temp[i] = layout[x[1]][x[0]]
			enePos[i] = x
			layout[enePos[i][1]][enePos[i][0]] = 'e'
		else:
			pass

	#check whether enemy and pacman have collided
	if pacman_position in enePos:
		score = 0
		layout = loadtxt('layout.txt', dtype=str)
		pacman_position = (1,1)
		life -=1
	else:
		pass 

	#check maximum score and flash Winning screen
	if score == MaxScore:
		myfont = pygame.font.SysFont("monospace", 100)
		win = myfont.render("YOU WIN", 1, (255,255,255))
		TextRect = win.get_rect()
		TextRect.center = ((320),(320))
		screen.blit(win, TextRect)
		pygame.display.update()
		time.sleep(5)

	#Check lives remaining and if equal to zero flash GAME OVER
	elif life == 0:
		myfont = pygame.font.SysFont("monospace", 100)
		lose = myfont.render("GAME OVER", 1, (255,255,255))
		TextRect = lose.get_rect()
		TextRect.center = ((320),(320))
		screen.blit(lose, TextRect)
		pygame.display.update()
		time.sleep(5)	

	time.sleep(0.1)

	#Update the display
	pygame.display.update()


	
