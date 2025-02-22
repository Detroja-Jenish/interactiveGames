import pygame
import os
import json

from utils.getPersistentPath import getPersistentPath 
class GameGlobals:
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    pygame.init()
    pygame.mixer.init()
    font = pygame.font.Font(None, 74)
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w - 10,info.current_h - 10
    screen = pygame.display.set_mode((screen_width, screen_height))
    quit = False
    isCameraCallibered = False
    startToPlay = False
    clock = pygame.time.Clock()
    game = None
    config = {
    "calliberationCords": {
        "x": 14,
        "y": 13,
        "width": 1400,
        "height": 818
    },
    "camera": {
        "source": 0,
        "flip": False
    },
    "climbBall": {
        "background": 0
    },
    "astroidShooter": {}
}
    try:
        with open(getPersistentPath("config.json"),"r") as fp:
            config = json.load(fp)
    except Exception as e:
        pass
    @classmethod 
    def doQuit(cls):
        cls.quit = True
    @classmethod 
    def setIsCameraCallibered(cls,flag):
        cls.isCameraCallibered = flag
    
    @classmethod 
    def setStartToPlay(cls,flag):
        cls.startToPlay = flag
    
    @classmethod
    def setGame(cls,game):
        cls.game = game

