import math
import random
import sys

import pygame
from pygame.locals import QUIT

def obstacleMovement(obstacleList,speed):
  if obstacleList:
    for obstacleRect in obstacleList:
      obstacleRect.x -= speed
      
      if obstacleRect.bottom == 260:
        screen.blit(bin,obstacleRect)
      else:
        screen.blit(bush,obstacleRect)
      
    obstacleList = [obstacle for obstacle in obstacleList if obstacle.x > -100]
    return obstacleList
  else:
    return []

def collision(player,obstacles):
  if obstacles:
    for obstacleRect in obstacles:
      if player.colliderect(obstacleRect):
        return False
  return True 

def pixieAnimation():
  global pixie, pixieIndex
  if pixieRect.bottom < 260:
    pixie = pixieJump
  else:
    pixieIndex += 0.1
    if pixieIndex >= len(pixieRun):
      pixieIndex = 0
    pixie = pixieRun[int(pixieIndex)]
    
pygame.init()

clock = pygame.time.Clock()
FPS = 90
FRAMEWIDTH = 800
FRAMEHEIGHT = 500
score = 0
highscore = 0
playerGravity = 0
ballGravity = 0
gameActive = True
gameStarted = False
speed = 4

screen = pygame.display.set_mode((FRAMEWIDTH, FRAMEHEIGHT))
pygame.display.set_caption("PixieBall")

#image surfaces
bg = pygame.image.load("assets/background.png").convert_alpha()

pixie1 = pygame.image.load("assets/pixie/pixie.png").convert_alpha()
pixie2 = pygame.image.load("assets/pixie/pixie2.png").convert_alpha()
pixie3 = pygame.image.load("assets/pixie/pixie3.png").convert_alpha()
pixieRun = [pixie1,pixie2,pixie3]
pixieIndex = 0
pixieJump = pygame.image.load("assets/pixie/pixie2.png").convert_alpha()
pixie = pixieRun[pixieIndex]

bin = pygame.image.load("assets/bin.png").convert_alpha()
bush = pygame.image.load("assets/bush.png").convert_alpha()
ball = pygame.image.load("assets/ball.png").convert_alpha()
#fonts
titleFont = pygame.font.Font("assets/dpcomic.ttf",80)
textFont = pygame.font.Font("assets/dpcomic.ttf",60)
scoreFont = pygame.font.Font("assets/dpcomic.ttf",40)
#text surfaces
title = titleFont.render("PIXIEBALL",False,"Black")
text = textFont.render("PRESS ANY KEY TO START", False, "Black")
gameOver = titleFont.render("GAME OVER",False,"Black")
#rectangles
titleRect = title.get_rect(center = (FRAMEWIDTH/2 , 60))
textRect = text.get_rect(center = (FRAMEWIDTH/2,180))
pixieRect = pixie.get_rect(bottomleft = (50,260))
ballRect = ball.get_rect(bottomleft = (500,260))
gameOverRect = gameOver.get_rect(center = (FRAMEWIDTH/2,75))

obstacleRectList = []

bgWidth = bg.get_width()

scroll = 0
tiles = math.ceil(800/bgWidth) + 1

obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer,1500)

while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    if gameActive and gameStarted:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and pixieRect.bottom == 260:
          playerGravity = -14
      if event.type == obstacleTimer:
        if random.randint(0,2):
          obstacleRectList.append(bin.get_rect(bottomleft = (random.randint(1200,1500),260)))
          obstacle = bin
        else:
          obstacleRectList.append(bush.get_rect(bottomleft = (random.randint(1200,1500),261)))
          obstacle = bush

    else:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        gameActive = True
        gameStarted = True
        score = 0
  
  if gameActive:
    speed = 4
    screen.blit(bg,(0,0)) 
    screen.blit(title,titleRect)
    screen.blit(text,textRect)
    screen.blit(pixie,pixieRect)
    if gameStarted:
      for i in range(0,tiles):
        screen.blit(bg,(i*bgWidth + scroll,0))
      scroll -= speed
      if abs(scroll) > bgWidth: scroll = 0
  
      scoreSurf = scoreFont.render(str(score),False,"Black")
      screen.blit(scoreSurf,(20,20))
  
      #player
      playerGravity += 0.4
      pixieRect.y += playerGravity
      if pixieRect.bottom >= 260: pixieRect.bottom = 260
      pixieAnimation()
      screen.blit(pixie,pixieRect)

      #ball
      ballGravity += 0.4
      ballRect.y += ballGravity 
      if ballRect.bottom >= 260:
        ballRect.bottom = 260
        ballGravity = -12
      screen.blit(ball,ballRect)

      #obstacle movement
      obstacleRectList = obstacleMovement(obstacleRectList,speed)

      gameActive = collision(pixieRect,obstacleRectList)
      
      score += 1
      if score % 1000 == 0:
        speed += 0.5
  else: 
    if score > highscore:
      highscore = score
      
    showScore = textFont.render("SCORE: " + str(score),False,"Black")
    showScoreRect = showScore.get_rect(center = (FRAMEWIDTH/2,150))

    showHigh = textFont.render("HIGH SCORE: " + str(highscore),False,"Black")
    showHighRect = showHigh.get_rect(center = (FRAMEWIDTH/2,220))
    
    screen.blit(bg,(0,0))
    screen.blit(gameOver,gameOverRect)
    screen.blit(showScore,showScoreRect)
    screen.blit(showHigh,showHighRect)
    obstacleRectList.clear()
           
  pygame.display.update()
  clock.tick(FPS)

