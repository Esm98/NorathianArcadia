import pygame
import random
from constants import *
from animation import Animation
from player import Player
from random import choice, randint
from pygame.math import Vector2
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self,spritesheet,x,y,player):
        super().__init__()
        self.spritesheet = spritesheet
        self.x = x
        self.y = y
        self.image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        self.image.fill(RED)
        self.rect = pygame.Rect(self.x, self.y, 64, 64)  # Assuming the animation frame size is 64x64
        self.hitbox = self.image.get_rect().inflate(-10, +10)  # Decrease the size of the hitbox by 10 pixels on each side



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

        #attacking
        self.damage = 10
        self.last_attack_time = pygame.time.get_ticks()
        self.attack_delay = 2000
        self.is_attacking = False
        self.attack_timer = 0

    @staticmethod
    def get_direction_from_vector(vector):
        angles = {'down': 90, 'left': 180, 'up': -90, 'right': 0}
        vx, vy = vector
        angle = (180 / math.pi) * math.atan2(vy, vx)
        return min(angles.items(), key=lambda item: abs(item[1] - angle))[0]


    def attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > self.attack_delay:
            self.is_attacking = True  # This was originally mis-capitalized
            self.attack_timer = pygame.time.get_ticks()  # start the timer when we attack
            player.health -= self.damage
            print("Enemy Attacked!")
            self.last_attack_time = current_time
        else:
            if pygame.time.get_ticks() - self.attack_timer > len(self.current_animation.frames) * self.current_animation.frame_delay:  # Reset is_attacking when the animation has played
                self.is_attacking = False
                print("attack delay not over yet")



    
    def update_image(self,player=None):
        self.current_animation.update(True)
        self.image = self.current_animation.frames[self.current_animation.current_frame]
        self.rect = self.image.get_rect(center=self.rect.center)  # Update the rect to match the image's size and position

    #def draw(self, surface):
        #surface.blit(self.image, self.rect)
        #pygame.draw.rect(surface, BLUE,self.hitbox,2)

    def draw(self, surface, offset_x, offset_y):
        surface.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))
        pygame.draw.rect(surface, RED, self.hitbox.move(offset_x, offset_y), 2)


class Undead(Enemy):
    def __init__(self, spritesheet, x, y,player):
        super().__init__(spritesheet, x, y,player)
        
        self.state = 'patrol'
        self.directions = ['up','down',
                           'left','right']
        self.direction = choice(self.directions)
        self.rect.topleft = (x, y)  # Update the position of the rectangle

        self.agro_radius = 200
        self.damage = 10
        self.player = player
        self.patrol_counter = 0
        self.attack_delay = 2000
       


    def update(self):  # Pass player instance for distance calculation
        if self.player is not None:
            player_position = Vector2(self.player.rect.x, self.player.rect.y)
            self_position = Vector2(self.rect.x, self.rect.y)

            # Check distance to player
            if player_position.distance_to(self_position) <= self.agro_radius:
                self.state = 'attack'
            else:
             self.state = 'patrol'

        if self.state == 'patrol':
            if self.direction == 'up':
                self.rect.y -= ENEMY_SPEED
            elif self.direction == 'down':
                self.rect.y += ENEMY_SPEED
            elif self.direction == 'left':
                self.rect.x -= ENEMY_SPEED
            elif self.direction == 'right':
                self.rect.x += ENEMY_SPEED

            # Randomly change patrol direction
            if randint(1, 100) <= 3:  # 3% chance to change direction each frame
                self.direction = choice(self.directions)

            self.current_animation = self.animations['walk'][self.direction]

        elif self.state == 'attack':
        # Move towards player
            direction_vector = (player_position - self_position)
            if direction_vector.length() > 0:  # Only normalize if the vector is not a zero vector
                direction_vector = direction_vector.normalize()
            


            self.direction = Enemy.get_direction_from_vector(direction_vector)

            # Attack player if close enough (assuming rect is the hit box)
            if self.rect.colliderect(self.player.rect):  # Shrink player's rect to prevent overlap
                self.attack(self.player)  # Call the attack method
            else:
                self.rect.x += direction_vector.x * ENEMY_SPEED
                self.rect.y += direction_vector.y * ENEMY_SPEED

            if self.is_attacking:  # Check if we are attacking
                self.current_animation = self.animations['swing'][self.direction]
            else:
                self.current_animation = self.animations['walk'][self.direction]

            self.current_animation.update(True)

        # Update self.rect to match the image's size and position
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.hitbox.center = self.rect.center

        self.update_image()