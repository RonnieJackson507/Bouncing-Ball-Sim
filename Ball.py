import random
import math
import pygame

#Define Ball class
class Ball:
    #Constructor
    def __init__(self, border, sound_effect, image):
        self.border = border
        self.pos = [self.random_Xpos(), self.random_Ypos()] # Initial position
        self.radius = random.randint(10, 30) # Ball's radius
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255)) # Ball's color
        self.vel = [0, 0] # Initial velocity
        self.collision = 0 # Initial times of collision
        self.sound_effect = sound_effect # Sound effect of the ball
        self.img = image # Image of the ball

        # Scale the image to the size of the ball (radius)
        if self.img is not None:
            self.img = pygame.transform.scale(self.img, (self.radius, self.radius))

    # Methods:
    # Generate random x position
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

    # Generate random y position
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

    # Draws the Ball
    def draw(self, screen):
        # Draw the image if the user gave one
        if self.img is not None:
            screen.blit(self.img, (self.pos[0], self.pos[1]))
        # Draw a random colored ball if the user did not give an image
        else:
            pygame.draw.circle(screen, self.color, (self.pos[0], self.pos[1]), self.radius)

    # Update the ball bouncing in the border
    def update(self):
        # Physics variables
        gravity = 0.5 # Gravity Constant
        
        # Apply Gravity
        self.vel[1] += gravity
        self.pos[1] += self.vel[1]
        self.pos[0] += self.vel[0]

        # Calculate the distance from the center of the border to the ball
        dist = math.sqrt((self.pos[0] - self.border.center[0]) ** 2 + (self.pos[1] - self.border.center[1]) ** 2)

        # Dectect Collisions
        if dist + self.radius >= self.border.radius:
            # Reflect the velocity (bounce) by using normal
            norm = [(self.pos[0] - self.border.center[0]) / dist, (self.pos[1] - self.border.center[1]) / dist]
            speed_dot_norm = self.vel[0] * norm[0] + self.vel[1] * norm[1]
            self.vel[0] -= 2 * speed_dot_norm * norm[0]
            self.vel[1] -= 2 * speed_dot_norm * norm[1]

            # Increase the radius of the ball
            #ball.radius += 1

            #Reset the ball position
            self.pos[0] = self.border.center[0] + norm[0] * (self.border.radius - self.radius)
            self.pos[1] = self.border.center[1] + norm[1] * (self.border.radius - self.radius)

            if self.sound_effect is not None:  # Check if sound_effect is valid
                self.sound_effect.play()

            # Increase the number of times the ball collide
            self.collision += 1