import math
from Camera import Camera
from EventHandler import Event, EventHandler
from Game.AstroidShooter.Background.Space import Space
from Game.AstroidShooter.Shooter import Shooter
from Game.AstroidShooter.astroids import AstroidHandler
from PoseEstimater import PoseEstimater
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
        results = PoseEstimater.detectHand(Camera.frame)
        self.background.draw()
        
        self.astroidHandler.moveAstroids()
        self.shooter.moveBullet()
        if (self.astroidHandler.detectCollisonWithAstroids(self.shooter.bullet) or (not self.shooter.isBulletAlive)) and results and results[0].rightHand:
            dx = (results[0].rightHand.point2[0] - results[0].rightHand.point1[0])*GameGlobals.screen_width
            dy = (results[0].rightHand.point2[1] - results[0].rightHand.point1[1])*GameGlobals.screen_height
            angle = math.atan2(dy,dx)
            self.shooter.shoot( angle )
        self.shooter.draw()
        self.astroidHandler.drawAstroids()
        pygame.display.flip()
        self.eventHandler.checkEventOccurnce()

# color,x,y,width,height, speed,target_x,target_y