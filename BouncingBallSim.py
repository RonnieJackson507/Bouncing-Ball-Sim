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

collisions = 0 # Collisions from the ball

# Physics variables
gravity = 0.5 # Gravity Constant
bounce = 0.5 #Bounce Constant

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
    
    # Render the updated collision count
    text_surface = font.render(f"Collisions = {collisions}", True, (255,255,255))

    # Get the position of the text
    text_rect = text_surface.get_rect(center = (CENTER[0], CENTER[1] + 300))

    # Display the text onto the bottom of the screen
    screen.blit(text_surface, text_rect)

    # Draw the border in the center of the screen
    pygame.draw.circle(screen, (255, 255, 255), (border.center[0], border.center[1]), border.radius, border.width)

    # Traverse through the Balls array
    for ball in balls:
        # Apply Gravity
        ball.vel[1] += gravity
        ball.pos[1] += ball.vel[1]
        ball.pos[0] += ball.vel[0]

        # Calculate the distance from the center of the border to the ball
        dist = math.sqrt((ball.pos[0] - border.center[0]) ** 2 + (ball.pos[1] - border.center[1]) ** 2)

        # Dectect Collisions
        if dist + ball.radius >= border.radius:
            # Reflect the velocity (bounce) by using normal
            norm = [(ball.pos[0] - border.center[0]) / dist, (ball.pos[1] - border.center[1]) / dist]
            speed_dot_norm = ball.vel[0] * norm[0] + ball.vel[1] * norm[1]
            ball.vel[0] -= 2 * speed_dot_norm * norm[0]
            ball.vel[1] -= 2 * speed_dot_norm * norm[1]

            # Increase the radius of the ball
            ball.radius += 10

            # TODO Add sound when the ball hits the border

            #Reset the ball position
            ball.pos[0] = border.center[0] + norm[0] * (border.radius - ball.radius)
            ball.pos[1] = border.center[1] + norm[1] * (border.radius - ball.radius)
            collisions += 1

        # Draw the ball
        pygame.draw.circle(screen, ball.color, (ball.pos[0], ball.pos[1]), ball.radius)

    # Update the display
    pygame.display.update()

    # Limit the frame rate to 60 FPS
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()