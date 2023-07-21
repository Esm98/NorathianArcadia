import pygame
import random
from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(RED)

        # Spawn enemy on a random edge of the screen
        edge = random.choice(("top", "right", "bottom", "left"))
        if edge == "top":
            self.rect = self.image.get_rect(midbottom=(random.randrange(SCREEN_WIDTH), 0))
        elif edge == "right":
            self.rect = self.image.get_rect(midleft=(SCREEN_WIDTH, random.randrange(SCREEN_HEIGHT)))
        elif edge == "bottom":
            self.rect = self.image.get_rect(midtop=(random.randrange(SCREEN_WIDTH), SCREEN_HEIGHT))
        else:  # edge == "left"
            self.rect = self.image.get_rect(midright=(0, random.randrange(SCREEN_HEIGHT)))

    def update(self):
        self.rect.move_ip(ENEMY_SPEED, 0)  # For simplicity, enemies just move in a straight line for now

    def draw(self, surface):
        surface.blit(self.image, self.rect)
