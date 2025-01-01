from Game.ClimbBall.ball import Ball
import random 
from gameGlobals import GameGlobals

class GameState:
    def __init__(self,ballColor):
        self.ball = Ball(x=random.randint(50, GameGlobals.screen_width-50), y=random.randint(50, GameGlobals.screen_height-50), radius=40, color=ballColor, speed_x=5, speed_y=5)
        self.left_score = 0 
        self.right_score = 0
        self.running = True
        self.state = 'start' # 'start' | 'play' | 'crop'

    def updateScore(self):
        scoreSide = self.ball.check_score()
        if scoreSide == 'left': 
            self.left_score += 1
            self.ball.x, self.ball.y = GameGlobals.screen_width // 2, GameGlobals.screen_height // 2  # Reset ball position
        elif scoreSide == 'right' : 
            self.right_score += 1
            self.ball.x, self.ball.y = GameGlobals.screen_width // 2, GameGlobals.screen_height // 2  # Reset ball position