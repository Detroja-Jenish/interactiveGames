import pygame
from gameState import GameState
from camera import Camera
from utils.getCenteres import get_centers
import numpy as np

class Event:
    def __init__(self, type, callback, condition=lambda e: True):
        self.type = type
        self.callback = callback
        self.condition = condition

class PyGameRender:
    pygame.init()
    fps_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((Camera.width, Camera.height))
    pygame.display.set_caption("Hand Bounding Circle and Ball")
    font = pygame.font.Font(None, 74)
    registered_events = {
        "quit": Event(pygame.QUIT, lambda e: setattr(GameState, 'running', False))
    }
    # cropping_rect = pygame.Rect(100, 100, 200, 150)
    cropping_rect = pygame.Rect(332, 338, 109, 66)
      # Initial rectangle
    resizing = False
    moving = False
    offset_x = 0
    offset_y = 0
    resizing_margin = 10  # Margin for corner resizing
    
    @classmethod
    def renderCropScreen(cls):
        # Fill the screen with a background color/frame (if necessary)
        Camera.readFrame()
        frame_surface = pygame.surfarray.make_surface(np.transpose(Camera.frame, (1, 0, 2)))
        cls.screen.blit(frame_surface, (0, 0))

        # Draw the cropping rectangle
        pygame.draw.rect(cls.screen, (255, 0, 0), cls.cropping_rect, 2)  # Draw a red rectangle with a border thickness of 2

        pygame.display.flip()

    @classmethod
    def addCropEvents(cls):
        def handleResize(event):
            if cls.is_resizing_area(event.pos):
                cls.resizing = True
            else:
                cls.moving = True
                cls.offset_x = cls.cropping_rect.x - event.pos[0]
                cls.offset_y = cls.cropping_rect.y - event.pos[1]

        def deactiveResize(event):
            cls.moving = False
            cls.resizing = False

        def handleRectMove(event):
            
            if cls.moving:
                cls.cropping_rect.x = event.pos[0] + cls.offset_x
                cls.cropping_rect.y = event.pos[1] + cls.offset_y
            elif cls.resizing:
                # Resize the rectangle (only lower-right corner resizing for simplicity)
                cls.cropping_rect.width = event.pos[0] - cls.cropping_rect.x
                cls.cropping_rect.height = event.pos[1] - cls.cropping_rect.y


        cls.addEvent("1",pygame.MOUSEBUTTONDOWN,handleResize,lambda event: cls.cropping_rect.collidepoint(event.pos))
        cls.addEvent("2",pygame.MOUSEBUTTONUP,deactiveResize)
        cls.addEvent("3",pygame.MOUSEMOTION,handleRectMove)

    @classmethod
    def is_resizing_area(cls, mouse_pos):
        # Check if the mouse is within the resizing margin of the bottom-right corner
        return (
            abs(mouse_pos[0] - (cls.cropping_rect.x + cls.cropping_rect.width)) <= cls.resizing_margin and
            abs(mouse_pos[1] - (cls.cropping_rect.y + cls.cropping_rect.height)) <= cls.resizing_margin
        )
    
    @classmethod
    def renderScore(cls):
        left_text = cls.font.render(str(GameState.left_score), True, (0, 0, 0))
        right_text = cls.font.render(str(GameState.right_score), True, (0, 0, 0))
        cls.screen.blit(left_text, (Camera.width // 4, 10))
        cls.screen.blit(right_text, (3 * Camera.width // 4, 10))

    @classmethod
    def renderHands(cls, multi_hand_landmarks):
        hand_objects = get_centers(multi_hand_landmarks, Camera.frame)
        for index, hand in enumerate(hand_objects):
            cls.renderHand(hand)
            GameState.ball.check_collision_with_hand(hand.center_x, hand.center_y, hand.radius)
            if(index == 1): print(cls.fps_clock.get_fps())

    @classmethod
    def renderBall(cls):
        pygame.draw.circle(cls.screen, GameState.ball.color, (GameState.ball.x, GameState.ball.y), GameState.ball.radius)

    @classmethod
    def renderHand(cls, hand):
        pygame.draw.circle(cls.screen, hand.color, (hand.center_x, hand.center_y), hand.radius, 0)

    @classmethod
    def renderBtn(cls, name, x1, y1, width, height):
        button_color = (0, 128, 255)
        hover_color = (0, 200, 255)
        font = pygame.font.Font(None, 36)
        text_color = (255, 255, 255)

        # Create the button rectangle
        btn = pygame.Rect(x1, y1, width, height)

        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw the button (hover effect)
        pygame.draw.rect(cls.screen, hover_color if btn.collidepoint(mouse_pos) else button_color, btn)

        # Render the text
        text = font.render(name, True, text_color)

        # Get the size of the text
        text_rect = text.get_rect()

        # Calculate the position to center the text inside the button
        text_x = x1 + (width - text_rect.width) // 2
        text_y = y1 + (height - text_rect.height) // 2

        # Render the text on the screen at the calculated position
        cls.screen.blit(text, (text_x, text_y))

        return btn


    @classmethod
    def addEvent(cls, name, type, callback, condition=lambda e: True):
        if name not in cls.registered_events:
            cls.registered_events[name] = Event(type, callback, condition)

    @classmethod
    def checkEvents(cls):
        for event in pygame.event.get():
            for name, registered_event in cls.registered_events.items():

                if event.type == registered_event.type and registered_event.condition(event):
                    registered_event.callback(event)
