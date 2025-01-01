import math
from gameGlobals import GameGlobals
import random
import pygame
import time
from threading import Thread
class __Astroid__:
    def __init__(self, x, y, radius, color, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.accelration = 1
    
    def move(self):
        self.x -= self.speed_x*self.accelration
        self.y -= self.speed_y*self.accelration
        return self.x + self.radius <= 0
    
    def draw(self):
        pygame.draw.circle(GameGlobals.screen, self.color, (self.x, self.y), self.radius) 

    def isCollideBullet(self,bullet):
        distance = math.sqrt((self.x - bullet.x)**2 + (self.y - bullet.y)**2)

        return distance <= self.radius + bullet.radius
           
        


class AstroidHandler:
    def __init__(self):
        self.astroids = []
        self.needToGenrateAstroids = True
        Thread(target=self.__genrateAstroids__).start()
    
    def stopGenratingAstroids(self):
        self.needToGenrateAstroids = False
    def __genrateAstroids__(self):
        while self.needToGenrateAstroids:
            self.astroids.extend([
            __Astroid__(
                GameGlobals.screen_width, 
                random.randint(100, GameGlobals.screen_height - 100),
                random.randint(20,100),(150,75,0),
                random.randint(1,4),
                0
            )
            for _ in range(0,random.randint(0,4))])
            time.sleep(random.randint(2,7))

    def moveAstroids(self):
        for astroid in self.astroids:
            outOfBound = astroid.move()
            if outOfBound :
                self.astroids.remove(astroid)

    def detectCollisonWithAstroids(self,bullet):
        for astroid in self.astroids:
            if astroid.isCollideBullet(bullet):
                self.astroids.remove(astroid)
                return True
    
    def drawAstroids(self):
        for astroid in self.astroids:
            astroid.draw()