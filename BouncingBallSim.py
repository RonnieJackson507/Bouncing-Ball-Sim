import pygame
import math
import Ball

# Initialize Pygame
pygame.init()

# Create a screen (window) with aspect ration of 9:16
width = 450
height = width * 1.778
centerX = width / 2
centerY = height / 2
screen = pygame.display.set_mode((width, height))

# Set title of the window
pygame.display.set_caption("Bouncing Ball Simulator")

# Create a font object
font = pygame.font.Font(None, 50)

# Border variables
borderX = centerX
borderY = centerY - 50
borderRadius = 200
borderWidth = 2

# Physics variables
gravity = 0.5 # Gravity Constant
bounce = 0.5 #Bounce Constant

# Ball object(s)
balls = [Ball.Ball(centerX + 0, centerY -50, (255,0,0)),
         Ball.Ball(centerX + 150, centerY -50, (0,255,0)),
         Ball.Ball(centerX - 50, centerY -150, (0,0,255))]

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
    text_rect = text_surface.get_rect(center = (centerX, height - 100))

    # Display the text onto the bottom of the screen
    screen.blit(text_surface, text_rect)

    # Draw the border in the center of the screen
    pygame.draw.circle(screen, (255, 255, 255), (borderX, borderY), borderRadius, borderWidth)

    # Traverse through the Balls array
    for ball in balls:
        # Apply Gravity
        ball.velY += gravity
        ball.posY += ball.velY * bounce

        # Calculate the distance from the center of the border to the ball
        dist = math.sqrt((ball.posX - borderX) ** 2 + (ball.posY - borderY) ** 2)

        # Dectect Collisions
        if dist + ball.radius >= borderRadius:
            ball.velY = -ball.velY
            ball.posY -= ball.radius #Reset the ball position
            collisions += 1

        # Draw the ball
        pygame.draw.circle(screen, ball.color, (ball.posX, ball.posY), ball.radius)

    # Update the display
    pygame.display.update()

    # Limit the frame rate to 60 FPS
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()