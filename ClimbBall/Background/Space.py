import random

from ClimbBall.Background.IBackground import IBackground
from gameGlobals import GameGlobals
import pygame

class __Star__:
    def __init__(self):
        self.x = random.randint(0, GameGlobals.screen_width)
        self.y = random.randint(0, GameGlobals.screen_height)
        self.speed = random.uniform(0.1, 1)
        self.size = random.uniform(0.5, 2)
    
    def move(self):
        self.y += self.speed
        if self.y > GameGlobals.screen_height:
            self.y = 0
            self.x = random.randint(0, GameGlobals.screen_width)

    def draw(self):
        pygame.draw.circle(GameGlobals.screen, (255,255,255), (int(self.x), int(self.y)), int(self.size))

class Space(IBackground):
    def __init__(self):
        self.scorePointColor = (255,255,255)
        self.ballColor = (255, 255, 0)
        self.stars = [__Star__() for _ in range(200)]

    def draw(self):
        GameGlobals.screen.fill((0,0,0))

    # Update and draw stars
        for star in self.stars:
            star.move()
            star.draw()