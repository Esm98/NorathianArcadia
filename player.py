import pygame
from constants import *
from animation import Animation

class Player(pygame.sprite.Sprite):
    def __init__(self, spritesheet):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        self.health = PLAYER_HEALTH
        self.attack = PLAYER_ATTACK
        self.defense = PLAYER_DEFENSE
        
        self.direction = 'down'
        self.is_moving = False

        self.animations = {
            'walk': {
                'up': Animation(spritesheet,8, 0, 8),
                'down': Animation(spritesheet,10, 0, 8),
                'left': Animation(spritesheet,9, 0, 8),
                'right': Animation(spritesheet,11, 0, 8)
            },
            'attack': {
                'up': Animation(spritesheet,1, 0, 4),
                'down': Animation(spritesheet,1, 1, 4),
                'left': Animation(spritesheet,1, 2, 4),
                'right': Animation(spritesheet,1, 3, 4)
            }
        }

        self.current_animation = self.animations['walk']['down']  # Initial animation

    def update(self):
        keys = pygame.key.get_pressed()
        self.is_moving = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]

        if self.is_moving:
            if keys[pygame.K_SPACE]:
                self.current_animation = self.animations['attack'][self.direction]
            else:
                self.current_animation = self.animations['walk'][self.direction]

            if keys[pygame.K_LEFT]:
                self.rect.x -= PLAYER_SPEED
                self.direction = 'left'
                self.is_moving = True
            if keys[pygame.K_RIGHT]:
                self.rect.x += PLAYER_SPEED
                self.direction = 'right'
                self.is_moving = True
            if keys[pygame.K_UP]:
                self.rect.y -= PLAYER_SPEED
                self.direction = 'up'
                self.is_moving = True
            if keys[pygame.K_DOWN]:
                self.rect.y += PLAYER_SPEED
                self.direction = 'down'
                self.is_moving = True

        self.current_animation.update(self.is_moving)

    def draw(self, surface):
        self.current_animation.draw(surface, self.rect.x, self.rect.y)
