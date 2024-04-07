import pygame
white = (255, 255, 255)

class Block(pygame.sprite.Sprite):
    def __init__(self, colour, width, height, speed):
        # Initialise attributes
        super().__init__()
        self.colour = colour
        self.width = width
        self.height = height + 2
        self.speed = speed
        self.landed = True
        self.counted = False
        self.first = False
        
        # Create surface
        self.image = pygame.Surface([width, height + 2])
        self.image.fill(white)
        self.image.set_colorkey(white)
        
        # Draw block
        pygame.draw.rect(self.image, self.colour, [0, 1, self.width, self.height])
        
        # Get rect object
        self.rect = self.image.get_rect()
        
    def moveLeft(self, speed):
        self.rect.x -= self.speed
        
    def jump(self):
        self.speed += 10
        self.landed = False
    
    def moveUp(self, speed):
        self.rect.y -= self.speed
    
    def platformCollision(self):
        self.speed = 0