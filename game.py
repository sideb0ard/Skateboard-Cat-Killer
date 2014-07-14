#!/usr/bin/env python
# code based up following the pygame tutorial here -
# http://www.raywenderlich.com/24252/beginning-game-programming-for-teens-with-python

import pygame
from pygame.locals import *
import math
import random

pygame.init()
width,height = 1140, 480
screen = pygame.display.set_mode((width,height))

gamelength = 60000 # ms
# gamelength = 5000 # ms

keys = [False, False, False, False]

pygame.mixer.init()

skater = pygame.image.load("resources/images/skater_roll.png")
skaterpop = pygame.image.load("resources/images/skater_pop.png")
skaterollie = pygame.image.load("resources/images/skater_ollie.png")
skaterimg = skater
skaterpos = [10, height - skater.get_height()]

catrun = pygame.image.load("resources/images/cat_run.png")
catsplat = pygame.image.load("resources/images/cat_splat.png")
catguyimg1 = catrun
catguyimg=catguyimg1

cattimer=100
cattimer1=0
catguys=[[1140, height - catrun.get_height() ]]
healthvalue=194

bgOne = pygame.image.load("resources/images/buildingz1.png")
bgTwo = pygame.image.load("resources/images/buildingz2.png")

bgOne_x = 0
bgTwo_x = bgOne.get_width()

healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")

gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# Load audio
olliepop = pygame.mixer.Sound("resources/audio/olliepop.wav")
olliepop.set_volume(0.75)
ollieland = pygame.mixer.Sound("resources/audio/ollieland.wav")
ollieland.set_volume(0.75)

catwah = pygame.mixer.Sound("resources/audio/catsqueek.wav")
catwah.set_volume(0.65)

#pygame.mixer.music.load('resources/audio/bass.wav')
pygame.mixer.music.load('resources/audio/hoodlike.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

running = 1
exitcode = 0
while running:
    # print pygame.font.get_fonts()
    cattimer-=1
    screen.fill(0)

    screen.blit(bgOne, (bgOne_x, 0))
    screen.blit(bgTwo, (bgTwo_x, 0))

    screen.blit(skaterimg, skaterpos)
    if cattimer==0:
        catguys.append([980, height - catrun.get_height()])
        cattimer=random.randint(0,100)
    index=0
    for catguy in catguys:
        if catguy[0]< -140:
            catguys.pop(index)
        # catguy speed ##
        #catguy[0]-=9
        catguy[0]-=10
        catrect=pygame.Rect(0, 0, (catguyimg.get_width() - 180), (catguyimg.get_height() - 180))
        catrect.top=catguy[1]
        catrect.left=catguy[0]
        if catrect.left<0:
            catguys.pop(index)
        index1=0
        skaterect=pygame.Rect(skater.get_rect())
        skaterect.left=skaterpos[0] - 80
        skaterect.top=skaterpos[1] - 50
        if catrect.colliderect(skaterect):
           catwah.play()
           catguys.pop(index)
           screen.blit(catsplat, catguy)
           healthvalue -= random.randint(10,40)
           index1+=1
        index+=1
    for catguy in catguys:
        screen.blit(catguyimg, catguy)

    font = pygame.font.Font(None, 54)
    survivedtext = font.render(str((gamelength-pygame.time.get_ticks())/gamelength)+":"+str((gamelength-pygame.time.get_ticks())/1000%60).zfill(2), True, (255,255,255))
    textRect = survivedtext.get_rect()
    textRect.topright=[1100,5]
    screen.blit(survivedtext, textRect) 
    # 6.5 - Draw health bar
    screen.blit(healthbar, (5,5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1+8,8))

    pygame.display.flip()

    bgOne_x -= 1
    bgTwo_x -= 1

    if bgOne_x <= -1 * bgOne.get_width():
        bgOne_x = bgTwo_x + bgTwo.get_width()
    if bgTwo_x <= -1 * bgTwo.get_width():
        bgTwo_x = bgOne_x + bgOne.get_width()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key==K_UP:
                keys[0]=True
            elif event.key==K_LEFT:
                keys[1]=True
            elif event.key==K_DOWN:
                keys[2]=True
            elif event.key==K_RIGHT:
                keys[3]=True
        if event.type == pygame.KEYUP:
            if event.key==K_UP:
                keys[0]=False
            elif event.key==K_LEFT:
                keys[1]=False
            elif event.key==K_DOWN:
                keys[2]=False
            elif event.key==K_RIGHT:
                keys[3]=False

    if skaterimg == skaterollie and (skaterpos[1] == height - skater.get_height()) :
        ollieland.play()
    if (skaterpos[1] == (height - skater.get_height())) : # and (skaterpos[0] + skater.get_width() < width) :
        skaterimg = skater
    if keys[0] and (skaterpos[1] == height - skater.get_height()) :
        olliepop.play()
    if keys[0] and (skaterpos[1] > 1) and skaterimg != skaterollie:
        skaterimg = skaterpop
        skaterpos[0]+=7
        skaterpos[1]-=7
    elif keys[2] and (skaterpos[1] + skater.get_height() < height) :
        skaterpos[1]+=7
    elif keys[1] and (skaterpos[0] > 0 ) and (skaterpos[1] + skater.get_height() < height ) and skaterimg == skaterollie: 
        skaterpos[0]-=7
        skaterpos[1]+=7
    elif keys[1] and (skaterpos[0] > 0 ):
        skaterpos[0]-=7
    elif keys[3] and (skaterpos[0] + skater.get_width() < width) and (skaterimg == skaterpop) :
        skaterimg = skaterollie
        skaterpos[0]+=7
        skaterpos[1]+=7
    elif keys[3] and (skaterpos[0] + skater.get_width() < width) :
        skaterpos[0]+=7
    elif (skaterpos[1] < (height - skater.get_height())) :
        skaterimg = skaterollie
        skaterpos[0]+=7
        skaterpos[1]+=7

    if pygame.time.get_ticks()>=gamelength:
        running=0
        exitcode=1
    if healthvalue<=0:
        running=0
        exitcode=0

# Win/lose display
if exitcode==0:
    # LOSER
    pygame.mixer.music.load('resources/audio/hell.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.font.init()
    font = pygame.font.Font(None, 47)
    #text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
    text = font.render("YOU SUCK, DUDE!! __ALL THE CATS ARE DEAD!!!! :(", True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    #textRect.centery = screen.get_rect().centery+24
    textRect.centery = 50
    #screen.blit(gameover, (0,0))
    screen.blit(text, textRect)
else:
    # WINNNER
    pygame.mixer.music.load('resources/audio/heaven.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.font.init()
    font = pygame.font.Font(None, 47)
    text = font.render("DAMN, DUDE, YOU RULE, LOTS OF CATS STILL ALIVE!!", True, (255,0,255))
    #text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    #textRect.centery = screen.get_rect().centery+24
    textRect.centery = 50
    #screen.blit(youwin, (0,0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
