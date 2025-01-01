import pygame
from camera import Camera
from game import Game
from gameState import GameState


while GameState.running:
    if GameState.state == 'play':
        Game.play()
    if GameState.state == 'start':
        Game.startScreen()
    
Camera.cam.release()
pygame.quit()