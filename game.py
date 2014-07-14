#!/usr/bin/env python
# code based up following the pygame tutorial here -
# http://www.raywenderlich.com/24252/beginning-game-programming-for-teens-with-python

import pygame
from pygame.locals import *
import math
import random

#2
pygame.init()
width,height = 1140, 480
screen = pygame.display.set_mode((width,height))

keys = [False, False, False, False]

#acc=[0,0]
#arrows=[]

pygame.mixer.init()

#3
skater = pygame.image.load("resources/images/skater.png")
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

grass = pygame.image.load("resources/images/grass.png")

healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")

gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# 3.1 - Load audio
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
    cattimer-=1
    screen.fill(0)

    for x in range(width/grass.get_width()+1):
        for y in range(height/grass.get_height()+1):
            screen.blit(grass,(x*100,y*100))
            print "TIMER: ", (pygame.time.get_ticks() % grass.get_width())

    screen.blit(skaterimg, skaterpos)
    if cattimer==0:
        catguys.append([980, height - catrun.get_height()])
        cattimer=random.randint(0,130)
    index=0
    for catguy in catguys:
        if catguy[0]< -140:
            catguys.pop(index)
        #catguy[0]-=9
        catguy[0]-=10
        catrect=pygame.Rect(0, 0, (catguyimg.get_width() - 180), (catguyimg.get_height() - 180))
        catrect.top=catguy[1]
        print "CatguyTOP %d" % (catguy[1], )
        catrect.left=catguy[0]
        print "CatguyLEFT %d" % (catguy[0], )
        if catrect.left<0:
            catguys.pop(index)
        index1=0
        skaterect=pygame.Rect(skater.get_rect())
        skaterect.left=skaterpos[0] - 80
        skaterect.top=skaterpos[1] - 50
        if catrect.colliderect(skaterect):
           catwah.play()
           #acc[0]+=1
           catguys.pop(index)
           screen.blit(catsplat, catguy)
           healthvalue -= random.randint(10,40)
           index1+=1
        index+=1
    for catguy in catguys:
        screen.blit(catguyimg, catguy)

    font = pygame.font.Font(None, 24)
    survivedtext = font.render(str((60000-pygame.time.get_ticks())/60000)+":"+str((60000-pygame.time.get_ticks())/1000%60).zfill(2), True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright=[635,5]
    screen.blit(survivedtext, textRect) 
    # 6.5 - Draw health bar
    screen.blit(healthbar, (5,5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1+8,8))

    #7
    pygame.display.flip()
    #8
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
        #if event.type==pygame.MOUSEBUTTONDOWN:
        #    # section 8, after if event.type==pygame.MOUSEBUTTONDOWN:
        #    #shoot.play()
        #    position=pygame.mouse.get_pos()
        #    acc[1]+=1
        #    arrows.append([math.atan2(position[1]-(skaterpos1[1]+32),position[0]-(skaterpos1[0]+26)),skaterpos1[0]+32,skaterpos1[1]+32])
    #9
    print "skaterpos[1] is %d and height minus skater height is %d" % (skaterpos[1], height - skater.get_height())
    #if (skaterpos[1] == (height - skater.get_height())) and (skaterpos[0] + skater.get_width() < width) :
    if skaterimg == skaterollie and (skaterpos[1] == height - skater.get_height()) :
        ollieland.play()
    if (skaterpos[1] == (height - skater.get_height())) : # and (skaterpos[0] + skater.get_width() < width) :
        skaterimg = skater
    if keys[0] and (skaterpos[1] == height - skater.get_height()) :
        olliepop.play()
    if keys[0] and (skaterpos[1] > 1) and skaterimg != skaterollie:
        skaterimg = skaterpop
        #olliepop.play()
        skaterpos[0]+=7
        skaterpos[1]-=7
    elif keys[2] and (skaterpos[1] + skater.get_height() < height) :
        #print "skaterpos[1] is %d and skater height is %d" % (skaterpos[1], skater.get_height())
        skaterpos[1]+=7
    elif keys[1] and (skaterpos[0] > 0 ) and (skaterpos[1] + skater.get_height() < height ) and skaterimg == skaterollie: 
        skaterpos[0]-=7
        skaterpos[1]+=7
    elif keys[1] and (skaterpos[0] > 0 ):
        print "skaterpos[0] is %d and skater width is %d" % (skaterpos[0], skater.get_width())
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

    if pygame.time.get_ticks()>=60000:
        running=0
        exitcode=1
    if healthvalue<=0:
        running=0
        exitcode=0

# Win/lose display
if exitcode==0:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    #text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
    text = font.render("THAT SUCKED, DUDE...!", True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("DAMN, DUDE, YOU THRASH BETTER THAN GONZ!!", True, (255,0,0))
    #text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
