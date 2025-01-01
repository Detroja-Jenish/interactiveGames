import math
import random
from ClimbBall.Background.IBackground import IBackground
import pygame
from gameGlobals import GameGlobals


class __ClimbingHold__:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.alpha = random.randint(50, 150)

class BlueOrangeGradient(IBackground):
    def __init__(self):
        self.CYAN = (0, 255, 255)
        self.BLUE = (0, 100, 255)
        self.ORANGE = (255, 140, 0)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.scorePointColor = (0,0,0)
        self.ballColor = (255, 0, 255)

    def __create_gradient_surface__(self,color1, color2, rect, vertical=True):
        surface = pygame.Surface((rect.width, rect.height))
        for i in range(rect.height if vertical else rect.width):
            ratio = i / (rect.height if vertical else rect.width)
            color = [int(color1[j] * (1 - ratio) + color2[j] * ratio) for j in range(3)]
            if vertical:
                pygame.draw.line(surface, color, (0, i), (rect.width, i))
            else:
                pygame.draw.line(surface, color, (i, 0), (i, rect.height))
        return surface
    
    def __draw_glowing_arc__(self,surface, color, center, radius, start_angle, end_angle, width=10):
        points = []
        for i in range(60):
            angle = math.radians(start_angle + (end_angle - start_angle) * i / 59)
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        
        # Draw main arc
        if len(points) > 1:
            pygame.draw.lines(surface, color, False, points, width)
        
        # Draw glow effect
        glow_surf = pygame.Surface((width * 4, width * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color, 50), (width * 2, width * 2), width * 2)
        for point in points[::3]:  # Draw fewer glow points for performance
            surface.blit(glow_surf, (point[0] - width * 2, point[1] - width * 2), 
                        special_flags=pygame.BLEND_RGB_ADD)
            
    def draw(self):
        GameGlobals.screen.fill(self.BLACK)

    # Create split background with gradients
        left_rect = pygame.Rect(0, 0, GameGlobals.screen_width // 2, GameGlobals.screen_height)
        right_rect = pygame.Rect(GameGlobals.screen_width // 2, 0, GameGlobals.screen_width // 2, GameGlobals.screen_height)
        
        left_gradient = self.__create_gradient_surface__(self.BLUE, self.CYAN, left_rect)
        right_gradient =self.__create_gradient_surface__(self.ORANGE, self.YELLOW, right_rect)
        
        GameGlobals.screen.blit(left_gradient, left_rect)
        GameGlobals.screen.blit(right_gradient, right_rect)

        # Draw glowing arcs
        self.__draw_glowing_arc__(GameGlobals.screen, self.CYAN, (GameGlobals.screen_width // 4, GameGlobals.screen_height // 2), 200, -60, 60)
        self.__draw_glowing_arc__(GameGlobals.screen, self.YELLOW, (3 * GameGlobals.screen_width // 4, GameGlobals.screen_height // 2), 200, 120, 240)
