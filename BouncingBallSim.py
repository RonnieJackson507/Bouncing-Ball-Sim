import pygame
import math
import Ball

# Initialize Pygame
pygame.init()

# Create a screen (window) with aspect ration of 9:16
width = 500
height = width * 1.778
screen = pygame.display.set_mode((width, height))

# Set title of the window
pygame.display.set_caption("Bouncing Ball Simulator")

# Create a font object
font = pygame.font.Font(None, 50)

# Border variables
borderX = width / 2
borderY = height / 2 - 50
borderRadius = 200
borderWidth = 2

# Physics variables
vel_y = 0 # Initial vertical velocity
gravity = 0.5 # Gravity Constant

# Ball object(s)
balls = [Ball.Ball(width/2, height/2 -50, (255,0,0))]

# Number of collisions from the ball
collisions = 0

# Main loop flag
running = True

# Main game loop
while running:
    # Check for events (like closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update collisions 
    #collisions += 1

    # Fill the screen with a color (RGB)
    screen.fill((0, 0, 0))  # Fill with black
    
    # Render the updated collision count
    text_surface = font.render(f"Collisions = {collisions}", True, (255,255,255))

    # Get the position of the text
    text_rect = text_surface.get_rect(center = (width/2, height - 100))

    # Display the text onto the bottom of the screen
    screen.blit(text_surface, text_rect)

    # Draw the border in the center of the screen
    pygame.draw.circle(screen, (255, 255, 255), (borderX, borderY), borderRadius, borderWidth)

    # Traverse through the Balls array
    for ball in balls:
        # Apply Gravity
        vel_y += gravity
        ball.posY += vel_y * 0.5

        # Calculate the distance from the center of the border to the ball
        dist = math.sqrt((ball.posX - borderX) ** 2 + (ball.posY - borderY) ** 2)

        # Dectect Collisions
        if dist + ball.radius >= borderRadius:
            vel_y = -vel_y
            #Reset the ball position
            ball.posY -= ball.radius
            collisions += 1

        # Draw the ball
        pygame.draw.circle(screen, ball.color, (ball.posX, ball.posY), ball.radius)

    # Update the display
    pygame.display.update()

    # Limit the frame rate to 60 FPS
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
