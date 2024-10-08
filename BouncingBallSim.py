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

# Create the text surface
text_surface = font.render('Collisions = 0', True, (255,255,255))

# Get the rectangle of the text
text_rect = text_surface.get_rect(center = (width/2, height - 100))


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

    # Display the text onto the bottom of the screen
    screen.blit(text_surface, text_rect)

    # Draw a border in the center of the screen
    pygame.draw.circle(screen, (255, 255, 255), (width/2, height/2 - 50), borderRadius, borderWidth)

    # Draw a red circle in the center of the screen
    pygame.draw.circle(screen, (255, 0, 0), (width/2, height/2 - 50), ballRadius)

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()
