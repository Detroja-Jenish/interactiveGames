import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ValoClimb Background")

# Colors
CYAN = (0, 255, 255)
BLUE = (0, 100, 255)
ORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Timer font
font = pygame.font.Font(None, 72)

class ClimbingHold:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.alpha = random.randint(50, 150)

def create_gradient_surface(color1, color2, rect, vertical=True):
    surface = pygame.Surface((rect.width, rect.height))
    for i in range(rect.height if vertical else rect.width):
        ratio = i / (rect.height if vertical else rect.width)
        color = [int(color1[j] * (1 - ratio) + color2[j] * ratio) for j in range(3)]
        if vertical:
            pygame.draw.line(surface, color, (0, i), (rect.width, i))
        else:
            pygame.draw.line(surface, color, (i, 0), (i, rect.height))
    return surface

def draw_glowing_arc(surface, color, center, radius, start_angle, end_angle, width=10):
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

# Create climbing holds
holds = [ClimbingHold(random.randint(0, width), random.randint(0, height), 
                     random.randint(10, 25)) for _ in range(50)]

# Main game loop
running = True
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(BLACK)

    # Create split background with gradients
    left_rect = pygame.Rect(0, 0, width // 2, height)
    right_rect = pygame.Rect(width // 2, 0, width // 2, height)
    
    left_gradient = create_gradient_surface(BLUE, CYAN, left_rect)
    right_gradient = create_gradient_surface(ORANGE, YELLOW, right_rect)
    
    screen.blit(left_gradient, left_rect)
    screen.blit(right_gradient, right_rect)

    # Draw climbing holds
    for hold in holds:
        hold_surface = pygame.Surface((hold.size * 2, hold.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(hold_surface, (255, 255, 255, hold.alpha), 
                         (hold.size, hold.size), hold.size)
        screen.blit(hold_surface, (hold.x - hold.size, hold.y - hold.size))

    # Draw glowing arcs
    draw_glowing_arc(screen, CYAN, (width // 4, height // 2), 200, -60, 60)
    draw_glowing_arc(screen, YELLOW, (3 * width // 4, height // 2), 200, 120, 240)

    # Draw timer
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer_text = font.render(f"{minutes}:{seconds:02d}", True, WHITE)
    timer_rect = timer_text.get_rect(center=(width // 2, 50))
    
    # Draw timer background circle
    pygame.draw.circle(screen, BLACK, timer_rect.center, 50)
    screen.blit(timer_text, timer_rect)

    # Draw logo text
    logo_font = pygame.font.Font(None, 36)
    logo_text = logo_font.render("VALOCLIMB", True, WHITE)
    screen.blit(logo_text, (20, height - 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()