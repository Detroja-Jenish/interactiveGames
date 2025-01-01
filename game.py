import pygame
from camera import Camera
from gameState import GameState
from pygameRender import PyGameRender
import numpy as np
from gameGlobals import GameGlobals

class Game:
    @classmethod
    def updateScore(cls):
        score_side = GameState.ball.check_score()
        if score_side == 'left':
            GameState.left_score += 1
            GameState.ball.x, GameState.ball.y = GameGlobals.screen_width // 2, GameGlobals.screen_height // 2  # Reset ball position
        elif score_side == 'right':
            GameState.right_score += 1
            GameState.ball.x, GameState.ball.y = GameGlobals.screen_width // 2, GameGlobals.screen_height // 2  # Reset ball position

    @classmethod
    def play(cls):
        Camera.readFrame()
        if not Camera.ret:
            raise "error occurred"

        results = GameState.handsModel.process(Camera.frame)

        # frame_surface = pygame.surfarray.make_surface(np.transpose(Camera.frame, (1, 0, 2)))
        # GameGlobals.screen.blit(frame_surface, (0, 0))
        GameGlobals.screen.fill((200, 200, 200))

        if results.multi_hand_landmarks:
            PyGameRender.renderHands(results.multi_hand_landmarks)

        GameState.ball.move()
        PyGameRender.renderBall()

        Game.updateScore()
        PyGameRender.renderScore()

        pygame.display.flip()
        PyGameRender.checkEvents()
        
        PyGameRender.fps_clock.tick(60)
    @classmethod
    def startScreen(cls):
        # Capture the current frame from the camera
        Camera.readFrame()
        if not Camera.ret:
            raise "Error occurred in capturing frame"

        # Create a surface from the captured frame
        frame_surface = pygame.surfarray.make_surface(np.transpose(Camera.frame, (1, 0, 2)))
        GameGlobals.screen.blit(frame_surface, (0, 0))  # Set it as backgroun
        
        PyGameRender.renderCropScreen()
        PyGameRender.addCropEvents()

    # Add event handling for the cropping rectangle
        crop_button = PyGameRender.renderBtn("Crop",10, 10, 200, 50)
        start_button = PyGameRender.renderBtn("start game",10, 80, 200, 50)
        quit_button = PyGameRender.renderBtn("quit game",10, 150, 200, 50)
        pygame.draw.circle(GameGlobals.screen, (255,255,255), (0,0), GameState.ball.radius)
        pygame.draw.circle(GameGlobals.screen, (255,0,255), (0,GameGlobals.screen_height), GameState.ball.radius)
        pygame.draw.circle(GameGlobals.screen, (255,255,0), (GameGlobals.screen_width,0), GameState.ball.radius)
        pygame.draw.circle(GameGlobals.screen, (0,255,255), (GameGlobals.screen_width,GameGlobals.screen_height), GameState.ball.radius)
        # Flip display to render changes
        pygame.display.flip()
        # Add event for the start button
        PyGameRender.addEvent(
            "start_btn",
            pygame.MOUSEBUTTONDOWN, 
            lambda e: setattr(GameState, 'state', 'play'),  # Correct callback here
            lambda e: start_button.collidepoint(e.pos),  # Condition: Check if button is clicked
        )

        PyGameRender.addEvent(
            "quit_btn",
            pygame.MOUSEBUTTONDOWN, 
            lambda e: setattr(GameState, 'running', False),  # Correct callback here
            lambda e: quit_button.collidepoint(e.pos)  # Condition: Check if button is clicked
        )
        PyGameRender.addEvent(
            "crop_button",
            pygame.MOUSEBUTTONDOWN, 
            lambda e: Camera.setCrop( PyGameRender.cropping_rect.x,PyGameRender.cropping_rect.y ,PyGameRender.cropping_rect.width ,PyGameRender.cropping_rect.height),#
            # lambda e: setattr(GameState, 'state', 'play'),  # Correct callback here
            lambda e: start_button.collidepoint(e.pos),  # Condition: Check if button is clicked
        )
        # Check for all registered events
        PyGameRender.checkEvents()
