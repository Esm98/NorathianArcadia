import pygame
from animation import Animation
from enemy import Enemy
class Undead(Enemy):
    def __init__(self, spritesheet, x, y):
        super().__init__(spritesheet, x, y)
        self.state = 'walk'
        self.rect.topleft = (x, y)  # Update the position of the rectangle

    def update(self):
        self.direction = 'down'
        if self.state == 'walk':
            self.current_animation = self.animations['walk'][self.direction]
        elif self.state == 'swing':
            self.current_animation = self.animations['swing'][self.direction]
                
        self.current_animation.update(True)
        self.image = self.current_animation.frames[self.current_animation.current_frame]
        self.update_image()
