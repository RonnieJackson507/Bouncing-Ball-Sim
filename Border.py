import pygame

class Border:
    def __init__(self, x, y, radius, width):
        self.radius = radius # Border's Radius
        self.width = width # Width of the border
        self.center = [x, y] # Position of the center of the border

    # Methods:
    #Draw the border relative to the center of the screen
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.center[0], self.center[1]), self.radius, self.width)