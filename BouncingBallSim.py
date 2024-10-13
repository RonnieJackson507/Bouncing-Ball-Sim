import Ball, Border
import pygame
import tkinter as tk

# TODO Add a way to ask the user to add a sound
# TODO Add a way to add a image to the ball if the User wants it

# Initializes the simulator
def init_sim():
    # Get the number of balls
    balls_num = int(entry_balls.get())

    # Destroy the Menu's window
    root.destroy()

    # Start the simulation
    start_sim(balls_num)

# Starts the simulation
def start_sim(balls_num):  
    # Initialize Pygame
    pygame.init()

    # Create a screen (window) with aspect ration of 9:16
    WIDTH = 400
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
        # Draw the text for the number of balls
        draw_text(f"Balls = {balls_num}", font, (255, 255, 255), screen, CENTER[0], CENTER[1] - 300)

        # Draw the text for the collision
        draw_text(f"Collisions = {collision}", font, (255, 255, 255), screen, CENTER[0], CENTER[1] + 300)

        # Update the display
        pygame.display.update()

        # Limit the frame rate
        pygame.time.Clock().tick(FPS)

    # Quit Pygame
    pygame.quit()

# MENU
# Create the menu window
root = tk.Tk()
root.title("Bouncing Ball Simulator")
root.geometry("300x200")
root.configure(bg="grey")

# Create Input Fields
tk.Label(root, text="Number of Balls:").grid(row=0, column=0, padx=10, pady=5)
entry_balls = tk.Entry(root)
entry_balls.grid(row=0, column=1, padx=10, pady=5)

#Create a button to perform the simulation by quitting the menu
tk.Button(root, text="Simulate Bouncing Balls", command= init_sim).grid(row=6, column=0, columnspan=3, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()