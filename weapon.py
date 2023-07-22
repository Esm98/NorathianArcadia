import pygame
class Weapon(pygame.sprite.Sprite):
    def __init__(self, player,lifetime):
        super().__init__()

        # Each weapon will have its own image, rect, and lifetime attributes.
        self.image = None
        self.rect = None
        self.lifetime = lifetime
        self.player = player

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()