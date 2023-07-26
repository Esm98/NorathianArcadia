import pygame
from constants import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height):
        super().__init__()
        self.rect = pygame.Rect(left, top, width, height)
        # Fill with color for visibility, this can be removed later
        self.image = pygame.Surface((width, height))
        self.image.fill(YELLOW)

    def draw(self, surface, offset_x, offset_y):
        surface.blit(self.image, self.rect.move(offset_x, offset_y))

    

