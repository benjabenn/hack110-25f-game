"""PyGame project for Hack110 Advanced Topics in Games Workshop."""

# Import statements
import pygame
import random
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, K_DOWN, K_LEFT, K_RIGHT, K_UP, RLEACCEL

SCREEN_WIDTH: int = 900
SCREEN_HEIGHT: int = 600
TICK_RATE: int = 60
PLAYER_SPEED: int = 4
PLAYER_JUMP_POWER: int = 15
GRAVITY: int = 0.5
ENEMY_SPEED_MIN: int = 5
ENEMY_SPEED_MAX: int = 10
ROTATION_SPEED_MIN: int = 5
ROTATION_SPEED_MAX: int = 100
PLAYER_FILENAME: str = "assets/foot.png"
ENEMY_FILENAME: str = "assets/boulder.png"
BACKGROUND_COLOR = (255, 255, 255)
TIME_BETWEEN_BOULDERS = 2000
NUMBER_OF_BOULDERS = 100

# Learn more about pygame sprites below!
# Documentation: https://www.pygame.org/docs/ref/sprite.html
# Guide: http://programarcadegames.com/index.php?chapter=introduction_to_sprites&lang=en
# The guide above uses a slightly different method for creating sprites than I did (without using surf)
# It's also a pretty long guide so don't worry about reading all of it
class Player(pygame.sprite.Sprite):
    """The user controlled player."""
    is_jumping: bool
    vertical_velocity: float
    jump_power: int
    speed: int
    surf: pygame.Surface
    rect: pygame.Rect
    
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

class Boulder(pygame.sprite.Sprite):
    """Enemy class"""
    rotation_angle: int
    original_image: pygame.Surface
    speed: int
    rotation_speed: int
    surf: pygame.Surface
    rect: pygame.Rect

    def __init__(self, speed: int, rotation_speed: int) -> None:
        # Super class initialization of the sprite
        super(Boulder, self).__init__()
        
        self.original_image = pygame.image.load(ENEMY_FILENAME).convert()

        # Create the image for the enemy to be, convert it
        self.surf = self.original_image

        # Remove the background (can use a color picker to find the color's RGB values)
        self.surf.set_colorkey((246, 246, 246), RLEACCEL)

        # center = (x, y) specifies an (x, y) coordinate for the center of the sprite to spawn at
        self.rect = self.surf.get_rect(bottomleft = (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Set speed and rotation speed from args
        self.speed = speed
        self.rotation_speed = rotation_speed

        self.rotation_angle = 0


    def update(self):
        # Move left
        self.rect.move_ip(-self.speed, 0)
        # Bonus: Rotate the boulder!
        self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360
        rotated_surf = pygame.transform.rotate(self.original_image, self.rotation_angle)
        rotated_rect = rotated_surf.get_rect(center=self.rect.center)
        self.surf = rotated_surf
        self.rect = rotated_rect
        if self.rect.right < 0:
            self.kill()

def main() -> None:
    pygame.init()

    screen: pygame.Surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    clock: pygame.Clock = pygame.time.Clock()

    # Create an instance of the Player class that we defined
    player: Player = Player(PLAYER_JUMP_POWER)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    player_group = pygame.sprite.GroupSingle()
    player_group.add(player)

    boulders = pygame.sprite.Group()

    # Create an event! pygame events have numbers, we want to put one 
    # at the end of the list of numbers, which is at index pygame.USEREVENT. 
    # After that set a timer to loop the event, with args for ms between actions 
    # and number of loops
    # Go here for more information!
    # https://coderslegacy.com/python/pygame-userevents/
    ADDBOULDER = pygame.USEREVENT
    pygame.time.set_timer(ADDBOULDER, TIME_BETWEEN_BOULDERS, NUMBER_OF_BOULDERS)

    # Set a running bool variable to True, can be set to False at any time to end the game loop
    running: bool = True

    score: int = 0

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
            elif event.type == ADDBOULDER:
                new_speed = random.randint(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
                new_rotation_speed = random.randint(ROTATION_SPEED_MIN, ROTATION_SPEED_MAX)
                new_boulder: Boulder = Boulder(new_speed, new_rotation_speed)
                boulders.add(new_boulder)
                all_sprites.add(new_boulder)


        # Initalize a dict storing all pressed keys by calling the get_pressed() function that gets the state of all
        # keyboard buttons 
        # Documentation: https://www.pygame.org/docs/ref/key.html#pygame.key.get_pressed
        pressed_keys = pygame.key.get_pressed()

        # Call the update method on player by passing the pressed keys dict and within the 
        # update method we will check relevant pressed keys for True/False
        player.update(pressed_keys)

        for boulder in boulders:
            boulder.update()

        # Fill the screen with a background color
        screen.fill(BACKGROUND_COLOR)

        # Draw all of the sprites using a for loop
        # Another quick RealPython article for reference!
        # https://realpython.com/lessons/using-blit-and-flip/
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check for any collisions between the player and any boulder
        # Collisions are a difficult topic, the links below can help!
        # Documentation: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.spritecollideany
        # Guide: https://coderslegacy.com/python/pygame-sprite-collision-detection/#:~:text=Sprite%20Collision%20Functions
        if pygame.sprite.spritecollideany(player, boulders):
            # If so, kill player and end game (end loop)
            player.kill()
            print(f"\nYou got hit! Score: {score}")
            running = False

        # Update the display, is the equivalent of update() with no args
        pygame.display.flip()

        # Tick at constant frame rate
        clock.tick(TICK_RATE)

        score += 1

if __name__ == "__main__":
    main()