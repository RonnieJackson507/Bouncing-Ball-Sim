import pygame

# Initialize Pygame
pygame.init()

# Create a screen (window) with width=800 and height=600
screen = pygame.display.set_mode((600, 800))

# Set title of the window
pygame.display.set_caption("Bouncing Ball Simulator")

# Main loop flag
running = True

# Main game loop
while running:
    # Check for events (like closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with a color (RGB)
    screen.fill((0, 0, 0))  # Fill with black

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
