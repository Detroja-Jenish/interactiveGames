import pygame
import sys

# Initialize pygame
pygame.init()

# Set up screens
screen1 = pygame.display.set_mode((800, 600), flags=pygame.NOFRAME, display=0)  # Game display
screen2 = pygame.display.set_mode((800, 600), flags=pygame.NOFRAME, display=1)  # Settings display

pygame.display.set_caption("Game Play Screen", display=0)
pygame.display.set_caption("Settings & Selection Screen", display=1)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# State variables
current_game = None
running = True
selected_game = None


# Dummy game logic
def game_one(screen):
    screen.fill(BLUE)
    font = pygame.font.Font(None, 50)
    text = font.render("Game One Playing!", True, WHITE)
    screen.blit(text, (100, 250))


def game_two(screen):
    screen.fill(RED)
    font = pygame.font.Font(None, 50)
    text = font.render("Game Two Playing!", True, WHITE)
    screen.blit(text, (100, 250))


# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Press 1 or 2 to select games on the second screen
            if event.key == pygame.K_1:
                selected_game = "game_one"
            elif event.key == pygame.K_2:
                selected_game = "game_two"
            elif event.key == pygame.K_ESCAPE:
                running = False

    # Update screen1 based on selected game
    if selected_game == "game_one":
        game_one(screen1)
    elif selected_game == "game_two":
        game_two(screen1)
    else:
        screen1.fill(BLACK)

    # Update screen2 with game selection menu
    screen2.fill(WHITE)
    font = pygame.font.Font(None, 40)
    screen2.blit(font.render("Press 1 for Game One", True, BLACK), (50, 100))
    screen2.blit(font.render("Press 2 for Game Two", True, BLACK), (50, 200))
    screen2.blit(font.render("Press ESC to Quit", True, BLACK), (50, 300))

    # Update displays
    pygame.display.update()

# Quit pygame
pygame.quit()
sys.exit()
