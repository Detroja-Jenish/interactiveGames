import pygame
import random

# Initialize Pygame
# pygame.init()

# # Set up the display
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Space Background")

# # Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Star:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.speed = random.uniform(0.1, 1)
        self.size = random.uniform(0.5, 2)

    def move(self):
        self.y += self.speed
        if self.y > self.height:
            self.y = 0
            self.x = random.randint(0, self.width)

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), int(self.size))

# Create stars
# stars = [Star() for _ in range(200)]

# # Main game loop
# running = True
# clock = pygame.time.Clock()

# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Clear the screen
#     screen.fill(BLACK)

#     # Update and draw stars
#     for star in stars:
#         star.move()
#         star.draw(screen)

#     # Update the display
#     pygame.display.flip()

#     # Cap the frame rate
#     clock.tick(60)

# # Quit Pygame
# pygame.quit()

class SpaceBackGround:
    def __init__(self,width,height):
        self.stars = [Star(width,height) for _ in range(200)]

    def draw(self,screen):
        screen.fill(BLACK)

    # Update and draw stars
        for star in self.stars:
            star.move()
            star.draw(screen)