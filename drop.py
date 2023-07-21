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