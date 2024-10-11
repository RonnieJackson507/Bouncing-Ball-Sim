import pygame
import math
import Ball
import Border

# TODO Add a menu to customize the simulator
# TODO Add a way to ask the user to add a sound
# TODO Add a way to add a image to the ball if the User wants it

# Initialize Pygame
pygame.init()

# Create a screen (window) with aspect ration of 9:16
WIDTH = 550
HEIGHT = WIDTH * 1.778
CENTER = [WIDTH / 2, HEIGHT / 2]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60

# Set title of the window
pygame.display.set_caption("Bouncing Ball Simulator")

# Create a font object
font = pygame.font.Font(None, 50)

# Border object
border = Border.Border(CENTER[0], CENTER[1] - 50, 200, 2)

# Ball object(s)
balls = []
balls_num = 50
for i in range(1,balls_num + 1):
    balls.append(Ball.Ball(border))

# Draws the text onto the screen
def draw_text (text, font, color, surface, x, y):
    # Render the updated collision count
    text_surface = font.render(text, True, color)

    # Get the position of the text
    text_rect = text_surface.get_rect(center = (x, y))

    # Display the text onto the bottom of the screen
    surface.blit(text_surface, text_rect)

# Main game loop flag
running = True

# Main game loop
while running:
    # Check for events (like closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (RGB)
    screen.fill((0, 0, 0))  # Fill with black
    
    # Draw the border in the center of the screen
    border.draw(screen)

    collision = 0 # Collisions from the ball

    # Traverse through the Balls array
    for ball in balls:
        # Update the ball
        ball.update()

        collision += ball.collision

        # Draw the ball
        ball.draw(screen)

    # Draw the text for the collision
    draw_text(f"Collisions = {collision}", font, (255, 255, 255), screen, CENTER[0], CENTER[1] + 300)

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    pygame.time.Clock().tick(FPS)

# Quit Pygame
pygame.quit()