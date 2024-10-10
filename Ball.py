import random
import math

#Define Ball class
class Ball:
    #Constructor
    def __init__(self, border):
        self.border = border
        self.pos = [self.random_Xpos(), self.random_Ypos()] # Initial position
        self.radius = random.randint(10, 30) # Ball's radius
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255)) # Ball's color
        self.vel = [0, 0] # Initial velocity

    # Ball Methods
    def random_Xpos(self):
        # Generate a random radius (between 0 and the border's radius)
        r = random.uniform(0, self.border.radius - 10)
    
        # Generate a random angle in radians (0 to π for the upper half-circle)
        angle = random.uniform(math.pi, 2 * math.pi)
    
        # Convert polar coordinates to Cartesian x
        x = r * math.cos(angle)

        # Adjust x to the center
        x += self.border.center[0]

        return int(x)

    def random_Ypos(self):
        # Generate a random radius (between 0 and the border's radius)
        r = random.uniform(0, self.border.radius - 10)
    
        # Generate a random angle in radians (0 to π for the upper half-circle)
        angle = random.uniform(math.pi, 2 * math.pi)
    
        # Convert polar coordinates to Cartesian y
        y = r * math.sin(angle)
    
        # Adjust y to the center
        y += self.border.center[1]

        return int(y)