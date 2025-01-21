
import time
from Camera import Camera
from EventHandler import Event, EventHandler
from Game.Flash.Background import Space
from PoseEstimater import PoseEstimater
from gameGlobals import GameGlobals
import pygame

class Flash:
    def __init__(self):
        self.prev_frame_time = 0
        self.new_frame_time = 0
        self.background = Space()
        self.eventHandler = EventHandler()
        self.eventHandler.registerEvent("quit",Event(pygame.QUIT,lambda _ : GameGlobals.doQuit()))
        self.eventHandler.registerEvent("quit_by_press_q",Event( pygame.KEYDOWN, lambda _ : GameGlobals.doQuit(), condition = lambda e : e.key == pygame.K_q))

    def selectBackground(self):
        pass
    def play(self):
        Camera.readFrame()
        if not Camera.ret:
            raise "error occurred"
        self.new_frame_time = time.time() 
        results = PoseEstimater.detectHand(Camera.frame)
        # GameGlobals.screen.fill((200, 200, 200))
        # drawBackground(GameGlobals.screen)

        # frame_surface = pygame.surfarray.make_surface(np.transpose(Camera.frame, (1, 0, 2)))
        # GameGlobals.screen.blit(frame_surface, (0, 0))
        self.background.draw()