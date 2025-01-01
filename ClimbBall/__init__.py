from Camera import Camera
from ClimbBall.background import drawBackground
from EventHandler import Event, EventHandler
from HandDetection import HandDetection
from ClimbBall.gameState import GameState
from gameGlobals import GameGlobals
import pygame

class ClimbBall:
    def __init__(self):
        self.gameState = GameState()
        self.eventHandler = EventHandler()
        self.eventHandler.registerEvent("quit",Event(pygame.QUIT,lambda _ : GameGlobals.doQuit()))
        self.eventHandler.registerEvent("quit_by_press_q",Event( pygame.KEYDOWN, lambda _ : GameGlobals.doQuit(),lambda e : print("from lambda",e.key == pygame.K_q), condition = lambda e : e.key == pygame.K_q))

    def play(self):
        Camera.readFrame()
        if not Camera.ret:
            raise "error occurred"
        results = HandDetection.detectHand(Camera.frame)
        # GameGlobals.screen.fill((200, 200, 200))
        drawBackground(GameGlobals.screen)
        if results:
            for index, hand in enumerate(results):
                pygame.draw.circle(GameGlobals.screen, hand.color, (hand.center_x, hand.center_y), hand.radius, 0)
                self.gameState.ball.check_collision_with_hand(hand.center_x, hand.center_y, hand.radius)
            

        self.gameState.ball.move();
        pygame.draw.circle(GameGlobals.screen, self.gameState.ball.color, (self.gameState.ball.x, self.gameState.ball.y), self.gameState.ball.radius)

        self.gameState.updateScore()
        left_score = GameGlobals.font.render(str(self.gameState.left_score), True, (0, 0, 0))
        right_score = GameGlobals.font.render(str(self.gameState.right_score), True, (0, 0, 0))
        GameGlobals.screen.blit(left_score, (GameGlobals.screen_width // 4, 10))
        GameGlobals.screen.blit(right_score, (3 * GameGlobals.screen_width // 4, 10))

        pygame.display.flip()
        self.eventHandler.checkEventOccurnce()
        print(GameGlobals.clock.get_fps())