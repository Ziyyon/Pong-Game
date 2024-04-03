import pygame
import random

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Constants
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 20
PADDLE_SPEED = 10
INITIAL_BALL_SPEED_X = 5
INITIAL_BALL_SPEED_Y = 5
MISS_PROBABILITY = 0  
BALL_ACCELERATION = 0.005 

# Paddles
def reset_paddles():
    global player_paddle, computer_paddle
    player_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    computer_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

reset_paddles()

# Ball
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x = INITIAL_BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = INITIAL_BALL_SPEED_Y * random.choice((1, -1))

player_score = 0
computer_score = 0
rally_length = 0
paused = False
winner = None

def draw_objects():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, computer_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    # Display scores
    font = pygame.font.Font(None, 36)
    player_text = font.render(f"Thabo: {player_score}", True, WHITE)
    computer_text = font.render(f"Computer: {computer_score}", True, WHITE)
    screen.blit(player_text, (50, 20))
    screen.blit(computer_text, (WIDTH - 200, 20))
    # Display winner
    if paused and winner is not None:
        winner_text = font.render(f"{winner} WINS!", True, WHITE)
        screen.blit(winner_text, ((WIDTH - winner_text.get_width()) // 2, (HEIGHT - winner_text.get_height()) // 2))
    # Display pause text
    if paused and winner is None:
        pause_text = font.render("PAUSED", True, WHITE)
        screen.blit(pause_text, ((WIDTH - pause_text.get_width()) // 2, (HEIGHT - pause_text.get_height()) // 2))

def move_paddles():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_paddle.top > 0:
        player_paddle.move_ip(0, -PADDLE_SPEED)
    if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
        player_paddle.move_ip(0, PADDLE_SPEED)

    # AI for the computer-controlled paddle
    if ball_speed_x > 0:
        if computer_paddle.top < ball.y:
            computer_paddle.move_ip(0, PADDLE_SPEED)
        elif computer_paddle.bottom > ball.y:
            computer_paddle.move_ip(0, -PADDLE_SPEED)

def move_ball():
    global ball_speed_x, ball_speed_y, rally_length, player_score, computer_score, winner, paused
    
    if not paused: 
        ball.move_ip(ball_speed_x, ball_speed_y)
        # Check for collisions with walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y = -ball_speed_y
        if ball.left <= 0:
            # Player scores
            computer_score += 1
            reset_ball()
            reset_paddles()
        if ball.right >= WIDTH:
            # Computer scores
            player_score += 1
            reset_ball()
            reset_paddles()
        
        # Check for winner
        if player_score >= 10 or computer_score >= 10:
            paused = True
            # Determine winner
            if player_score >= 10:
                winner = "Thabo"
            else:
                winner = "Computer"
    
        # Check for collisions with paddles
        if ball.colliderect(player_paddle) or ball.colliderect(computer_paddle):
            ball_speed_x = -ball_speed_x
            rally_length += 1
        else:
            rally_length = 0
    
        # Accelerate ball speed based on rally length
        ball_speed_x += BALL_ACCELERATION * (1 if ball_speed_x > 0 else -1)
        ball_speed_y += BALL_ACCELERATION * (1 if ball_speed_y > 0 else -1)

# Reset the ball position
def reset_ball():
    global ball_speed_x, ball_speed_y, rally_length
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = INITIAL_BALL_SPEED_X * random.choice((1, -1))
    ball_speed_y = INITIAL_BALL_SPEED_Y * random.choice((1, -1))
    rally_length = 0

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused 
            
    # Move paddles and ball
    move_paddles()
    move_ball()
    
    # Draw objects
    draw_objects()
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
