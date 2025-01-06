import time
from Camera import Camera
from EventHandler import Event, EventHandler
from Game.ClimbBall.Background.BlueOrangeGradient import BlueOrangeGradient
from Game.ClimbBall.Background.Space import Space
from Game.ClimbBall.gameState import GameState
from PoseEstimater import PoseEstimater
from gameGlobals import GameGlobals
import pygame
import numpy as np

class ClimbBall:
    def __init__(self):
        self.prev_frame_time = 0
        self.new_frame_time = 0
        if(GameGlobals.config["climbBall"]["background"]):
            self.background = Space()
        else:
            self.background = BlueOrangeGradient()
        self.gameState = GameState(self.background.ballColor)
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

        if results:
            for index, person in enumerate(results):
                for paddle in person.getNotNoneValues(takeNose=False):
                    pygame.draw.circle(GameGlobals.screen, paddle.color, (paddle.center_x, paddle.center_y), paddle.radius, 0)
                    self.gameState.ball.check_collision_with_hand(paddle)
            

        self.gameState.ball.move();
        self.gameState.ball.draw()
        self.gameState.updateScore()
        left_score = GameGlobals.font.render(str(self.gameState.left_score), True, self.background.scorePointColor)
        right_score = GameGlobals.font.render(str(self.gameState.right_score), True, self.background.scorePointColor)
        GameGlobals.screen.blit(left_score, (GameGlobals.screen_width // 4, 10))
        GameGlobals.screen.blit(right_score, (3 * GameGlobals.screen_width // 4, 10))

        fps = 1/(self.new_frame_time-self.prev_frame_time) 
        self.prev_frame_time = self.new_frame_time 
        fps = int(fps)
        fps_to_render = GameGlobals.font.render(str(fps), True, (255,0,0))
        GameGlobals.screen.blit(fps_to_render, ( GameGlobals.screen_width // 2, 10))

        pygame.display.flip()
        self.eventHandler.checkEventOccurnce()
        # print(GameGlobals.clock.get_fps())