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
            },
            'idle': {
                'up': Animation(spritesheet,0, 8, 1),
                'down': Animation(spritesheet,0, 10, 1),
                'left': Animation(spritesheet,0, 9, 1),
                'right': Animation(spritesheet,0, 11, 1)
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
            #print("Enemy Attacked!")
            self.last_attack_time = current_time
        else:
            if pygame.time.get_ticks() - self.attack_timer > len(self.current_animation.frames) * self.current_animation.frame_delay:  # Reset is_attacking when the animation has played
                self.is_attacking = False
                #print("attack delay not over yet")



    
    def update_image(self,player=None):
        self.current_animation.update(True)
        self.image = self.current_animation.frames[self.current_animation.current_frame]
        self.rect = self.image.get_rect(center=self.rect.center)  # Update the rect to match the image's size and position

    #def draw(self, surface):
        #surface.blit(self.image, self.rect)
        #pygame.draw.rect(surface, BLUE,self.hitbox,2)

    def draw(self, surface, offset_x, offset_y):
        surface.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))
        pygame.draw.rect(surface, BLUE, self.hitbox.move(offset_x, offset_y), 2)


class Undead(Enemy):
    dead_enemies = 0
    def __init__(self, spritesheet, x, y,player,can_patrol=True):
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

        self.world_width = 2213
        self.world_height = 2924
        self.patrol_direction = Vector2(1, 0)  # Initially move to the right
        self.patrol_distance = 0  # Initially we haven't moved yet
        self.can_patrol = can_patrol
    def create_undeads(player, undead_spritesheet):
        undeads = pygame.sprite.Group()

        

        undead1 = Undead(undead_spritesheet, 1597, 2815, player,can_patrol = True)  
        undead2 = Undead(undead_spritesheet, 1720, 2326, player,can_patrol= False)  
        undead3 = Undead(undead_spritesheet, 1711, 2149, player,can_patrol = False) 
        undead4 = Undead(undead_spritesheet, 1860, 2400, player,can_patrol = False)  

        undeads.add(undead1)
        undeads.add(undead2)
        undeads.add(undead3)
        undeads.add(undead4)

        return undeads



    def update(self,walls = None,enemies = None):  # Pass player instance for distance calculation
        if self.player is not None:
            player_position = Vector2(self.player.rect.x, self.player.rect.y)
            self_position = Vector2(self.rect.x, self.rect.y)

            distance_to_player = player_position.distance_to(self_position)
            

            # Check distance to player
            if distance_to_player <= self.agro_radius:
                #print('Now in Attack state')
                self.state = 'attack'
            else:
                #print('Now in Patrol state')
                self.state = 'patrol'
        if self.state == 'patrol':
            if not self.can_patrol:
                self.current_animation = self.animations['idle'][self.direction]  # Use the walk animation as the idle animation
                self.current_animation.current_frame = 0 # Set the frame to the first frame
                self.update_image()  # Only patrol if the enemy can patrol
                return


            self.state == 'patrol'
            old_x, old_y = self.rect.x, self.rect.y
            self.rect.x += self.patrol_direction.x * ENEMY_SPEED
            self.rect.y += self.patrol_direction.y * ENEMY_SPEED

            self.patrol_distance += ENEMY_SPEED
            if self.patrol_distance >= PATROL_LIMIT:
                # If we've moved far enough, switch direction and reset distance
                self.patrol_direction *= -1
                self.patrol_distance = 0


            if self.direction == 'up':
                self.rect.y -= ENEMY_SPEED
            elif self.direction == 'down':
                self.rect.y += ENEMY_SPEED
            elif self.direction == 'left':
                self.rect.x -= ENEMY_SPEED
            elif self.direction == 'right':
                self.rect.x += ENEMY_SPEED

             # Check for collisions
            if not any(self.rect.colliderect(enemy.hitbox) for enemy in enemies):
                self.rect.x, self.rect.y = old_x, old_y
                self.state = 'patrol'
            if any(self.rect.colliderect(wall.rect) for wall in walls):
                self.rect.x, self.rect.y = old_x, old_y   

            # Randomly change patrol direction
            if randint(1, 100) <= 3:  # 3% chance to change direction each frame
                self.direction = choice(self.directions)

            self.current_animation = self.animations['walk'][self.direction]
            self.current_animation.update(True)
        elif self.state == 'attack':
        # Move towards player
            old_x, old_y = self.rect.x, self.rect.y
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

            if any(self.rect.colliderect(enemy.hitbox) for enemy in enemies if enemy != self) or \
            any(self.rect.colliderect(wall.rect) for wall in walls):
                self.rect.x, self.rect.y = old_x, old_y  # Move back to the old position

            # Check for boundaries
            self.rect.x = max(0, min(self.rect.x, self.world_width - self.rect.width))
            self.rect.y = max(0, min(self.rect.y, self.world_height - self.rect.height))

            if self.is_attacking:  # Check if we are attacking
                self.current_animation = self.animations['swing'][self.direction]
            else:
                self.current_animation = self.animations['walk'][self.direction]

            self.current_animation.update(True)

        # Update self.rect to match the image's size and position
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.hitbox.center = self.rect.center

        self.update_image()