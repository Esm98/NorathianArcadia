import pygame
from constants import *
import random

class Drop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((DROP_SIZE, DROP_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.loot = random.choice(LOOT)
        self.hitbox = self.image.get_rect().inflate(-10, +10)  # Add this line

    #def draw(self, surface):
        #surface.blit(self.image,self.rect)
    def draw(self, surface, offset_x, offset_y):
        surface.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))
        pygame.draw.rect(surface, BLUE, self.hitbox.move(offset_x, offset_y), 2)
