
import pygame
import os
class GameGlobals:
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    pygame.init()
    font = pygame.font.Font(None, 74)
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w - 10,info.current_h - 10
    screen = pygame.display.set_mode((screen_width, screen_height))
    quit = False
    isCameraCallibered = False
    startToPlay = False
    clock = pygame.time.Clock()
    @classmethod 
    def doQuit(cls):
        cls.quit = True
    @classmethod 
    def setIsCameraCallibered(cls,flag):
        cls.isCameraCallibered = flag
    
    @classmethod 
    def setStartToPlay(cls,flag):
        cls.startToPlay = flag

