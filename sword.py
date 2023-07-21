import pygame
from constants import *

class Sword(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = pygame.Surface((SWORD_SIZE, SWORD_SIZE))
        self.image.fill(YELLOW)
        
        if player.direction == pygame.K_RIGHT:
            self.rect = self.image.get_rect(midleft=player.rect.midright)
        elif player.direction == pygame.K_LEFT:
            self.rect = self.image.get_rect(midright=player.rect.midleft)
        elif player.direction == pygame.K_UP:
            self.rect = self.image.get_rect(midbottom=player.rect.midtop)
        elif player.direction == pygame.K_DOWN:
            self.rect = self.image.get_rect(midtop=player.rect.midbottom)
        
        self.lifetime = SWORD_LIFETIME

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()