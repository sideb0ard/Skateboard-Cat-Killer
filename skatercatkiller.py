#!/usr/bin/env python
# coding=utf-8
# Music by Delroy Edwards - Slowed Down Funk - http://www.sloweddownfunk.net/
# my first version based on this kid's tutorial - http://www.raywenderlich.com/24252/beginning-game-programming-for-teens-with-python
# Then i made it more object oriented after reading this tutorial - http://ezide.com/games/writing-games.html
# Probably still remants of their code to be found in here

import pygame
from pygame.locals import *
import math
import random
import time

def Debug( msg ):
    print msg

DIRECTION_UP    = 0
DIRECTION_DOWN  = 1
DIRECTION_LEFT  = 2
DIRECTION_RIGHT = 3

WIN  = 1
LOSE = 0

SKATESPEED = 9
BACKGROUNDSPEED = 2
CATTIMER = 60

GAMELENGTH = 60000 # ms

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

class SkaterMoveEvent(Event):
    def __init__(self, direction, onoff):
        self.name = "Skater Move Request"
        self.direction = direction
        self.onoff = onoff

class HealthChangeEvent(Event):
    def __init__(self):
        self.name = "Health Change Request"
        self.value = random.randint(10,40)

class GameOverEvent(Event):
    def __init__(self, result):
        self.name = "Game Over Event"
        self.result = result

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
                        ev = SkaterMoveEvent(DIRECTION_UP, True)
                    elif event.key==K_LEFT:
                        ev = SkaterMoveEvent(DIRECTION_LEFT, True)
                    elif event.key==K_DOWN:
                        ev = SkaterMoveEvent(DIRECTION_DOWN, True)
                    elif event.key==K_RIGHT:
                        ev = SkaterMoveEvent(DIRECTION_RIGHT, True)
                if event.type == pygame.KEYUP:
                    if event.key==K_UP:
                        ev = SkaterMoveEvent(DIRECTION_UP, False)
                    elif event.key==K_LEFT:
                        ev = SkaterMoveEvent(DIRECTION_LEFT, False)
                    elif event.key==K_DOWN:
                        ev = SkaterMoveEvent(DIRECTION_DOWN, False)
                    elif event.key==K_RIGHT:
                        ev = SkaterMoveEvent(DIRECTION_RIGHT, False)
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

class Cat(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.runimg   = pygame.image.load("resources/images/cat_run.png")
        self.splatimg = pygame.image.load("resources/images/cat_splat.png")
        self.img = self.runimg
        self.wah = pygame.mixer.Sound("resources/audio/catsqueek.wav")
        self.wah.set_volume(0.65)
        self.speed = random.randint(7,15)
        self.position = [width, height - self.runimg.get_height()]
        self.splatcounter = 7

    def Notify(self, event):
        if isinstance(event,TickEvent):
            pass
            #print "MEOW! position %d " % self.position[0]


class Skater(pygame.sprite.Sprite):
    def __init__(self, evManager, group=None):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.rollimg  = pygame.image.load("resources/images/skater_roll.png")
        self.popimg   = pygame.image.load("resources/images/skater_pop.png")
        self.ollieimg = pygame.image.load("resources/images/skater_ollie.png")
        self.img = self.rollimg
        self.olliepop = pygame.mixer.Sound("resources/audio/olliepop.wav")
        self.olliepop.set_volume(10.95)
        self.ollieland = pygame.mixer.Sound("resources/audio/ollieland.wav")
        self.ollieland.set_volume(0.75)
        self.SOUNDON = True
        self.position = [10, height - self.rollimg.get_height()]
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False

    def Notify(self, event):
        if isinstance(event,SkaterMoveEvent):
            if event.direction == DIRECTION_UP:
                if event.onoff == True:
                    self.UP = True
                else:
                    self.UP = False
            elif event.direction == DIRECTION_DOWN:
                if event.onoff == True:
                    self.DOWN = True
                else:
                    self.DOWN = False
            elif event.direction == DIRECTION_LEFT:
                if event.onoff == True:
                    self.LEFT = True
                else:
                    self.LEFT = False
            elif event.direction == DIRECTION_RIGHT:
                if event.onoff == True:
                    self.RIGHT = True
                else:
                    self.RIGHT = False

        # SOUNDZ
        if self.SOUNDON == True:
            if (self.img == self.ollieimg or self.img == self.popimg) and (self.position[1] == height - self.rollimg.get_height()) :
                self.ollieland.play()
            if self.UP and (self.position[1] == height - self.rollimg.get_height()) and not (self.LEFT and self.position[0] <= 0):
                self.olliepop.play()

        # IMAGEZ and POSITION
        if (self.position[1] == (height - self.rollimg.get_height())) : # default position
            self.img = self.rollimg
        elif (self.position[1] <= 0):
            self.img = self.ollieimg # hit top, time for gravity to kick in

        if self.LEFT and (self.position[0] > 0) :
            self.position[0]-= SKATESPEED
        elif self.RIGHT and (self.position[0] + self.rollimg.get_width() < width):
            self.position[0]+= SKATESPEED

        if self.img == self.ollieimg: # Once your in ollie position, gravity takes hold and brings ye down
            self.position[1]+= SKATESPEED
            if self.position[0] > 0:
                self.position[0]+= 2

        if self.UP and self.img != self.ollieimg:
            self.img = self.popimg
            self.position[1]-= SKATESPEED
            if not self.LEFT and self.position[0] + self.popimg.get_width() < width:
                self.position[0]+= 7
            elif self.RIGHT and self.position[0] > 0:
                self.position[0]+= 2

        if not self.UP and self.img == self.popimg:
            self.img = self.ollieimg

class CountDownDisplay:
    def __init__(self,evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

class HealthBar:
    def __init__(self,evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.display = pygame.image.load("resources/images/healthbar.png")
        self.current    = pygame.image.load("resources/images/health.png")

        self.healthvalue = 194

    def Notify(self, event):
        if isinstance(event,HealthChangeEvent):
            self.healthvalue -= event.value
            print "Healthy! %d" % self.healthvalue

            if self.healthvalue<=0:
                event = GameOverEvent(LOSE)
                self.evManager.Post(event)

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

        self.skater = Skater(self.evManager)

        self.CatTimer = 100
        self.Catz = [ Cat(self.evManager) ]

        self.healthbar = HealthBar(self.evManager)

        #pygame.mixer.music.load('resources/audio/hoodlike.wav')
        pygame.mixer.music.load('resources/audio/longhood.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.25)

        self.GAMEON = True

    def Notify(self, event):
        if isinstance(event,GameOverEvent):
            self.GAMEON = False
            self.skater.SOUNDON = False
            if event.result == WIN:
                pygame.mixer.music.load('resources/audio/heaven.wav')
                pygame.mixer.music.play(-1, 0.0)
                pygame.font.init()
                font = pygame.font.Font(None, 47)
                text = font.render("DAMN, DUDE, YOU RULE, PLENTY OF RAMPAGIN CATS STILL ALIVE!!", True, (255,0,255))
                textRect = text.get_rect()
                textRect.centerx = self.window.get_rect().centerx
                textRect.centery = 50
                self.window.blit(text, textRect)
                #print pygame.time.get_ticks()
                #self.window.blit(text, textRect)
            else:
                pygame.mixer.music.load('resources/audio/hell.wav')
                pygame.mixer.music.play(-1, 0.0)
                pygame.font.init()
                font = pygame.font.Font(None, 47)
                text = font.render("YOU SUCK, DUDE!! __ SO MANY DEAD CATS !!!! :(", True, (255,0,0))
                textRect = text.get_rect()
                textRect.centerx = self.window.get_rect().centerx
                textRect.centery = 50
                self.window.blit(text, textRect)
            pygame.display.flip()

        if isinstance(event,TickEvent) and self.GAMEON == True:
            self.background.fill((0,0,0))
            self.window.blit(self.bgOne, (self.bgOne_x, 0))
            self.window.blit(self.bgTwo, (self.bgTwo_x, 0))

            self.window.blit(self.skater.img, self.skater.position)

            self.CatTimer-=1

            if self.CatTimer<=0:
                self.Catz.append( Cat(self.evManager) )
                self.CatTimer=random.randint(1,CATTIMER)
            index = 0
            for cat in self.Catz:

                if cat.position[0] < -140 or cat.splatcounter <= 0:
                    self.Catz.pop(index)

                if cat.img == cat.splatimg:
                    cat.splatcounter -= 1
                    cat.position[1] = height - cat.img.get_height()
                else:
                    cat.position[0] -= cat.speed

                if cat.img == cat.runimg:
                    catrect=pygame.Rect(cat.position[0],cat.position[1],(cat.runimg.get_width() - 180), (cat.runimg.get_height() - 180))
                    skaterect=pygame.Rect(self.skater.img.get_rect())
                    skaterect.left=self.skater.position[0] - 80
                    skaterect.top=self.skater.position[1] - 50

                    if catrect.colliderect(skaterect):
                        cat.wah.play()
                        cat.img = cat.splatimg
                        #self.Catz.pop(index)
                        #self.window.blit(cat.splatimg, cat.position)
                        event = HealthChangeEvent()
                        self.evManager.Post(event)

                index+=1

            for cat in self.Catz:
                self.window.blit(cat.img, cat.position)

            font = pygame.font.Font(None, 54)
            timertext = font.render(str((GAMELENGTH-pygame.time.get_ticks())/GAMELENGTH)+":"+str((GAMELENGTH-pygame.time.get_ticks())/1000%60).zfill(2), True, (255,255,255))
            textRect = timertext.get_rect()
            textRect.topright=[1100,5]
            self.window.blit(timertext, textRect) 

            self.window.blit(self.healthbar.display, (10,10))
            for val in range(self.healthbar.healthvalue):
                self.window.blit(self.healthbar.current, (val+13,13))


            self.bgOne_x -= BACKGROUNDSPEED
            self.bgTwo_x -= BACKGROUNDSPEED

            if self.bgOne_x <= -1 * self.bgOne.get_width():
                self.bgOne_x = self.bgTwo_x + self.bgTwo.get_width()
            if self.bgTwo_x <= -1 * self.bgTwo.get_width():
                self.bgTwo_x = self.bgOne_x + self.bgOne.get_width()

            pygame.display.flip()

        if pygame.time.get_ticks()>=GAMELENGTH and self.GAMEON == True:
            event = GameOverEvent(WIN)
            self.evManager.Post(event)

def main():
    evManager = EventManager()
    keybd = KeyboardController(evManager)
    spinner = CPUSpinnerController(evManager)
    pygameView = PygameView(evManager)
    spinner.Run()

if __name__=="__main__":
    main()
