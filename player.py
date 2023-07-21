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
        self.move_timer = 0
        self.current_animation = self.animations['walk']['down']  # Initial animation

    def update(self):
        keys = pygame.key.get_pressed()
        
        if self.move_timer > 3:
            self.is_moving = False

        
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
            self.direction = 'left'   
            self.is_moving = True
            self.move_timer = 0
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED
            self.direction = 'right'
            self.is_moving = True
            self.move_timer = 0
        if keys[pygame.K_UP]:
            self.rect.y -= PLAYER_SPEED
            self.direction = 'up'   
            self.is_moving = True
            self.move_timer = 0
        if keys[pygame.K_DOWN]:
            self.rect.y += PLAYER_SPEED
            self.direction = 'down'
            self.is_moving = True
            self.move_timer = 0
            
        if keys[pygame.K_SPACE]:
            self.current_animation = self.animations['attack'][self.direction]
        else:self.current_animation = self.animations['walk'][self.direction]
        self.current_animation.update(not self.is_moving)

        if not self.is_moving:
            self.move_timer +=1

        print(f'Player is moving: {self.is_moving}')

        self.image = self.current_animation.frames[self.current_animation.current_frame]
    def draw(self, surface):
        surface.blit(self.image,self.rect)
