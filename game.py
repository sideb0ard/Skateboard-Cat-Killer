#!/usr/bin/env python
# coding=utf-8

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
    def __init__(self, direction, onoff):
        self.name = "Skater Move Request"
        self.direction = direction
        self.onoff = onoff

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
        if isinstance(event, SkaterMove):
            print "GOT EVENT..."
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
                        ev = SkaterMove(DIRECTION_UP, True)
                    elif event.key==K_LEFT:
                        ev = SkaterMove(DIRECTION_LEFT, True)
                    elif event.key==K_DOWN:
                        ev = SkaterMove(DIRECTION_DOWN, True)
                    elif event.key==K_RIGHT:
                        ev = SkaterMove(DIRECTION_RIGHT, True)
                if event.type == pygame.KEYUP:
                    if event.key==K_UP:
                        ev = SkaterMove(DIRECTION_UP, False)
                    elif event.key==K_LEFT:
                        ev = SkaterMove(DIRECTION_LEFT, False)
                    elif event.key==K_DOWN:
                        ev = SkaterMove(DIRECTION_DOWN, False)
                    elif event.key==K_RIGHT:
                        ev = SkaterMove(DIRECTION_RIGHT, False)
                if ev:
                    print "EVENT! KEEEEYYYYZZZZ"
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
    def __init__(self, evManager, group=None):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.rollimg  = pygame.image.load("resources/images/skater_roll.png")
        self.popimg   = pygame.image.load("resources/images/skater_pop.png")
        self.ollieimg = pygame.image.load("resources/images/skater_ollie.png")
        self.img = self.rollimg
        self.position = [10, height - self.rollimg.get_height()]
        self.SPEED = 9
        self.UP = False
        self.DOWN = False
        self.LEFT = False
        self.RIGHT = False

    def Notify(self, event):
        print "EVENTYAAAASSS!"
        #if self.img == self.ollieimg and (self.position[1] == height - self.rollimg.get_height()) :
        #    self.ollieland.play()
        if isinstance(event,SkaterMove):
            print "SKATEMOVEYAAAASSS!"
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

        #if self.img == self.ollieimg and (self.position[1] == height - self.rollimg.get_height()) :
        #    ollieland.play()
        if (self.position[1] == (height - self.rollimg.get_height())) : # and (self.position[0] + skater.get_width() < width) :
            self.img = self.rollimg
        if self.UP and (self.position[1] == height - self.rollimg.get_height()) :
        #    #olliepop.play()
            print "OLLIE SOUND"
        if self.UP and (self.position[1] > 1) and self.img != self.ollieimg:
            self.img = self.popimg
            self.position[0]+=7
            self.position[1]-=7
        elif self.RIGHT and (self.position[1] + self.rollimg.get_height() < height) :
            self.position[1]+=7
        elif self.DOWN and (self.position[0] > 0 ) and (self.position[1] + self.rollimg.get_height() < height ) and self.img == self.ollieimg: 
            self.position[0]-=7
            self.position[1]+=7
        elif self.DOWN and (self.position[0] > 0 ):
            self.position[0]-=7
        elif self.LEFT and (self.position[0] + self.rollimg.get_width() < width) and (self.img == self.popimg) :
            self.img = self.ollieimg
            self.position[0]+=7
            self.position[1]+=7
        elif self.LEFT and (self.position[0] + self.rollimg.get_width() < width) :
            self.position[0]+=7
        elif (self.position[1] < (height - self.rollimg.get_height())) :
            self.img = self.ollieimg
            self.position[0]+=7
            self.position[1]+=7


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

        self.skater = Skater(evManager)

    def Notify(self, event):
        if isinstance(event,TickEvent):
            self.background.fill((0,0,0))
            self.window.blit(self.bgOne, (self.bgOne_x, 0))
            self.window.blit(self.bgTwo, (self.bgTwo_x, 0))

            self.window.blit(self.skater.img, self.skater.position)

            pygame.display.flip()

            self.bgOne_x -= 2
            self.bgTwo_x -= 2

            if self.bgOne_x <= -1 * self.bgOne.get_width():
                self.bgOne_x = self.bgTwo_x + self.bgTwo.get_width()
            if self.bgTwo_x <= -1 * self.bgTwo.get_width():
                self.bgTwo_x = self.bgOne_x + self.bgOne.get_width()

def main():
    evManager = EventManager()
    keybd = KeyboardController(evManager)
    spinner = CPUSpinnerController(evManager)
    pygameView = PygameView(evManager)
    spinner.Run()

if __name__=="__main__":
    main()
