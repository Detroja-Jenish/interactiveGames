import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Selector")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Font
FONT = pygame.font.Font(None, 36)

# Game boxes
BOXES = [
    pygame.Rect(50, 50, 200, 200),
    pygame.Rect(350, 50, 200, 200),
    pygame.Rect(50, 350, 200, 200),
    pygame.Rect(350, 350, 200, 200)
]

# Game names
GAMES = ["Game 1", "Game 2", "Game 3", "Game 4"]

# Callback functions (simulated for this example)
def game_1_callback():
    print("Starting Game 1")

def game_2_callback():
    print("Starting Game 2")

def game_3_callback():
    print("Starting Game 3")

def game_4_callback():
    print("Starting Game 4")

CALLBACKS = [game_1_callback, game_2_callback, game_3_callback, game_4_callback]

# Main game loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, box in enumerate(BOXES):
                        if box.collidepoint(event.pos):
                            CALLBACKS[i]()

        # Clear the screen
        SCREEN.fill(WHITE)

        # Draw the boxes
        colors = [RED, GREEN, BLUE, YELLOW]
        for i, box in enumerate(BOXES):
            pygame.draw.rect(SCREEN, colors[i], box)
            text = FONT.render(GAMES[i], True, BLACK)
            text_rect = text.get_rect(center=box.center)
            SCREEN.blit(text, text_rect)

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()