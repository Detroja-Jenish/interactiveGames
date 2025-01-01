
from Camera import Camera
from EventHandler import Event, EventHandler
from Game.ClimbBall.Background.BlueOrangeGradient import BlueOrangeGradient
from Game.ClimbBall.Background.Space import Space
from Game.ClimbBall.gameState import GameState
from HandDetection import HandDetection
from gameGlobals import GameGlobals
import pygame

class ClimbBall:
    def __init__(self):
        if(int(input("enter background number"))):
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
        results = HandDetection.detectHand(Camera.frame)
        # GameGlobals.screen.fill((200, 200, 200))
        # drawBackground(GameGlobals.screen)
        self.background.draw()

        if results:
            for index, hand in enumerate(results):
                pygame.draw.circle(GameGlobals.screen, hand.color, (hand.center_x, hand.center_y), hand.radius, 0)
                self.gameState.ball.check_collision_with_hand(hand.center_x, hand.center_y, hand.radius)
            

        self.gameState.ball.move();
        self.gameState.ball.draw()
        self.gameState.updateScore()
        left_score = GameGlobals.font.render(str(self.gameState.left_score), True, self.background.scorePointColor)
        right_score = GameGlobals.font.render(str(self.gameState.right_score), True, self.background.scorePointColor)
        GameGlobals.screen.blit(left_score, (GameGlobals.screen_width // 4, 10))
        GameGlobals.screen.blit(right_score, (3 * GameGlobals.screen_width // 4, 10))

        pygame.display.flip()
        self.eventHandler.checkEventOccurnce()
        # print(GameGlobals.clock.get_fps())