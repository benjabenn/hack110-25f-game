"""PyGame project for Hack110 Advanced Topics in Games Workshop."""

# Import statements
import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, K_DOWN, K_LEFT, K_RIGHT, K_UP, RLEACCEL

SCREEN_WIDTH: int = 900
SCREEN_HEIGHT: int = 600
TICK_RATE: int = 60
PLAYER_SPEED: int = 4
PLAYER_JUMP_POWER: int = 20
GRAVITY: int = 0.5
PLAYER_FILENAME: str = "assets/foot.png"
BACKGROUND_COLOR = (255, 255, 255)

# Learn more about pygame sprites below!
# Documentation: https://www.pygame.org/docs/ref/sprite.html
# Guide: http://programarcadegames.com/index.php?chapter=introduction_to_sprites&lang=en
# The guide above uses a slightly different method for creating sprites than I did (without using surf)
# It's also a pretty long guide so don't worry about reading all of it
class Player(pygame.sprite.Sprite):
    """The user controlled player."""
    # These are the attributes that we define but there's also surf and rect that we haven't defined
    # but are still there because we are inheriting some characteristics of pygame.sprite.Sprite
    is_jumping: bool
    vertical_velocity: float
    jump_power: int
    speed: int
    
    def __init__(self, jump_power: int) -> None:
        # Super class initialization of the sprite
        super(Player, self).__init__()
        self.is_jumping = False
        self.vertical_velocity = 0
        self.jump_power = jump_power

        # Set the players image, convert, set the surf to be equal to it, then set the black (color (0, 0, 0))
        # background to be transparent (you won't have to do this if you have a transparent image)
        self.surf = pygame.image.load(PLAYER_FILENAME).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        # Set the speed to the constant
        self.speed = PLAYER_SPEED

        # Get the rect from the surface
        # Spawn in the center, a little from the left
        # bottomleft = (x, y) specifies an (x, y) coordinate for the bottom left of the sprite to spawn at
        # https://www.pygame.org/docs/ref/surface.html#pygame.Surface.get_rect
        # https://www.pygame.org/docs/ref/rect.html#:~:text=right%0Atopleft%2C-,bottomleft,-%2C%20topright%2C
        self.rect = self.surf.get_rect(bottomleft = (50, SCREEN_HEIGHT))

    def update(self, pressed_keys) -> None:
        # Checks keys bool value with subscription notation, if True then it moves
        # pressed_keys is a dict that looks kinda like {K_UP: True, K_DOWN : False, K_LEFT : False, K_RIGHT : False}
        # We check the value associated with the key (which is a literal key on the keyboard) to see if true or false
        # It is true when it is being pressed, so then we update in the appropriate direction or jump
        if pressed_keys[K_UP] and not self.is_jumping:
            # If we are not already jumping, start a jump by setting the velocity to the jump power
            self.is_jumping = True
            self.vertical_velocity = self.jump_power
        if self.is_jumping:
            # Move in the direction of the jump
            self.rect.move_ip(0, -self.vertical_velocity)
            # Apply some gravity at each step so that the player will come back down
            self.vertical_velocity -= GRAVITY
            # Once the bottom of the player is at the bottom of the screen, end the jump this way
            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                self.is_jumping = False
                self.vertical_velocity = 0
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        # Checks the bounds, if player reaches the bounds then hold player in place
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


def main() -> None:
    pygame.init()

    screen: pygame.Surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    clock: pygame.Clock = pygame.time.Clock()

    # Create an instance of the Player class that we defined
    player: Player = Player(PLAYER_JUMP_POWER)

    all_sprites = pygame.sprite.Group()

    all_sprites.add(player)

    # Set a running bool variable to True, can be set to False at any time to end the game loop
    running: bool = True

    # Main loop
    while running:
        # Event queue
        for event in pygame.event.get():
            # Stop loop when X button is hit
            if event.type == QUIT:
                running = False
            # Check for KEYDOWN events
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        # Initalize a dict storing all pressed keys by calling the get_pressed() function that gets the state of all
        # keyboard buttons 
        # Documentation: https://www.pygame.org/docs/ref/key.html#pygame.key.get_pressed
        pressed_keys = pygame.key.get_pressed()

        # Call the update method on player by passing the pressed keys dict and within the 
        # update method we will check relevant pressed keys for True/False
        player.update(pressed_keys)

        # Fill the screen with a background color
        screen.fill(BACKGROUND_COLOR)

        # Draw all of the sprites using a for loop
        # Another quick RealPython article for reference!
        # https://realpython.com/lessons/using-blit-and-flip/
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Update the display, is the equivalent of update() with no args
        pygame.display.flip()

        # Tick at constant frame rate
        clock.tick(TICK_RATE)

if __name__ == "__main__":
    main()