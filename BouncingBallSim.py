import pygame

ballRadius = 10
borderRadius = 200
borderWidth = 2

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

    # Draw a border in the center of the screen
    pygame.draw.circle(screen, (255, 255, 255), (width/2, height/2 - 50), borderRadius, borderWidth)

    # Draw a red circle in the center of the screen
    pygame.draw.circle(screen, (255, 0, 0), (width/2, height/2 - 50), ballRadius)

    # Update the display
    pygame.display.update()

    # Limit the frame rate to 60 FPS
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
