import pygame
from EventHandler import Event, EventHandler
from Game.AstroidShooter import AstroidShooter
from Game.ClimbBall import ClimbBall
from Game.Flash import Flash
from gameGlobals import GameGlobals
from utils.color import Color


class GameSelector:
    def __init__(self):
        self.eventHandler = EventHandler()
        self.eventHandler.registerEvent("quit",Event(pygame.QUIT,lambda _ : GameGlobals.doQuit()))
        self.eventHandler.registerEvent("quit_by_press_q",Event( pygame.KEYDOWN, lambda _ : GameGlobals.doQuit(), condition = lambda e : e.key == pygame.K_q))
        self.BOXES = [
    pygame.Rect(50, 50, 200, 200),
    pygame.Rect(350, 50, 200, 200),
    pygame.Rect(50, 350, 200, 200),
    pygame.Rect(350, 350, 200, 200)
]
        self.eventHandler.registerEvent("flash", Event(pygame.MOUSEBUTTONDOWN, lambda _ : GameGlobals.setGame( Flash()) ,condition=lambda e: self.BOXES[0].collidepoint(e.pos)))
        self.eventHandler.registerEvent("ClimbBall", Event(pygame.MOUSEBUTTONDOWN, lambda _ : GameGlobals.setGame( ClimbBall()) ,condition=lambda e: self.BOXES[1].collidepoint(e.pos)))
        self.eventHandler.registerEvent("Save Earth", Event(pygame.MOUSEBUTTONDOWN, lambda _ : GameGlobals.setGame( AstroidShooter()) ,condition=lambda e: self.BOXES[2].collidepoint(e.pos)))
        self.GAMES = ["Flash", "ClimbBall", "Save Earth", "Game 4"]

    def play(self):
        GameGlobals.screen.fill(Color.WHITE)

        # Draw the boxes
        colors = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]
        for i, box in enumerate(self.BOXES):
            pygame.draw.rect(GameGlobals.screen, colors[i], box)
            text = GameGlobals.font.render(self.GAMES[i], True, Color.BLACK)
            text_rect = text.get_rect(center=box.center)
            GameGlobals.screen.blit(text, text_rect)

        # Update the display
        self.eventHandler.checkEventOccurnce()
        pygame.display.flip()