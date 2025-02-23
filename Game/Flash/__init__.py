
import time
from Camera import Camera
from EventHandler import Event, EventHandler
from Game.Flash.Background.Space import Space
from Game.ClimbBall.gameState import GameState
from Game.Flash.Hexagon import HexagonHandler
from PoseEstimater import PoseEstimater
import pygame

from gameGlobals import GameGlobals

class Flash:
    def __init__(self):
        self.prev_frame_time = 0
        self.new_frame_time = 0
        self.background = Space()
        self.gameState = GameState(self.background.ballColor)
        self.eventHandler = EventHandler()
        self.eventHandler.registerEvent("quit",Event(pygame.QUIT,lambda _ : GameGlobals.setGame(None)))
        self.eventHandler.registerEvent("quit_by_press_q",Event( pygame.KEYDOWN, lambda _ : GameGlobals.setGame(None), condition = lambda e : e.key == pygame.K_q))
        self.hexagonHandler = HexagonHandler()
    
    def play(self):
        GameGlobals.tick()
        Camera.readFrame()
        if not Camera.ret:
            raise "error occurred"
        
        self.new_frame_time = time.time() 
        results = PoseEstimater.detectPersons(Camera.frame)
        # GameGlobals.screen.fill((200, 200, 200))
        # drawBackground(GameGlobals.screen)

        # frame_surface = pygame.surfarray.make_surface(np.transpose(Camera.frame, (1, 0, 2)))
        # GameGlobals.screen.blit(frame_surface, (0, 0))
        self.background.draw()
        if results:
            for result in results:
                for paddle in result.getNotNoneValues(takeNose=False):
                    pygame.draw.circle(GameGlobals.screen, paddle.color, (paddle.center_x, paddle.center_y), paddle.radius, 0)
                    self.hexagonHandler.checkCollision(paddle)
        self.hexagonHandler.draw()
        self.hexagonHandler.cleanup()
        pygame.display.flip()
        self.eventHandler.checkEventOccurnce()
