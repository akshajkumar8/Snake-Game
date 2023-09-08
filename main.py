# Import required libraries
import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set up display dimensions
width, height = 640, 480
screen = pygame.display.set_mode((width, height))  # Create the game window
pygame.display.set_caption('Snake Game by Akshaj Kumar')  # Set the window title

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Load font
font = pygame.font.Font(None, 36)

# Initialize snake and food
snake = [(200, 200)]  # Snake's initial position
snake_dir = (0, 0)  # Snake's initial direction
food = (random.randrange(0, width, 10), random.randrange(0, height, 10))  # Random initial food position

# Create a clock to control frame rate
clock = pygame.time.Clock()

# Initialize game variables
game_over = False
score = 0

# Initialize menu and pause variables
menu = True
paused = False

# Main game loop
while True:
    # Event handling loop
    for event in pygame.event.get():
        # Check if the user clicked the red 'X' button to quit the game
        if event.type == pygame.QUIT:
            pygame.quit()  # Quit the pygame library
            exit()  # Exit the Python script

        # Check if a key was pressed down
        elif event.type == pygame.KEYDOWN:
            # Check if the Esc key was pressed
            if event.key == pygame.K_ESCAPE:
                # Check if the game is currently in the menu
                if menu:
                    pygame.quit()  # Quit the pygame library
                    exit()  # Exit the Python script
                else:
                    paused = not paused  # Toggle the paused state

            # Check if the game is not in the menu and not paused
            if not menu and not paused:
                # Check for specific keys to control the snake's direction
                if event.key == pygame.K_UP and snake_dir != (0, 10):
                    snake_dir = (0, -10)  # Change the snake's direction to move up
                if event.key == pygame.K_DOWN and snake_dir != (0, -10):
                    snake_dir = (0, 10)   # Change the snake's direction to move down
                if event.key == pygame.K_LEFT and snake_dir != (10, 0):
                    snake_dir = (-10, 0)  # Change the snake's direction to move left
                if event.key == pygame.K_RIGHT and snake_dir != (-10, 0):
                    snake_dir = (10, 0)   # Change the snake's direction to move right

    if menu:
        # Draw menu
        screen.fill(black)  # Fill the screen with black color
        menu_text = font.render("Snake Game", True, white)  # Render the menu text
        start_text = font.render("Press SPACE to Start", True, white)  # Render the start text

        # Render directions for pausing the game
        pause_directions = font.render("Press 'P' to Pause/Unpause", True, white)

        # Display the instructions and start prompt
        screen.blit(menu_text, (width // 2 - menu_text.get_width() // 2, height // 2 - 50))
        screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2))

        # Display the pause directions below the start prompt
        screen.blit(pause_directions, (width // 2 - pause_directions.get_width() // 2, height // 2 + 50))

        keys = pygame.key.get_pressed()  # Get the state of all keyboard keys
        if keys[pygame.K_SPACE]:  # Check if SPACE key is pressed
            menu = False  # Start the game
    elif not paused:
        # Move the snake
        new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])  # Calculate new head position
        snake.insert(0, new_head)  # Insert the new head into the snake list

        # Check for collision with food
        if snake[0] == food:
            score += 1
            food = (random.randrange(0, width, 10), random.randrange(0, height, 10))  # Place new food randomly
        else:
            snake.pop()  # Remove the last segment of the snake

        # Check for collision with walls
        if snake[0][0] < 0 or snake[0][0] >= width or snake[0][1] < 0 or snake[0][1] >= height:
            game_over = True

        # Check for self-collision
        if len(snake) != len(set(snake)):
            game_over = True

    screen.fill(black)  # Clear the screen with black color

    if not menu:
        if game_over:
            # Draw Game Over message
            game_over_text = font.render("Game Over", True, white)
            restart_text = font.render("Press SPACE to Restart", True, white)
            screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))
            screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 50))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                # Reset game variables
                snake = [(200, 200)]
                snake_dir = (0, 0)
                food = (random.randrange(0, width, 10), random.randrange(0, height, 10))
                score = 0
                game_over = False

                # Delay before restarting
                pygame.time.delay(1000)

        else:
            # Draw snake
            for segment in snake:
                pygame.draw.rect(screen, green, pygame.Rect(segment[0], segment[1], 10, 10))  # Draw snake segment

            # Draw food
            pygame.draw.rect(screen, red, pygame.Rect(food[0], food[1], 10, 10))  # Draw food

            # Draw score
            score_text = font.render(f"Score: {score}", True, white)
            screen.blit(score_text, (10, 10))  # Display the score at the top left corner of the screen

            if paused:
                pause_text = font.render("Paused", True, white)
                screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2))  # Display "Paused" message at the center of the screen

    pygame.display.flip()  # Update the display

    clock.tick(15)  # Limit the frame rate to 15 frames per second
