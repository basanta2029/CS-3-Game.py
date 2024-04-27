import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
RED = (255, 0, 0)        # Color for the ball
BLUE = (0, 0, 255)       # Color for the paddles
BLACK = (0, 0, 0)        # Background color
WHITE = (255, 255, 255)  # Color for text
FONT = pygame.font.Font(None, 36)
WINNING_SCORE = 10

# Difficulty settings
difficulties = {
    'easy': 3,
    'medium': 5,
    'hard': 8
}

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Paddle settings
paddle_width, paddle_height = 10, 100
paddle_speed = 5
ai_speed = 5  # Default cpu speed, will change based on difficulty

# Ball settings
ball_radius = 7
ball_speed_x = 7
ball_speed_y = 7

# Initialize positions and ball speed
def init_positions():
    global player_y, opponent_y, ball_x, ball_y, ball_speed_x, ball_speed_y
    player_y = HEIGHT // 2 - paddle_height // 2
    opponent_y = HEIGHT // 2 - paddle_height // 2
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_x = 7 * (-1 if ball_speed_x > 0 else 1)
    ball_speed_y = 7

init_positions()

# Player positions
player_x = 30
opponent_x = WIDTH - 30 - paddle_width

# Scores
player_score = 0
opponent_score = 0

# Game state
paused = True
game_over = False
mode = "menu"  # Could be 'menu', 'single', 'multi', 'choose_difficulty'

# CPU movement
def ai_movement():
    global opponent_y
    if ball_y > opponent_y + paddle_height // 2:
        opponent_y += ai_speed
    elif ball_y < opponent_y + paddle_height // 2:
        opponent_y -= ai_speed

# Display menu
def display_menu():
    screen.fill(BLACK)
    menu_text = FONT.render("Press 1 for Single Player, 2 for Multiplayer", True, WHITE)
    screen.blit(menu_text, (WIDTH // 2 - 300, HEIGHT // 2 - 60))
    pygame.display.flip()

# Display difficulty selection
def display_difficulty_menu():
    screen.fill(BLACK)
    difficulty_text = FONT.render("Choose difficulty: E for Easy, M for Medium, H for Hard", True, WHITE)
    screen.blit(difficulty_text, (WIDTH // 2 - 400, HEIGHT // 2 - 20))
    pygame.display.flip()

# Set difficulty
def set_difficulty(level):
    global ai_speed
    ai_speed = difficulties[level]

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if mode == "menu":
                if event.key == pygame.K_1:
                    mode = "choose_difficulty"
                elif event.key == pygame.K_2:
                    mode = "multi"
                    paused = False
            elif mode == "choose_difficulty":
                if event.key == pygame.K_e:
                    set_difficulty('easy')
                    mode = "single"
                    paused = False
                elif event.key == pygame.K_m:
                    set_difficulty('medium')
                    mode = "single"
                    paused = False
                elif event.key == pygame.K_h:
                    set_difficulty('hard')
                    mode = "single"
                    paused = False
            elif not game_over:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_r:
                    player_score = 0
                    opponent_score = 0
                    game_over = False
                    paused = True
                    init_positions()

    if mode == "menu":
        display_menu()
    elif mode == "choose_difficulty":
        display_difficulty_menu()
    else:
        if not paused and not game_over:
            if mode == "single":
                ai_movement()
            elif mode == "multi":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_s]:
                    opponent_y += paddle_speed
                if keys[pygame.K_w]:
                    opponent_y -= paddle_speed

            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                player_y += paddle_speed
            if keys[pygame.K_UP]:
                player_y -= paddle_speed

            # Ball movement
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Ball collision with top and bottom
            if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
                ball_speed_y *= -1

            # Ball collision with paddles
            if (ball_x - ball_radius <= player_x + paddle_width and player_y <= ball_y <= player_y + paddle_height) or \
            (ball_x + ball_radius >= opponent_x and opponent_y <= ball_y <= opponent_y + paddle_height):
                ball_speed_x *= -1

            # Ball out of bounds
            if ball_x < 0:
                opponent_score += 1
                if opponent_score >= WINNING_SCORE:
                    game_over = True
                init_positions()
            if ball_x > WIDTH:
                player_score += 1
                if player_score >= WINNING_SCORE:
                    game_over = True
                init_positions()

        # Drawing
        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, (player_x, player_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, BLUE, (opponent_x, opponent_y, paddle_width, paddle_height))
        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
        player_text = FONT.render(str(player_score), True, WHITE)
        opponent_text = FONT.render(str(opponent_score), True, WHITE)
        screen.blit(player_text, (WIDTH // 4, 20))
        screen.blit(opponent_text, (3 * WIDTH // 4, 20))

        if paused and mode != "menu" and not game_over:
            pause_text = FONT.render("Paused - Press SPACE to continue", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - 200, HEIGHT // 2 - 20))

        if game_over:
            winner = "Player 1" if player_score > opponent_score else "Player 2"
            game_over_text = FONT.render(f"{winner} Wins! Press R to Restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 230, HEIGHT // 2 - 20))

        pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
