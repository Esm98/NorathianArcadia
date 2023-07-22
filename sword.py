import pygame
from constants import *
from weapon import Weapon
class Sword(Weapon):
    def __init__(self, player):
        super().__init__(player, SWORD_LIFETIME)
        self.image = pygame.Surface((SWORD_SIZE, SWORD_SIZE))
        self.image.fill(YELLOW)
        
        if player.direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright)
        elif player.direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft)
        elif player.direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop)
        elif player.direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom)
        self.hit_box = self.rect  # For now, the hit box is the same as the Sword's rect. Modify this as needed.
        self.lifetime = SWORD_LIFETIME

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image,self.rect)