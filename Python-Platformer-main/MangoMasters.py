import os
import random
import math
import pygame
from os import listdir
from os.path import isfile, join, abspath, dirname

pygame.init()
pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 5
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Get the absolute path of the directory where this script is located
BASE_DIR = dirname(abspath(__file__))

def flip(sprites):
    """
    Flip a list of sprites horizontally.

    Args:
        sprites (list): List of Pygame surfaces.

    Returns:
        list: Horizontally flipped sprites.
    """

    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    """
    Load and split sprite sheets into individual animation frames.

    Args:
        dir1 (str): Main asset directory.
        dir2 (str): Subdirectory for sprites.
        width (int): Width of each sprite frame.
        height (int): Height of each sprite frame.
        direction (bool): If True, also create left/right versions.

    Returns:
        dict: Dictionary mapping animation names to lists of frames.
    """
    path = join(BASE_DIR, "assets", dir1, dir2)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Cannot find asset folder: {path}")
    
    images = [f for f in listdir(path) if isfile(join(path, f))]
    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites

def get_block(size):
    """
    Load and return a terrain block sprite.

    Args:
        size (int): Size of the block (one side length).

    Returns:
        pygame.Surface: Scaled block surface.
    """
    path = join(BASE_DIR, "assets", "Terrain", "Terrain.png")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Cannot find terrain file: {path}")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

# -------------------- Player Class --------------------
class Player(pygame.sprite.Sprite):
    """
    Represents the player character.

    This class handles movement (left/right/jump), gravity, collision behavior,
    animation updates, and score tracking.
    """
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        """
        Initialize the player with a starting position and size.

        Args:
            x (int): Starting x-position.
            y (int): Starting y-position.
            width (int): Width of the player hitbox.
            height (int): Height of the player hitbox.
        """
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.score = 0  # added score for mangoes

    def jump(self):
        """
        Make the player jump and update jump counters.
        """
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        """
        Move the player by a given offset.

        Args:
            dx (int): Horizontal movement.
            dy (int): Vertical movement.
        """
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        """
        Mark the player as hit (used for damage effects).
        """
        self.hit = True

    def move_left(self, vel):
        """
        Move the player left at a given speed.

        Args:
            vel (int): Movement speed.
        """
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        """
        Move the player right at a given speed.

        Args:
            vel (int): Movement speed.
        """
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        """
        Update player physics and animations every frame.

        Args:
            fps (int): Frames per second (used to scale gravity timing).
        """
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        """
        Reset jump/fall counters when the player lands.
        """
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        """
        Handle collision when the player hits a block above.
        """
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        """
        Update the player's sprite based on velocity and state.
        """
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        """
        Update the player's rect and mask based on the current sprite frame.
        """

        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
         """
        Draw the player on the screen.

        Args:
            win (pygame.Surface): Game window surface.
            offset_x (int): Camera x-offset for side scrolling.
        """
         win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

# -------------------- Object Classes --------------------
class Object(pygame.sprite.Sprite):
    """
    Base class for all game objects (terrain, traps, items).
    """
    def __init__(self, x, y, width, height, name=None):
        """
        Initialize a generic game object.

        Args:
            x (int): X position.
            y (int): Y position.
            width (int): Object width.
            height (int): Object height.
            name (str, optional): Identifier name (ex: "fire", "mango").
        """
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        """
        Draw the object on the screen.

        Args:
            win (pygame.Surface): Game window surface.
            offset_x (int): Camera x-offset for side scrolling.
        """
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    """
    Solid terrain block that the player can stand on and collide with.
    """
    def __init__(self, x, y, size):
        """
        Create a block at a given position.

        Args:
            x (int): X position.
            y (int): Y position.
            size (int): Size of the square block.
        """
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """
        Placeholder update method (blocks are static by default).
        """
        pass

    def collide(self, player):
        """
        Check pixel-perfect collision with the player.

        Args:
            player (Player): The player sprite.

        Returns:
            bool: True if colliding, otherwise False.
        """
        return pygame.sprite.collide_mask(self, player)

    def destroy(self):
        """
        Make the block invisible and remove its collision mask.
        """
        self.image.fill((0, 0, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)

    def highlight(self, color=(0, 255, 0)):
        """
        Draw an outline around the block (useful for debugging).

        Args:
            color (tuple): RGB color for the outline.
        """
        pygame.draw.rect(self.image, color, self.image.get_rect(), 2)

    def get_position(self):
        """
        Get the block's current top-left position.

        Returns:
            tuple: (x, y) position.
        """
        return self.rect.topleft

    def resize(self, new_size):
        """
        Resize the block and reload the block sprite.

        Args:
            new_size (int): New block size.
        """
        self.rect.width = new_size
        self.rect.height = new_size
        block = get_block(new_size)
        self.image = pygame.Surface((new_size, new_size), pygame.SRCALPHA)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, x, y):
        """
        Move the block to a new position.

        Args:
            x (int): New x position.
            y (int): New y position.
        """
        self.rect.x = x
        self.rect.y = y

    def is_above(self, player):
        """
        Check if the player is above this block (used for logic checks).

        Args:
            player (Player): The player sprite.

        Returns:
            bool: True if player is above the block, otherwise False.
        """
        return (player.rect.bottom <= self.rect.top and
                player.rect.right > self.rect.left and
                player.rect.left < self.rect.right)


class Fire(Object):
    """
    Animated fire trap that can be toggled on/off and damages the player.
    """
    ANIMATION_DELAY = 3
    def __init__(self, x, y, width, height):
        """
        Create a fire trap.

        Args:
            x (int): X position.
            y (int): Y position.
            width (int): Sprite width.
            height (int): Sprite height.
        """
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        """
        Turn the fire animation on.
        """
        self.animation_name = "on"

    def off(self):
        """
        Turn the fire animation off.
        """
        self.animation_name = "off"

    def loop(self):
        """
        Update fire animation frames each tick.
        """
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)
        if self.animation_count // self.ANIMATION_DELAY >= len(sprites):
            self.animation_count = 0

    def toggle(self):
        """
        Toggle the fire between on and off states.
        """
        if self.animation_name == "on":
            self.off()
        else:
            self.on()

    def damage(self, player):
        """
        Damage the player if fire is on and touching the player.

        Args:
            player (Player): Player sprite to damage.
        """
        if self.animation_name == "on" and pygame.sprite.collide_mask(self, player):
            player.make_hit()

    def reset_animation(self):
        """
        Reset the animation counter back to zero.
        """
        self.animation_count = 0

    def get_position(self):
        """
        Get the fire trap's top-left position.

        Returns:
            tuple: (x, y) position.
        """
        return self.rect.topleft

    def set_size(self, width, height):
        """
        Resize the fire trap sprite.

        Args:
            width (int): New width.
            height (int): New height.
        """
        self.rect.width = width
        self.rect.height = height
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire[self.animation_name][0]
        self.mask = pygame.mask.from_surface(self.image)

# -------------------- Mango Class --------------------
class Mango(Object):
    """
    Collectible mango that increases the player's score when collected.
    """
    def __init__(self, x, y, width, height):
        """
        Create a mango collectible.

        Args:
            x (int): X position.
            y (int): Y position.
            width (int): Mango width.
            height (int): Mango height.
        """
        super().__init__(x, y, width, height, "mango")
        path = join(BASE_DIR, "assets", "Items", "Fruits", "mango.png")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Cannot find mango: {path}")
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.mask = pygame.mask.from_surface(self.image)

# -------------------- Background --------------------
def get_background(name):
    """
    Load and tile the background image across the window.

    Args:
        name (str): Background image filename.

    Returns:
        tuple: (tiles, image) where tiles is a list of positions to blit,
               and image is the loaded background surface.
    """
    path = join(BASE_DIR, "assets", "Background", name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Cannot find background: {path}")
    image = pygame.image.load(path)
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image

# -------------------- Game Loop Helpers --------------------
def draw(window, background, bg_image, player, objects, offset_x):
    """
    Draw the background, objects, and player to the screen.

    Args:
        window (pygame.Surface): Main game window.
        background (list): List of background tile positions.
        bg_image (pygame.Surface): Background image surface.
        player (Player): The player object.
        objects (list): List of all game objects.
        offset_x (int): Camera x-offset.
    """
    for tile in background:
        window.blit(bg_image, tile)
    for obj in objects:
        obj.draw(window, offset_x)
    player.draw(window, offset_x)
    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    """
    Handle vertical collisions between the player and objects.

    Args:
        player (Player): Player sprite.
        objects (list): List of objects to collide with.
        dy (float): Player's vertical movement amount.

    Returns:
        list: Objects that the player collided with vertically.
    """
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
            collided_objects.append(obj)
    return collided_objects

def collide(player, objects, dx):
    """
    Check if the player would collide with something when moving horizontally.

    Args:
        player (Player): Player sprite.
        objects (list): Objects to check collision against.
        dx (int): Horizontal movement amount.

    Returns:
        Object or None: The object collided with (if any).
    """
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break
    player.move(-dx, 0)
    player.update()
    return collided_object

def handle_move(player, objects):
    """
    Handle player movement input and collision checks.

    Also handles interactions like getting hit by fire or collecting mangoes.

    Args:
        player (Player): Player object.
        objects (list): List of all game objects.
    """
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]
    for obj in to_check:
        if obj:
            if obj.name == "fire":
                player.make_hit()
            elif obj.name == "mango":
                objects.remove(obj)
                player.score += 1
                print(f"Mango collected! Score: {player.score}")

# -------------------- Start Screen --------------------
def start_screen(window):
    """
    Display the start screen and wait until the user presses SPACE.
    """
    run = True
    font = pygame.font.SysFont("comicsans", 60)
    small_font = pygame.font.SysFont("comicsans", 40)
    
    while run:
        window.fill((0, 150, 255))
        title_text = font.render("Welcome to Mango Masters!", True, (255, 255, 0))
        start_text = small_font.render("Press SPACE to start", True, (255, 255, 255))
        
        window.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//3))
        window.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False

# -------------------- Main Game --------------------
def main(window):
    """
    Initialize the game objects and run the main game loop.
    """
    start_screen(window)  # <-- added start screen here

    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 96
    player = Player(100, 100, 50, 50)
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size), fire]

    # Add some mangoes
    mango1 = Mango(250, HEIGHT - block_size - 50, 70, 70)
    mango2 = Mango(500, HEIGHT - block_size - 100, 70, 70)
    mango3 = Mango(800, HEIGHT - block_size - 150, 70, 70)
    mango4 = Mango(1200, HEIGHT - block_size - 80, 70, 70)
    objects.extend([mango1, mango2, mango3, mango4])

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        fire.loop()
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or \
           ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)
