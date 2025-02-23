import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hexagon Points")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Generate random points
num_points = 10
points = [(random.randint(50, width-50), random.randint(50, height-50)) for _ in range(num_points)]

# Function to draw a hexagon
def draw_hexagon(surface, color, center, radius):
    points = []
    for i in range(6):
        angle = i * (2 * math.pi / 6) - math.pi / 2
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    pygame.draw.polygon(surface, color, points, 2)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw hexagons and numbers
    for i, point in enumerate(points, 1):
        draw_hexagon(screen, WHITE, point, 30)
        font = pygame.font.Font(None, 36)
        text = font.render(str(i), True, RED)
        text_rect = text.get_rect(center=point)
        screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()