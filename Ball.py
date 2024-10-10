import random
import math

#Define Ball class
class Ball:
    #Constructor
    def __init__(self, border, color):
        self.border = border
        self.posX = self.random_Xpos() # Ball's X position
        self.posY = self.random_Ypos() # Ball's Y position
        self.radius = 10 # Ball's radius
        self.color = color # Ball's color
        self.velY = 0 # Initial vertical velocity
        self.velX = 0 # Initial horizontal velocity

    # Definitions for functions
    def random_Xpos(self):
        # Generate a random radius (between 0 and the border's radius)
        r = random.uniform(0, self.border.radius)
    
        # Generate a random angle in radians (0 to π for the upper half-circle)
        angle = random.uniform(math.pi, 2 * math.pi)
    
        # Convert polar coordinates to Cartesian x
        x = r * math.cos(angle)

        # Adjust x to the center
        x += self.border.x

        return int(x)

    def random_Ypos(self):
        # Generate a random radius (between 0 and the border's radius)
        r = random.uniform(0, self.border.radius)
    
        # Generate a random angle in radians (0 to π for the upper half-circle)
        angle = random.uniform(math.pi, 2 * math.pi)
    
        # Convert polar coordinates to Cartesian y
        y = r * math.sin(angle)
    
        # Adjust y to the center
        y += self.border.y - 60

        return int(y)