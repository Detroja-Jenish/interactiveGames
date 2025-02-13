from os import path
import time
from Camera import Camera
from EventHandler import Event, EventHandler
from Game.ClimbBall.Background.BlueOrangeGradient import BlueOrangeGradient
from PoseEstimater import PoseEstimater
from Segmetaion import Segmetation
from gameGlobals import GameGlobals
import pygame
import numpy as np

class DareToCollect:
    def __init__(self):
        self.prev_frame_time = 0
        self.new_frame_time = 0
        self.eventHandler = EventHandler()
        self.eventHandler.registerEvent("quit",Event(pygame.QUIT,lambda _ : GameGlobals.setGame(None)))
        self.eventHandler.registerEvent("quit_by_press_q",Event( pygame.KEYDOWN, lambda _ : GameGlobals.setGame(None), condition = lambda e : e.key == pygame.K_q))
        self.count = 0
        self.key = pygame.image.load(path.abspath(path.dirname(path.dirname(path.abspath(__file__)))+'../../assets/images/Meteors/Meteor_01.png')).convert_alpha()
        self.key_mask = pygame.mask.from_surface(self.key)
        self.key2 = pygame.image.load(path.abspath(path.dirname(path.dirname(path.abspath(__file__)))+'../../assets/images/Meteors/Meteor_03.png')).convert_alpha()
        self.key_mask2 = pygame.mask.from_surface(self.key2)
        self.color = (0,0,0)
    def play(self):
        self.new_frame_time = time.time() 
        Camera.readFrame()
        if not Camera.ret:
            raise "error occurred"
        
        pos = pygame.mouse.get_pos()
        result = Segmetation.getPersonSegment(Camera.frame)
        # drawBackground(GameGlobals.screen)

        frame_surface = pygame.image.frombuffer(result.tobytes(), result.shape[1::-1], "RGBA")
        result_mask = pygame.mask.from_surface(frame_surface.convert_alpha())
        if not result_mask.overlap(self.key_mask, pos):
            self.color = (0,0,0)
        else:
            print("collide")
            self.color = (255,255,255)
        # frame_surface = pygame.surfarray.make_surface(np.transpose(result, (1, 0, 2)))
        GameGlobals.screen.fill(self.color)

        GameGlobals.screen.blit(frame_surface, (0, 0))
        GameGlobals.screen.blit(self.key, pos)
        # GameGlobals.screen.blit(self.key, (0,0))
        
            

        fps = 1/(self.new_frame_time-self.prev_frame_time) 
        self.prev_frame_time = self.new_frame_time 
        fps = int(fps)
        fps_to_render = GameGlobals.font.render(str(fps), True, (0,0,0))
        GameGlobals.screen.blit(fps_to_render, ( GameGlobals.screen_width // 2, 10))

        pygame.display.flip()
        self.eventHandler.checkEventOccurnce()
