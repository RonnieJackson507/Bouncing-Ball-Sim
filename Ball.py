#Define Ball class
class Ball:
    #Constructor
    def __init__(self, posX, posY, color):
        self.posX = posX # Ball's X position
        self.posY = posY # Ball's Y position
        self.radius = 10 # Ball's radius
        self.color = color # Ball's color
        self.velY = 0 # Initial vertical velocity