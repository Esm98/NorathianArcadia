import pygame
import random
from constants import *
from animation import Animation

class Enemy(pygame.sprite.Sprite):
    def __init__(self,spritesheet,x,y):
        super().__init__()
        self.spritesheet = spritesheet
        self.x = x
        self.y = y
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.direction = 'down'
        self.animations = {
            'walk': {
                'up': Animation(spritesheet,0, 8, 8),
                'down': Animation(spritesheet,0, 10, 8),
                'left': Animation(spritesheet,0, 9, 8),
                'right': Animation(spritesheet,0, 11, 8)
            },
            'swing': {
                'up': Animation(spritesheet,0, 12, 5),
                'down': Animation(spritesheet,0, 14, 5),
                'left': Animation(spritesheet,0, 13, 5),
                'right': Animation(spritesheet,0, 15, 5)
            },
            'thrust': {
                'up': Animation(spritesheet,0, 4, 7),
                'down': Animation(spritesheet,0, 6, 7),
                'left': Animation(spritesheet,0, 5, 7),
                'right': Animation(spritesheet,0, 7, 7)
            },
            'shoot': {
                'up': Animation(spritesheet,0, 16, 12),
                'down': Animation(spritesheet,0, 18, 12),
                'left': Animation(spritesheet,0, 17, 12),
                'right': Animation(spritesheet,0, 19, 12)
            },
            'cast': {
                'up': Animation(spritesheet,0, 0, 6),
                'down': Animation(spritesheet,0, 2, 6),
                'left': Animation(spritesheet,0, 1, 6),
                'right': Animation(spritesheet,0, 3, 6)
            },
            'death': {
                'die': Animation(spritesheet,0, 20, 5)
            }

        }
        
        self.current_animation = self.animations['walk']['down']  # Initial animation
    

    def update_image(self):
        self.current_animation.update(True)
        self.image = self.current_animation.frames[self.current_animation.current_frame]
        self.rect = self.image.get_rect(center=self.rect.center)  # Update the rect to match the image's size and position

    def draw(self, surface):
        surface.blit(self.image, (self.x,self.y))
