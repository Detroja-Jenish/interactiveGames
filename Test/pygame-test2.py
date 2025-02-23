import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Interactive Hexagons")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Generate random points
def generate_points(num_points):
    return [(random.randint(50, width-50), random.randint(50, height-50)) for _ in range(num_points)]

num_points = 10
points = generate_points(num_points)
active_points = list(range(num_points))

# Function to draw a hexagon
def draw_hexagon(surface, color, center, radius, width=2):
    hex_points = []
    for i in range(6):
        angle = i * (2 * math.pi / 6) - math.pi / 2
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        hex_points.append((x, y))
    pygame.draw.polygon(surface, color, hex_points, width)
    return hex_points

# Animation class for disappearing hexagons
class DisappearingHexagon:
    def __init__(self, center, initial_radius):
        self.center = center
        self.initial_radius = initial_radius
        self.current_radius = initial_radius
        self.opacity = 255
        self.animation_time = 0
        self.total_animation_time = 300  # 0.9 seconds


    def update(self, dt):
        self.animation_time += dt
        progress = min(self.animation_time / self.total_animation_time, 1)
        self.current_radius = self.initial_radius * (1 + progress)
        self.opacity = int(255 * (1 - progress))

    def draw(self, surface):
        color = (*WHITE, self.opacity)
        draw_hexagon(surface, color, self.center, self.current_radius, 2)

    def is_finished(self):
        return self.animation_time >= self.total_animation_time

# Main game loop
running = True
clock = pygame.time.Clock()
disappearing_hexagons = []

while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                for i in active_points:
                    hex_points = draw_hexagon(screen, WHITE, points[i], 30)
                    if pygame.draw.polygon(screen, WHITE, hex_points).collidepoint(mouse_pos):
                        disappearing_hexagons.append(DisappearingHexagon(points[i], 30))
                        active_points.remove(i)
                        break

    # Clear the screen
    screen.fill(BLACK)

    # Draw connections between hexagons
    for i in range(len(active_points) - 1):
        start = points[active_points[i]]
        end = points[active_points[i + 1]]
        pygame.draw.line(screen, YELLOW, start, end, 2)

    # Draw hexagons and numbers
    for i in active_points:
        draw_hexagon(screen, WHITE, points[i], 30)
        font = pygame.font.Font(None, 36)
        text = font.render(str(i + 1), True, RED)
        text_rect = text.get_rect(center=points[i])
        screen.blit(text, text_rect)

    # Update and draw disappearing hexagons
    for hex in disappearing_hexagons[:]:
        hex.update(dt)
        hex.draw(screen)
        if hex.is_finished():
            disappearing_hexagons.remove(hex)

    # Recreate list if all hexagons are gone
    if not active_points and not disappearing_hexagons:
        points = generate_points(num_points)
        active_points = list(range(num_points))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()