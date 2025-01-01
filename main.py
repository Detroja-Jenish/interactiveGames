import pygame
from camera import Camera
from game import Game
from gameState import GameState
from pygameRender import PyGameRender


while GameState.running:
    if GameState.state == 'play':
        # PyGameRender.screen = pygame.display.set_mode((GameGlobals.screen_width, GameGlobals.screen_height))
        Game.play()
    if GameState.state == 'start':
        Game.startScreen()
    
Camera.cam.release()
pygame.quit()