import math
import random
import pygame
from gameGlobals import GameGlobals

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class Hexagon:
    def __init__(self, center, initial_radius,id):
        self.id=id
        self.center = center
        self.initial_radius = initial_radius
        self.current_radius = initial_radius
        self.opacity = 255
        self.animation_time = 0
        self.total_animation_time = 300  # 0.9 seconds
        self.needToDisapper = False

    def checkCollision(self, paddle):
        if not paddle: return
        paddle_x = paddle.center_x
        paddle_y = paddle.center_y
        paddle_radius = paddle.radius
        # Calculate the distance between the ball and the hand center
        distance = math.sqrt((self.center[0] - paddle_x)**2 + (self.center[1] - paddle_y)**2)

        if distance <= self.initial_radius + paddle_radius:
            self.needToDisapper = True

    def update(self):
        self.animation_time += GameGlobals.dt
        progress = min(self.animation_time / self.total_animation_time, 1)
        self.current_radius = self.initial_radius * (1 + progress)
        self.opacity = int(255 * (1 - progress))

    def draw(self):
        if self.needToDisapper:
            self.update()
        color = (*WHITE, self.opacity)
        hex_points = []
        for i in range(6):
            angle = i * (2 * math.pi / 6) - math.pi / 2
            x = self.center[0] + self.current_radius * math.cos(angle)
            y = self.center[1] + self.current_radius * math.sin(angle)
            hex_points.append((x, y))
        pygame.draw.polygon(GameGlobals.screen, color, hex_points, 0)
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.id), True, RED)
        text_rect = text.get_rect(center=self.center)
        GameGlobals.screen.blit(text, text_rect)
        # self.draw_hexagon(surface, color, self.center, self.current_radius, 2)

    def is_finished(self):
        return self.animation_time >= self.total_animation_time

class HexagonHandler:
    def __init__(self):
        self.hexagonRadius = 30
        self.hexagons = self.generate_hexagons(10)

    def generate_hexagons(self,num_points):
        return [Hexagon((random.randint(50, GameGlobals.screen_width-50), random.randint(50, GameGlobals.screen_height-50)),self.hexagonRadius,i) for i in range(num_points)]
    
    def draw(self):
        for i in range(len(self.hexagons) - 1):
            start = self.hexagons[i].center
            end = self.hexagons[i+1].center
            pygame.draw.line(GameGlobals.screen, YELLOW, start, end, 2)
        for hexagon in self.hexagons:
            hexagon.draw()
        

    def checkCollision(self,paddle):
        self.hexagons[0].checkCollision(paddle)

    def cleanup(self):
        for hexagon in self.hexagons:
            if hexagon.is_finished():
                self.hexagons.remove(hexagon)
        if len(self.hexagons) ==0 :
            self.hexagons = self.generate_hexagons(10)
