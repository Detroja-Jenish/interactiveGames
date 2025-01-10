from math import sqrt
from random import choice, randint
import threading
from time import sleep
from abc import ABC, abstractmethod
from Game.AstroidShooter.Shooter import Shooter
from Game.AstroidShooter.astroids import __Astroid__
from gameGlobals import GameGlobals
import pygame

class IPowerUp(ABC):
    @abstractmethod
    def run(self):
        pass

class Freeze(IPowerUp):
    def __init__(self):
        self.color = (255,255,0)
        self.isFinished = False
    def run(self):
        while __Astroid__.accelration!=1:
            pass
        __Astroid__.accelration = 0;
        sleep(5)
        __Astroid__.accelration = 1;
        self.isFinished = True

class SlowDown(IPowerUp):
    def __init__(self):
        self.color = (255,0,255)
        self.isFinished = False
    def run(self):
        while __Astroid__.accelration != 1:
            pass
        __Astroid__.accelration = 0.3;
        sleep(5)
        __Astroid__.accelration = 1;
        self.isFinished = True

class ThreeShots:
    def __init__(self):
        self.color = (0,255,255)
        self.isFinished = False
    def run(self):
        while Shooter.noOfBullet > 1:
            pass
        Shooter.noOfBullet = 3;
        sleep(60)
        Shooter.noOfBullet = 1;
        self.isFinished = True

class ContinuesShots:
    def __init__(self):
        self.color = (50,110,255)
        self.isFinished = False
    def run(self):
        while Shooter.isContinuousShot:
            pass
        Shooter.isContinuousShot = True;
        sleep(6)
        Shooter.isContinuousShot = False;
        self.isFinished = True

class PowerUp:
    def __init__(self,powerUp):
        self.powerUp = powerUp()
        self.center_x = randint(100, GameGlobals.screen_width-100)
        self.center_y = randint(100, GameGlobals.screen_height-100)
        self.radius = 25
        self.bounce = randint(0,10)
        self.direction = choice([-1,1])
        self.isActivated = False;
    
    def detectColide(self,paddle):
        if not self.isActivated:
            distance = sqrt((self.center_x - paddle.center_x)**2 + (self.center_y - paddle.center_y)**2)
            if distance <= self.radius + paddle.radius:
                threading.Thread(target=self.powerUp.run, daemon=True).start()
                self.isActivated = True
    
    def draw(self):
        if not self.isActivated:
            self.bounce += self.direction
            if self.bounce >= 10:
                self.direction = -1
            elif self.bounce <= -10:
                self.direction = 1
            pygame.draw.circle(GameGlobals.screen,self.powerUp.color, (self.center_x, self.center_y + self.bounce), self.radius)

class PowerUpHandler:
    def __init__(self):
        self.powerUpList = [Freeze,SlowDown,ThreeShots,ContinuesShots]
        self.powerUps = []
        threading.Thread(target=self.genratePowerUp, daemon=True).start()
    
    def genratePowerUp(self):
        while True:
            if len(self.powerUps) < 2  and randint(0,100) < 33:
                self.powerUps.append(PowerUp(choice(self.powerUpList)))
            sleep(3)
    
    def detectColide(self,paddle):
        for powerUp in self.powerUps:
            powerUp.detectColide(paddle)
            
    def clearPowerUp(self):
        for powerUp in self.powerUps:
            if powerUp.isActivated and powerUp.powerUp.isFinished:
                self.powerUps.remove(powerUp)
        
    def draw(self):
        for powerUp in self.powerUps:
            powerUp.draw()
        # self.powerUps
            

