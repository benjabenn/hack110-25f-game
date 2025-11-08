"""PyGame project for Hack110 Advanced Topics in Games Workshop."""

# Import statements
import pygame
import random
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, K_DOWN, K_LEFT, K_RIGHT, K_UP

SCREEN_WIDTH: int = 900
SCREEN_HEIGHT: int = 600
TICK_RATE: int = 60

class Player(pygame.sprite.Sprite):
    is_jumping: bool
    vertical_velocity: int
    jump_power: int
    speed: int
    surf: pygame.Surface
    rect: pygame.Rect
    
    def __init__(self):
        super(Player, self).__init__()
        self.is_jumping = False
        self.vertical_velocity = 0
        self.jump_power = 50
        self.speed = 5

        # Boilerplate, copy this
        self.surf = pygame.image.load("assets/foot.png").convert()
        self.rect = self.surf.get_rect(bottomleft = (50, SCREEN_HEIGHT))  

    def update(self, pressed_keys) -> None:
        if pressed_keys[K_UP] and not self.is_jumping:
            self.is_jumping = True
            self.vertical_velocity = self.jump_power
        if self.is_jumping:
            self.rect.move_ip(0, -self.vertical_velocity)
            self.vertical_velocity -= 1

            if self.rect.bottom >= SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
                self.is_jumping = False
                self.vertical_velocity = 0

class Boulder(pygame.sprite.Sprite):
    speed: int
    surf: pygame.Surface
    rect: pygame.Rect

    def __init__(self):
        super(Boulder, self).__init__()

        self.speed = random.randint(4, 12)
        self.surf = pygame.image.load("assets/boulder.png").convert()
        self.rect = self.surf.get_rect(bottomleft = (SCREEN_WIDTH, SCREEN_HEIGHT))

    def update(self):
        self.rect.move_ip(-self.speed, 0)

        if self.rect.right < 0:
            self.kill()

def main() -> None:
    pygame.init()

    screen: pygame.Surface = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    clock: pygame.Clock = pygame.time.Clock()

    ADDBOULDER = pygame.USEREVENT
    pygame.time.set_timer(ADDBOULDER, 2000, 100)

    player: Player = Player()

    all_sprites = pygame.sprite.Group()
    boulders = pygame.sprite.Group()
    all_sprites.add(player)

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
            elif event.type == ADDBOULDER:
                new_boulder: Boulder = Boulder()
                boulders.add(new_boulder)
                all_sprites.add(new_boulder)

        screen.fill((255, 255, 255))

        pressed_keys = pygame.key.get_pressed()

        player.update(pressed_keys)
        
        for boulder in boulders:
            boulder.update()

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollideany(player, boulders):
            player.kill()
            print(f"You are dead!")
            running = False

        # Update the display, is the equivalent of update() with no args
        pygame.display.flip()

        # Tick at constant frame rate
        clock.tick(TICK_RATE)

if __name__ == "__main__":
    main()