import pygame  # type: ignore

# Initialize Pygame
pygame.init()

# Screen configuration
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Game variables
running = True
dt = 0

# Player configuration
player_pos = pygame.Vector2(100, SCREEN_HEIGHT - 200 - 70)
player_size = (70, 70)
player_speed = 300
player_angle = 0
rotation_speed = -125
vertical_velocity = 0
jump_force = 900
gravity = 2500
is_jumping = False
jump_start_time = 0

# Ground configuration
ground_height = 200

# Scrolling configuration
scroll_speed = 500
scroll_offset = 0

# Load player image
player_image = pygame.image.load(r"C:\Users\alexa\Documents\ISEP\Garage\Projet_IA_GD\Player.png")
player_image = pygame.transform.scale(player_image, player_size)
# Spike player image
triangle_image = pygame.image.load(r"C:\Users\alexa\Documents\ISEP\Garage\Projet_IA_GD\Spike.png")
triangle_image = pygame.transform.scale(triangle_image, (70, 70))  # Ajustez la taille si nécessaire


# Colors
BG_COLOR = "#2117d4"
GROUND_COLOR = "#0a047a"
OBSTACLE_FILL_COLOR = "black"
OBSTACLE_BORDER_COLOR = "gray"

# Functions
def draw_ground():
    """Draw the ground at the bottom of the screen."""
    pygame.draw.rect(
        screen, 
        GROUND_COLOR, 
        pygame.Rect(0, SCREEN_HEIGHT - ground_height, SCREEN_WIDTH, ground_height)
    )

def draw_triangle(position):
    """Draw a triangular obstacle at a given position."""
    obstacle_x = scroll_offset + position
    obstacle_y = SCREEN_HEIGHT - ground_height - 70
    triangle_points = [
        (obstacle_x, obstacle_y + 70),         # Bottom-left
        (obstacle_x + 70, obstacle_y + 70),   # Bottom-right
        (obstacle_x + 35, obstacle_y)         # Top
    ]
    screen.blit(triangle_image, (obstacle_x, obstacle_y))

def draw_square(positionx, positiony):
    """Draw a square obstacle at a given position."""
    obstacle_x = scroll_offset + positionx
    obstacle_y = SCREEN_HEIGHT - ground_height - 70 - positiony
    square_rect = pygame.Rect(obstacle_x, obstacle_y, *player_size)
    pygame.draw.rect(screen, OBSTACLE_FILL_COLOR, square_rect)  # Fill
    pygame.draw.rect(screen, OBSTACLE_BORDER_COLOR, square_rect, width=3)  # Border

def handle_player_jump():
    """Handle the player's jump mechanics."""
    global is_jumping, vertical_velocity, jump_start_time
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping and player_pos.y + player_size[1] >= SCREEN_HEIGHT - ground_height:
        vertical_velocity = -jump_force
        is_jumping = True
        jump_start_time = pygame.time.get_ticks()

def apply_gravity():
    """Apply gravity to the player."""
    global vertical_velocity, is_jumping
    vertical_velocity += gravity * dt
    player_pos.y += vertical_velocity * dt
    if player_pos.y + player_size[1] >= SCREEN_HEIGHT - ground_height:
        player_pos.y = SCREEN_HEIGHT - ground_height - player_size[1]
        vertical_velocity = 0
        is_jumping = False

def rotate_player():
    """Rotate the player while in the air."""
    if is_jumping:
        elapsed_time = (pygame.time.get_ticks() - jump_start_time) / 1000  # Time in seconds
        return min(elapsed_time * rotation_speed, 360)  # Rotate gradually up to 360 degrees
    return 0

def draw_player():
    """Draw the player on the screen with rotation."""
    rotated_player = pygame.transform.rotate(player_image, player_angle)
    rotated_rect = rotated_player.get_rect(center=(
        player_pos.x + player_size[0] // 2, 
        player_pos.y + player_size[1] // 2
    ))
    screen.blit(rotated_player, rotated_rect.topleft)

def reset_game():
    """Reset the game to its initial state."""
    global player_pos, vertical_velocity, is_jumping, scroll_offset, player_angle
    player_pos = pygame.Vector2(100, SCREEN_HEIGHT - 200 - 70)
    vertical_velocity = 0
    is_jumping = False
    scroll_offset = 0
    player_angle = 0


# Game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(BG_COLOR)

    # Update game state
    scroll_offset -= scroll_speed * dt
    handle_player_jump()
    apply_gravity()
    player_angle = rotate_player()

    # Collision detection with triangles
    triangle_positions = [1000, 1070, 1140]
    player_rect = pygame.Rect(player_pos.x, player_pos.y, *player_size)

    for position in triangle_positions:
        obstacle_x = scroll_offset + position
        obstacle_y = SCREEN_HEIGHT - ground_height - 50
        triangle_rect = pygame.Rect(obstacle_x, obstacle_y, 50, 50)  # Approximative bounding box
        if player_rect.colliderect(triangle_rect):
            print("Collision with triangle!")  # Debugging
            reset_game()  # Reset the game


    # Draw elements
    draw_ground()
    draw_player()
    draw_triangle(1000)
    draw_triangle(1070)
    draw_triangle(1140)
    draw_square(1400, 0)
    draw_square(1400, 70)

    # Update display
    pygame.display.flip()

    # Control frame rate
    dt = clock.tick(60) / 1000  # 60 FPS

pygame.quit()