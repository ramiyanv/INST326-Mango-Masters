import pygame

# Initialize Pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Platformer")

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 100, 200)
RED = (200, 50, 50)
GREEN = (50, 200, 50)

# Clock
clock = pygame.time.Clock()

# Player setup
player_width, player_height = 30, 50
start_x = 50
start_y = HEIGHT - player_height - 50
player_x = start_x
player_y = start_y
player_speed = 5
player_vel_y = 0
gravity = 0.5
jump_strength = 10
on_ground = False

# Floor setup
floor_y = HEIGHT - 50
floor_rect = pygame.Rect(0, floor_y, WIDTH, 50)

# Obstacle setup
obstacle_rect = pygame.Rect(300, floor_y - 30, 50, 30)

# Main loop
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = -jump_strength
        on_ground = False

    # Apply gravity
    player_vel_y += gravity
    player_y += player_vel_y

    # Collision with floor
    if player_y + player_height >= floor_y:
        player_y = floor_y - player_height
        player_vel_y = 0
        on_ground = True

    # Collision with obstacle
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    if player_rect.colliderect(obstacle_rect):
        print("Hit obstacle!")
        # Reset player position
        player_x = start_x
        player_y = start_y
        player_vel_y = 0
        on_ground = False

    # Draw floor and obstacle
    pygame.draw.rect(screen, GREEN, floor_rect)
    pygame.draw.rect(screen, RED, obstacle_rect)

    # Draw player
    pygame.draw.rect(screen, BLUE, player_rect)

    # Update display
    pygame.display.flip()

pygame.quit()
