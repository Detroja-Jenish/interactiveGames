import math
import random
from gameGlobals import GameGlobals
import pygame

class __Bullet__():
    def __init__(self,x,y,radius,color,speed_x,speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.accelration = 1

    def move(self):
        self.x += self.speed_x*self.accelration
        self.y += self.speed_y*self.accelration

        return self.y <= 0 or self.y >= GameGlobals.screen_height or self.x >= GameGlobals.screen_width or self.x <= 0
    
    def draw(self):
        pygame.draw.circle(GameGlobals.screen, self.color, (self.x, self.y), self.radius)

class Shooter():
    def __init__(self):
        self.x = 200
        self.y = GameGlobals.screen_height // 2
        self.radius = 50
        self.isBulletAlive = False;
        self.bullet_speed = 10
        self.shoot(math.atan2(0,1))

    def draw(self):
        pygame.draw.circle(GameGlobals.screen, (255,0,0), (self.x, self.y), self.radius)
        self.bullet.move()
        self.bullet.draw()

    def moveBullet(self):
        isOutBound = self.bullet.move()
        if isOutBound:
            self.isBulletAlive = False

    def shoot(self, angle):
        self.isBulletAlive = True
        self.bullet = __Bullet__(self.x,self.y,10, (0,255,0),math.cos(angle)*self.bullet_speed,math.sin(angle)*self.bullet_speed)
    
         