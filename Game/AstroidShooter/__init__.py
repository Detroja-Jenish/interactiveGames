import math

import numpy as np
from Camera import Camera
from EventHandler import Event, EventHandler
from Game.AstroidShooter.Background.Space import Space
from Game.AstroidShooter.Shooter import Shooter
from Game.AstroidShooter.astroids import AstroidHandler
from Game.AstroidShooter.powerUpHandler import PowerUpHandler
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
        self.powerUpHandler = PowerUpHandler()
        self.eventHandler.registerEvent("quit",Event(pygame.QUIT,lambda _ : self.astroidHandler.stopGenratingAstroids() ,lambda _ : GameGlobals.doQuit()))
        self.eventHandler.registerEvent("quit_by_press_q",Event( pygame.KEYDOWN,lambda _ : self.astroidHandler.stopGenratingAstroids(), lambda _ : GameGlobals.doQuit(), condition = lambda e : e.key == pygame.K_q))

    def play(self):
        Camera.readFrame()
        if not Camera.ret:
            raise "error occurred"
        results = PoseEstimater.detectPersons(Camera.frame)
        # frame_surface = pygame.surfarray.make_surface(np.transpose(Camera.frame, (1, 0, 2)))
        # GameGlobals.screen.blit(frame_surface, (0, 0))
        self.background.draw()
        
        self.astroidHandler.moveAstroids()
        self.shooter.moveBullet()
        self.astroidHandler.detectCollisonWithAstroids(self.shooter.bullets)
        
        if results and results[0].rightHand:
            dx = (results[0].rightHand.point2[0] - results[0].rightHand.point1[0])*GameGlobals.screen_width
            dy = (results[0].rightHand.point2[1] - results[0].rightHand.point1[1])*GameGlobals.screen_height
            angle = math.atan2(dy,dx)
            self.shooter.angle = angle
            self.shooter.x = results[0].rightHand.center_x
            self.shooter.y = results[0].rightHand.center_y
        if self.shooter.isAllBulletsDead() and results and results[0].rightHand:
            self.shooter.shoot( )

        if results and results[0].rightHand:
            pygame.draw.circle(GameGlobals.screen,(0,0,255), (results[0].rightHand.center_x, results[0].rightHand.center_y), results[0].rightHand.radius)
            self.powerUpHandler.detectColide(results[0].rightHand)
        
        self.shooter.clearBullet()
        self.powerUpHandler.clearPowerUp()

        self.shooter.draw()
        self.astroidHandler.drawAstroids()
        self.powerUpHandler.draw()
        pygame.display.flip()
        self.eventHandler.checkEventOccurnce()
