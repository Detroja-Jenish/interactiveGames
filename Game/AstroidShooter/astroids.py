import math
from gameGlobals import GameGlobals
import random
import pygame
import time
from threading import Thread
from utils.getPersistentPath import getPersistentPath

images =[ 
    pygame.image.load(getPersistentPath("assets/images/Meteors/Meteor_01.png")),
    pygame.image.load(getPersistentPath("assets/images/Meteors/Meteor_03.png")),
    pygame.image.load(getPersistentPath("assets/images/Meteors/Meteor_05.png")),
    pygame.image.load(getPersistentPath("assets/images/Meteors/Meteor_07.png")),
    pygame.image.load(getPersistentPath("assets/images/Meteors/Meteor_10.png"))
]
explosionSound = pygame.mixer.Sound(getPersistentPath("assets/sounds/explosion.wav"))
class __Astroid__:
    accelration = 1;
    def __init__(self, x, y, radius, color, speed_x, speed_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.imageID = random.randint(0,4)
    
    def move(self):
        self.x -= self.speed_x*__Astroid__.accelration
        self.y -= self.speed_y*__Astroid__.accelration
        return self.x + self.radius <= 0
    
    def draw(self):
        resized_image = pygame.transform.scale(images[self.imageID], (self.radius*2, self.radius*2))
        image_rect = resized_image.get_rect()
        image_rect.center = (self.x,self.y)
        # pygame.draw.circle(GameGlobals.screen, self.color, (self.x, self.y), self.radius) 
        pygame.draw.circle(GameGlobals.screen, (0,0,0,0), (self.x, self.y), self.radius) 
        GameGlobals.screen.blit(resized_image, image_rect)

    def isCollideBullet(self,bullet):
        distance = math.sqrt((self.x - bullet.x)**2 + (self.y - bullet.y)**2)

        return distance <= self.radius + bullet.radius
           
        


class AstroidHandler:
    def __init__(self):
        self.astroids = []
        self.needToGenrateAstroids = True
        Thread(target=self.__genrateAstroids__,daemon=True).start()
    
    def stopGenratingAstroids(self):
        self.needToGenrateAstroids = False
    def __genrateAstroids__(self):
        while self.needToGenrateAstroids:
            self.astroids.extend([
            __Astroid__(
                GameGlobals.screen_width, 
                random.randint(100, GameGlobals.screen_height - 100),
                random.randint(20,50),
                (150,75,0),
                random.randint(1,4),
                0
            )
            for _ in range(0,random.randint(0,4))])
            time.sleep(random.randint(3,8))

    def moveAstroids(self):
        for astroid in self.astroids:
            outOfBound = astroid.move()
            if outOfBound :
                self.astroids.remove(astroid)

    def detectCollisonWithAstroids(self,bullets):
        flag = False
        for astroid in self.astroids:
            for bullet in bullets:
                if astroid.isCollideBullet(bullet):
                    bullets.remove(bullet)
                    try:self.astroids.remove(astroid)
                    except Exception as e: pass

                    explosionSound.play()
        return flag
    
    def drawAstroids(self):
        for astroid in self.astroids:
            astroid.draw()