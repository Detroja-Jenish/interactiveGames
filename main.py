from Calliberation import Calliberation
from Camera import Camera
from Game import GameSelector
from Game.AstroidShooter import AstroidShooter
from Game.ClimbBall import ClimbBall
from Game.Flash import Flash
from gameGlobals import GameGlobals
import pygame
import cv2
# game = ClimbBall()
# game = AstroidShooter()
gameSelector = GameSelector()
# def main():
calliberation = Calliberation()
while not GameGlobals.quit:
    if GameGlobals.startToPlay and GameGlobals.game:
        GameGlobals.game.play()
    elif GameGlobals.startToPlay:
        gameSelector.play()
    else:
        calliberation.doCaliber()

# main()
pygame.mixer.music.stop()
pygame.quit()
Camera.cam.release()
Camera.video_writer.release()