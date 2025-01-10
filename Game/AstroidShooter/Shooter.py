import math
import random
from gameGlobals import GameGlobals
import pygame
from os import path
from time import sleep
import threading
# bulletShootSound = pygame.mixer.Sound(path.abspath(path.dirname(path.dirname(path.abspath(__file__))))+'../../assets/sounds/bulletShoot.mp3')
bulletShootSound = pygame.mixer.Sound(path.abspath(path.dirname(path.dirname(path.abspath(__file__))))+'/../assets/sounds/bulletShoot.mp3')

class __Bullet__():
    def __init__(self,x,y,radius,color,speed_x,speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.accelration = 2
        self.isAlive = True
        bulletShootSound.play()

    def move(self):
        self.x += self.speed_x*self.accelration
        self.y += self.speed_y*self.accelration
        if self.y <= 0 or self.y >= GameGlobals.screen_height or self.x >= GameGlobals.screen_width or self.x <= 0:
            self.isAlive = False
        return self.y <= 0 or self.y >= GameGlobals.screen_height or self.x >= GameGlobals.screen_width or self.x <= 0
    
    def draw(self):
        pygame.draw.circle(GameGlobals.screen, self.color, (self.x, self.y), self.radius)

class Shooter():
    noOfBullet = 1
    continuesShots = 1
    isContinuousShot = False
    def __init__(self):
        self.x = 200
        self.y = GameGlobals.screen_height // 2
        self.radius = 50
        self.isBulletAlive = False;
        self.bullet_speed = 10
        self.bullets = []
        
        self.angle = 0

    def draw(self):
        pygame.draw.circle(GameGlobals.screen, (255,0,0), (self.x, self.y), self.radius)
        for bullet in self.bullets:
            bullet.draw()

    def moveBullet(self):
        for bullet in self.bullets:
            bullet.move()
        

    def shoot(self):
        threading.Thread(target=self.__shoot__, args=( Shooter.noOfBullet, Shooter.continuesShots,0.5), daemon=True).start()
        # try:
        #     angularDisplacement = (10*math.pi / 180)/(self.noOfBullet//2)
        # except Exception :
        #     angularDisplacement = 0
        # rightShift = angle
        # leftShift = angle

        # for _ in range(self.noOfBullet//2+1):
        #     self.bullets.append(__Bullet__(self.x,self.y,10, (0,255,0),math.cos(rightShift)*self.bullet_speed,math.sin(rightShift)*self.bullet_speed))
        #     if(rightShift != leftShift):
        #         self.bullets.append(__Bullet__(self.x,self.y,10, (0,255,0),math.cos(leftShift)*self.bullet_speed,math.sin(leftShift)*self.bullet_speed))
        #     rightShift += angularDisplacement
        #     leftShift -= angularDisplacement
    
    def __shoot__(self,noOfBullet,continuesShots,interval):
        try:
            angularDisplacement = (10*math.pi / 180)/(noOfBullet//2)
        except Exception :
            angularDisplacement = 0
        
        while(True):
            rightShift = self.angle
            leftShift = self.angle

            for _ in range(noOfBullet//2+1):
                self.bullets.append(__Bullet__(self.x,self.y,10, (0,255,0),math.cos(rightShift)*self.bullet_speed,math.sin(rightShift)*self.bullet_speed))
                if(rightShift != leftShift):
                    self.bullets.append(__Bullet__(self.x,self.y,10, (0,255,0),math.cos(leftShift)*self.bullet_speed,math.sin(leftShift)*self.bullet_speed))
                rightShift += angularDisplacement
                leftShift -= angularDisplacement
            if not Shooter.isContinuousShot:break
            sleep(interval)
    def clearBullet(self):
        for bullet in self.bullets:
            if not bullet.isAlive:
                self.bullets.remove(bullet)

    def isAllBulletsDead(self):
        return len(self.bullets) == 0
    
         