import pygame
from constants import *
import random

class Drop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image,self.name = self.create_item()
        self.rect = self.image.get_rect(center=(x, y))
        self.loot = random.choice(LOOT)
        self.hitbox = self.image.get_rect().inflate(-20, -20)
        


    #def draw(self, surface):
        #surface.blit(self.image,self.rect)
    def draw(self, surface, offset_x, offset_y):
        surface.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))
        pygame.draw.rect(surface, BLUE, self.hitbox.move(offset_x, offset_y), 2)
    
    def create_item(self):
        items = ['helmet.png', 'chestPlate.png', 'arms.png', 'legs.png', 'longSword.png']
        chosen_item = random.choice(items)
        print(chosen_item)
        try:
            image = pygame.image.load(chosen_item)
        except pygame.error as e:
            print(f"Unable to load image: {chosen_item}")
            print(e)
            image = pygame.Surface((0, 0))  # return an empty surface in case of an error

        return image, chosen_item.split('.')[0] # returns the item name without the .png extension