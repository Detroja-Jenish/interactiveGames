import math
from Camera import Camera
from EventHandler import Event, EventHandler
from Game.AstroidShooter.Shooter import Shooter
from Game.AstroidShooter.astroids import AstroidHandler
from Game.ClimbBall.Background.Space import Space
from HandDetection import HandDetection
from gameGlobals import GameGlobals
import pygame

class AstroidShooter:
    def __init__(self):
        self.count = 0
        self.background = Space()
        self.shooter : Shooter = Shooter()
        self.eventHandler = EventHandler()
        self.astroidHandler = AstroidHandler()
        self.eventHandler.registerEvent("quit",Event(pygame.QUIT,lambda _ : self.astroidHandler.stopGenratingAstroids() ,lambda _ : GameGlobals.doQuit()))
        self.eventHandler.registerEvent("quit_by_press_q",Event( pygame.KEYDOWN,lambda _ : self.astroidHandler.stopGenratingAstroids(), lambda _ : GameGlobals.doQuit(), condition = lambda e : e.key == pygame.K_q))

    def play(self):
        Camera.readFrame()
        if not Camera.ret:
            raise "error occurred"
        results = HandDetection.detectHand(Camera.frame)
        self.background.draw()
        
        self.astroidHandler.moveAstroids()
        self.shooter.moveBullet()
        if self.astroidHandler.detectCollisonWithAstroids(self.shooter.bullet) or (not self.shooter.isBulletAlive):
            if results:
                dx = (results[0].point2.x - results[0].point1.x)*GameGlobals.screen_width
                dy = (results[0].point2.y - results[0].point1.y)*GameGlobals.screen_height
                angle = math.atan2(dy,dx)
            self.shooter.shoot( angle if results else math.atan2(1,1))
        self.shooter.draw()
        self.astroidHandler.drawAstroids()
        pygame.display.flip()
        self.eventHandler.checkEventOccurnce()

# color,x,y,width,height, speed,target_x,target_y