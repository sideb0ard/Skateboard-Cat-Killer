#!/usr/bin/env python
# coding=utf-8

import pygame
from pygame.locals import *
import math
import random
import time

def Debug( msg ):
    print msg

DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

width,height = 1140, 480

class Event:
    def __init__(self):
        self.name = "Generic Event"

class TickEvent(Event):
        def __init__(self):
                self.name = "CPU Tick Event"

class QuitEvent(Event):
        def __init__(self):
                self.name = "Program Quit Event"

class GameStartedEvent(Event):
        def __init__(self, game):
                self.name = "Game Started Event"
                self.game = game

class SkaterMove(Event):
        def __init__(self, direction):
                self.name = "Skater Move Request"
                self.direction = direction

class EventManager:
    def __init__(self):
        from weakref import WeakKeyDictionary
        self.listeners = WeakKeyDictionary()
    def RegisterListener(self, listener):
        self.listeners[listener] = 1
    def UnregisterListener(self, listener):
        if listener in self.listeners.keys():
            del self.listeners[ listener ]
    def Post(self, event):
        for listener in self.listeners.keys():
            listener.Notify( event )

class KeyboardController:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

    def Notify(self,event):
        if isinstance(event,TickEvent):
            for event in pygame.event.get():
                ev = None
                if event.type==pygame.QUIT:
                    ev = QuitEvent()
                if event.type == pygame.KEYDOWN:
                    if event.key==K_ESCAPE:
                        ev = QuitEvent()
                    elif event.key==K_UP:
                        direction = DIRECTION_UP
                        ev = SkaterMove(direction)
                    elif event.key==K_LEFT:
                        direction = DIRECTION_LEFT
                        ev = SkaterMove(direction)
                    elif event.key==K_DOWN:
                        direction = DIRECTION_DOWN
                        ev = SkaterMove(direction)
                    elif event.key==K_RIGHT:
                        direction = DIRECTION_RIGHT
                        ev = SkaterMove(direction)
                if ev:
                    self.evManager.Post(ev)

class CPUSpinnerController:
    def __init__(self,evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.keepGoing = True
    def Run(self):
        while self.keepGoing:
            event = TickEvent()
            self.evManager.Post(event)
    def Notify(self,event):
        if isinstance(event,QuitEvent):
            self.keepGoing = False

#class Cat(pygame.sprite.Sprite):
#    runimg   = pygame.image.load("resources/images/cat_run.png")
#    splatimg = pygame.image.load("resources/images/cat_splat.png")
#
#    def __init__(self, position):
#        self.position = position
#
#    catguyimg1 = catrun
#    catguyimg=catguyimg1

class CatSprite(pygame.sprite.Sprite):
        def __init__(self, sector, group=None):
                pygame.sprite.Sprite.__init__(self, group)
                self.image = pygame.Surface( (128,128) )
                self.image.fill( (0,255,128) )

                self.sector = sector

class Skater(pygame.sprite.Sprite):
        def __init__(self, group=None):
                self.rollimg  = pygame.image.load("resources/images/skater_roll.png")
                self.popimg   = pygame.image.load("resources/images/skater_pop.png")
                self.ollieimg = pygame.image.load("resources/images/skater_ollie.png")
                self.img = self.rolling
                self.position = [10, height - roll.get_height()]
                self.SPEED = 9

        def Notify(self, event):
                if self.img == self.ollieimg and (self.position[1] == height - self.rollimg.get_height()) :
                        self.ollieland.play()
                if isinstance(event,SkaterMove):


class HealthBar:
    def __init__(self,evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.healthbar = pygame.image.load("resources/images/healthbar.png")
        self.health    = pygame.image.load("resources/images/health.png")


class PygameView:
    def __init__(self,evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        pygame.init()
        self.window = pygame.display.set_mode( (width, height) )
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((0,0,0))

        self.bgOne = pygame.image.load("resources/images/buildingz1.png")
        self.bgTwo = pygame.image.load("resources/images/buildingz2.png")

        self.bgOne_x = 0
        self.bgTwo_x = self.bgOne.get_width()

        pygame.display.set_caption('SKATEB0ARD CAT KILLER')
        font = pygame.font.Font(None,30)
        text = """Press SPACE BAR to start"""
        textImg = font.render(text, 1, (255,0,0))

    def Notify(self, event):
        if isinstance(event,TickEvent):
            self.background.fill((0,0,0))
            self.window.blit(self.bgOne, (self.bgOne_x, 0))
            self.window.blit(self.bgTwo, (self.bgTwo_x, 0))

            pygame.display.flip()

            self.bgOne_x -= 2
            self.bgTwo_x -= 2

            if self.bgOne_x <= -1 * self.bgOne.get_width():
                self.bgOne_x = self.bgTwo_x + self.bgTwo.get_width()
            if self.bgTwo_x <= -1 * self.bgTwo.get_width():
                self.bgTwo_x = self.bgOne_x + self.bgOne.get_width()

#def skatejamz():
#
#
#
#    gamelength = 60000 # ms
#    keys = [False, False, False, False]
#
#    pygame.mixer.init()
#
#    healthvalue=194
#
#    cattimer=100
#    cattimer1=0
#    catguys=[[1140, height - catrun.get_height() ]]
#
#    skater = Skater("tony")
#
#    bgOne = pygame.image.load("resources/images/buildingz1.png")
#    bgTwo = pygame.image.load("resources/images/buildingz2.png")
#    bgOne_x = 0
#    bgTwo_x = bgOne.get_width()
#
#    healthbar = pygame.image.load("resources/images/healthbar.png")
#    health = pygame.image.load("resources/images/health.png")
#
#    # Load audio
#    olliepop = pygame.mixer.Sound("resources/audio/olliepop.wav")
#    olliepop.set_volume(0.75)
#    ollieland = pygame.mixer.Sound("resources/audio/ollieland.wav")
#    ollieland.set_volume(0.75)
#
#    catwah = pygame.mixer.Sound("resources/audio/catsqueek.wav")
#    catwah.set_volume(0.65)
#
#    #pygame.mixer.music.load('resources/audio/bass.wav')
#    pygame.mixer.music.load('resources/audio/hoodlike.wav')
#    pygame.mixer.music.play(-1, 0.0)
#    pygame.mixer.music.set_volume(0.25)
#
#    catspeeds = {}
#
#    running = 1
#    exitcode = 0
#    while running:
#        # print pygame.font.get_fonts()
#        cattimer-=1
#        screen.fill(0)
#
#        screen.blit(bgOne, (bgOne_x, 0))
#        screen.blit(bgTwo, (bgTwo_x, 0))
#
#        screen.blit(skaterimg, skaterpos)
#        if cattimer==0:
#            speed=random.randint(1,10)
#            #print "Speed:" , speed
#            catguys.append([980, height - catrun.get_height()])
#            catspeeds[len(catguys)-1] = speed
#            cattimer=random.randint(0,100)
#
#        index=0
#        for catguy in catguys:
#            if catguy[0]< -140:
#                catguys.pop(index)
#            # catguy speed ##
#            speedindex = catguys.index(catguy)
#            print len(catspeeds) #[speedindex]
#            catguy[0]-=9
#            #catguy[0]-=catguy[2] # 2 is speed
#            catrect=pygame.Rect(0, 0, (catguyimg.get_width() - 180), (catguyimg.get_height() - 180))
#            catrect.top=catguy[1]
#            catrect.left=catguy[0]
#            if catrect.left<0:
#                catguys.pop(index)
#            index1=0
#            skaterect=pygame.Rect(skater.get_rect())
#            skaterect.left=skaterpos[0] - 80
#            skaterect.top=skaterpos[1] - 50
#            if catrect.colliderect(skaterect):
#               catwah.play()
#               catguys.pop(index)
#               screen.blit(catsplat, catguy)
#               healthvalue -= random.randint(10,40)
#               index1+=1
#            index+=1
#        for catguy in catguys:
#            screen.blit(catguyimg, catguy)
#
#        font = pygame.font.Font(None, 54)
#        survivedtext = font.render(str((gamelength-pygame.time.get_ticks())/gamelength)+":"+str((gamelength-pygame.time.get_ticks())/1000%60).zfill(2), True, (255,255,255))
#        textRect = survivedtext.get_rect()
#        textRect.topright=[1100,5]
#        screen.blit(survivedtext, textRect) 
#        # 6.5 - Draw health bar
#        screen.blit(healthbar, (5,5))
#        for health1 in range(healthvalue):
#            screen.blit(health, (health1+8,8))
#
#        pygame.display.flip()
#
#        bgOne_x -= 1
#        bgTwo_x -= 1
#
#        if bgOne_x <= -1 * bgOne.get_width():
#            bgOne_x = bgTwo_x + bgTwo.get_width()
#        if bgTwo_x <= -1 * bgTwo.get_width():
#            bgTwo_x = bgOne_x + bgOne.get_width()
#
#
#        if skaterimg == skaterollie and (skaterpos[1] == height - skater.get_height()) :
#            ollieland.play()
#        if (skaterpos[1] == (height - skater.get_height())) : # and (skaterpos[0] + skater.get_width() < width) :
#            skaterimg = skater
#        if keys[0] and (skaterpos[1] == height - skater.get_height()) :
#            olliepop.play()
#        if keys[0] and (skaterpos[1] > 1) and skaterimg != skaterollie:
#            skaterimg = skaterpop
#            skaterpos[0]+=7
#            skaterpos[1]-=7
#        elif keys[2] and (skaterpos[1] + skater.get_height() < height) :
#            skaterpos[1]+=7
#        elif keys[1] and (skaterpos[0] > 0 ) and (skaterpos[1] + skater.get_height() < height ) and skaterimg == skaterollie: 
#            skaterpos[0]-=7
#            skaterpos[1]+=7
#        elif keys[1] and (skaterpos[0] > 0 ):
#            skaterpos[0]-=7
#        elif keys[3] and (skaterpos[0] + skater.get_width() < width) and (skaterimg == skaterpop) :
#            skaterimg = skaterollie
#            skaterpos[0]+=7
#            skaterpos[1]+=7
#        elif keys[3] and (skaterpos[0] + skater.get_width() < width) :
#            skaterpos[0]+=7
#        elif (skaterpos[1] < (height - skater.get_height())) :
#            skaterimg = skaterollie
#            skaterpos[0]+=7
#            skaterpos[1]+=7
#
#        if pygame.time.get_ticks()>=gamelength:
#            running=0
#            exitcode=1
#        if healthvalue<=0:
#            running=0
#            exitcode=0
#
#    # Win/lose display
#    if exitcode==0:
#        # LOSER
#        pygame.mixer.music.load('resources/audio/hell.wav')
#        pygame.mixer.music.play(-1, 0.0)
#        pygame.font.init()
#        font = pygame.font.Font(None, 47)
#        #text = font.render("Accuracy: "+str(accuracy)+"%", True, (255,0,0))
#        text = font.render("YOU SUCK, DUDE!! __ALL THE CATS ARE DEAD!!!! :(", True, (255,0,0))
#        textRect = text.get_rect()
#        textRect.centerx = screen.get_rect().centerx
#        #textRect.centery = screen.get_rect().centery+24
#        textRect.centery = 50
#        #screen.blit(gameover, (0,0))
#        screen.blit(text, textRect)
#        time.sleep(5)
#        exit(0)
#    else:
#        # WINNNER
#        pygame.mixer.music.load('resources/audio/heaven.wav')
#        pygame.mixer.music.play(-1, 0.0)
#        pygame.font.init()
#        font = pygame.font.Font(None, 47)
#        text = font.render("DAMN, DUDE, YOU RULE, LOTS OF CATS STILL ALIVE!!", True, (255,0,255))
#        #text = font.render("Accuracy: "+str(accuracy)+"%", True, (0,255,0))
#        textRect = text.get_rect()
#        textRect.centerx = screen.get_rect().centerx
#        #textRect.centery = screen.get_rect().centery+24
#        textRect.centery = 50
#        #screen.blit(youwin, (0,0))
#        screen.blit(text, textRect)
#        time.sleep(5)
#        exit(0)
#    while 1:
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                pygame.quit()
#                exit(0)
#        pygame.display.flip()


def main():
    evManager = EventManager()
    keybd = KeyboardController(evManager)
    spinner = CPUSpinnerController(evManager)
    pygameView = PygameView(evManager)
    spinner.Run()

if __name__=="__main__":
    main()
