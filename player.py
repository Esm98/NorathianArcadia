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
        
        self.equipped_weapon = None

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

    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
            self.direction = 'left'
        if keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
            self.direction = 'right'
        if keys[pygame.K_w]:
            self.rect.y -= PLAYER_SPEED
            self.direction = 'up'
        if keys[pygame.K_s]:
            self.rect.y += PLAYER_SPEED
            self.direction = 'down'
        
        is_attacking = keys[pygame.K_q] or keys[pygame.K_e] or keys[pygame.K_r] or keys[pygame.K_f]
        is_moving = keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]

        if keys[pygame.K_q]:
            self.current_animation = self.animations['swing'][self.direction]
        elif keys[pygame.K_e]:
        # Assuming you have 'shoot' animation
            self.current_animation = self.animations['shoot'][self.direction]
        elif keys[pygame.K_r]:
        # Assuming you have 'cast' animation
            self.current_animation = self.animations['cast'][self.direction]
        elif keys[pygame.K_f]:
            self.current_animation = self.animations['thrust'][self.direction]
        elif is_moving:
            self.current_animation = self.animations['walk'][self.direction]
        else:
            self.current_animation.update(False)  # Update with is_moving = False





        self.current_animation.update(is_moving or is_attacking)  # Now we don't need to pass is_moving

        self.image = self.current_animation.frames[self.current_animation.current_frame]
        self.rect = self.image.get_rect(center=self.rect.center)

        
    def draw(self, surface):
        surface.blit(self.image,self.rect)
