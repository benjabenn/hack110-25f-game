"""PyGame project for Hack110 Advanced Topics in Games Workshop."""

# Import statements
import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

SCREEN_WIDTH: int = 900
SCREEN_HEIGHT: int = 600
TICK_RATE: int = 60

def main() -> None:
    pygame.init()

    screen: pygame.Surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    clock: pygame.Clock = pygame.time.Clock()

    running: bool = True

    while running:
        for event in pygame.event.get():
            # Stop loop when X button is hit
            if event.type == QUIT:
                running = False
            # Check for KEYDOWN events
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        # Update the display, is the equivalent of update() with no args
        pygame.display.flip()

        # Tick at constant frame rate
        clock.tick(TICK_RATE)

if __name__ == "__main__":
    main()