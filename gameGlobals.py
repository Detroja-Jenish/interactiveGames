import pygame
import os
class GameGlobals:
    os.environ["SDL_VIDEO_CENTERED"] = '1'
    pygame.init()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w - 10,info.current_h - 10
    screen = pygame.display.set_mode((screen_width, screen_height))
