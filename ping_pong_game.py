import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Paddle properties
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_COLOR = WHITE
paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2

# Ball properties
BALL_RADIUS = 10
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 5, 5

# Draw paddle
def draw_paddle(paddle_y):
    pygame.draw.rect(screen, PADDLE_COLOR, (50, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Draw ball
def draw_ball(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), BALL_RADIUS)

def game_loop(hand_y):
    global ball_x, ball_y, ball_dx, ball_dy
    screen.fill(BLACK)
    
    # Update paddle position based on hand_y
    paddle_y = hand_y - PADDLE_HEIGHT // 2
    draw_paddle(paddle_y)

    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with top/bottom walls
    if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
        ball_dy = -ball_dy

    # Ball collision with paddle
    if (50 <= ball_x - BALL_RADIUS <= 60 and paddle_y <= ball_y <= paddle_y + PADDLE_HEIGHT):
        ball_dx = -ball_dx

    # Draw ball
    draw_ball(ball_x, ball_y)
    
    pygame.display.flip()
    clock.tick(60)

