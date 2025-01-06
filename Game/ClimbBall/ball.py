import math
import numpy as np
from gameGlobals import GameGlobals
import pygame

class Ball:
    def __init__(self, x, y, radius, color, speed_x, speed_y):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.accelration = 1

    def draw(self):
        pygame.draw.circle(GameGlobals.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.speed_x*self.accelration
        self.y += self.speed_y*self.accelration
        if self.accelration > 1:
            self.accelration -= 0.05
        # Bounce the ball off the top and bottom edges of the screen
        if self.y - self.radius <= 0 or self.y + self.radius >= GameGlobals.screen_height:
            self.speed_y *= -1

    def check_collision_with_hand(self,paddle):
        if not paddle: return
        paddle_x = paddle.center_x
        paddle_y = paddle.center_y
        paddle_radius = paddle.radius
        # Calculate the distance between the ball and the hand center
        distance = math.sqrt((self.x - paddle_x)**2 + (self.y - paddle_y)**2)

        if distance <= self.radius + paddle_radius:
            # If there's a collision, calculate the normal vector
            normal = np.array([self.x - paddle_x, self.y - paddle_y])
            normal = normal / np.linalg.norm(normal)  # Normalize the normal vector

            # Velocity vector of the ball
            velocity = np.array([self.speed_x, self.speed_y])

            # Reflect the velocity using the formula: v' = v - 2(v . n)n
            dot_product = np.dot(velocity, normal)
            reflected_velocity = velocity - 2 * dot_product * normal

            # Update the ball's speed
            self.speed_x, self.speed_y = reflected_velocity

            # Apply a small displacement to avoid the ball getting stuck in the hand
            displacement = normal * (self.radius + paddle_radius - distance + 1)
            self.x += displacement[0]
            self.y += displacement[1]
            self.accelration += 1

    def check_score(self):
        # Check if the ball hits the left or right side of the screen
        if self.x - self.radius <= 0:
            self.accelration = 1
            return 'right'  # Right player gets a point
        elif self.x + self.radius >= GameGlobals.screen_width:
            self.accelration = 1
            return 'left'  # Left player gets a point
        return None
