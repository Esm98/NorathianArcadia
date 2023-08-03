import pygame
from constants import *
from animation import Animation
from walls import Wall
from inventory import Inventory
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        world_width = 2576
        world_height = 2924
        player_initial_x = world_width 
        player_initial_y = world_height
        self.equipped_items = []
        spritesheet_name = PLAYER_SPRITESHEETS[','.join(sorted(self.equipped_items))]
        spritesheet = pygame.image.load(spritesheet_name)
        self.image = spritesheet # load the default sprite

        

        
        self.rect = pygame.Rect(player_initial_x, player_initial_y, 64, 64)
        #self.hitbox = self.image.get_rect().inflate(-10, +10)  # Decrease the size of the hitbox by 10 pixels on each side
        self.hitbox = self.rect

        self.health = PLAYER_HEALTH
        self.is_dead = False

        self.attack = PLAYER_ATTACK
        self.defense = PLAYER_DEFENSE
        
        
        self.equipped_weapon = None
        self.equipment = {
            'helmet': False,
            'chestPlate': False,
            'arms': False,
            'legs': False,
            'longSword': False,

        }
        self.direction = 'down'

        self.death_timer = 0
       
        self.inventory = Inventory()
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
                'die': Animation(spritesheet,0, 20, 6,frame_delay=20)
            }

        }
        
        self.current_animation = self.animations['walk']['down']  # Initial animation
    
    def equip(self,item):
        print(f"Equipping item, player object id: {id(self)}")
        if item.name in self.equipped_items:
            return
        self.equipped_items.append(item.name)
        sorted_items = sorted(self.equipped_items)
        spritesheet_name = PLAYER_SPRITESHEETS[','.join(sorted_items)]
        print(f"New spritesheet name: {spritesheet_name}")  # For debugging
        self.image = pygame.image.load(spritesheet_name)
        
        print(f"Equipping item, player object id: {id(self)}")
        print(f"Equipped items: {self.equipped_items}")  # For debugging
        print(f"New image: {self.image}")  # Add this line
        self.animations = {
        'walk': {
            'up': Animation(self.image, 0, 8, 8),
            'down': Animation(self.image, 0, 10, 8),
            'left': Animation(self.image, 0, 9, 8),
            'right': Animation(self.image, 0, 11, 8)
            },
            'swing': {
                'up': Animation(self.image,0, 12, 5),
                'down': Animation(self.image,0, 14, 5),
                'left': Animation(self.image,0, 13, 5),
                'right': Animation(self.image,0, 15, 5)
            },
            'thrust': {
                'up': Animation(self.image,0, 4, 7),
                'down': Animation(self.image,0, 6, 7),
                'left': Animation(self.image,0, 5, 7),
                'right': Animation(self.image,0, 7, 7)
            },
            'shoot': {
                'up': Animation(self.image,0, 16, 12),
                'down': Animation(self.image,0, 18, 12),
                'left': Animation(self.image,0, 17, 12),
                'right': Animation(self.image,0, 19, 12)
            },
            'cast': {
                'up': Animation(self.image,0, 0, 6),
                'down': Animation(self.image,0, 2, 6),
                'left': Animation(self.image,0, 1, 6),
                'right': Animation(self.image,0, 3, 6)
            },
            'death': {
                'die': Animation(self.image,0, 20, 6,frame_delay=20)
            }
        }
        self.current_animation = self.animations['walk']['down']


    def unequip(self, item):
        # Mark this item as unequipped
        self.equipment[item] = False
        self.update_spritesheet()


    def pick_up(self,drop):
        self.inventory.add_item(drop)
        drop.kill()


    def is_death_animation_finished(self):
        if self.is_dead and self.current_animation.current_frame == len(self.current_animation.frames) - 1:
            return True
        return False

    def update(self,enemies=None,walls=None):
        keys = pygame.key.get_pressed()

        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx -= PLAYER_SPEED
            self.direction = 'left'
        if keys[pygame.K_d]:
            dx += PLAYER_SPEED
            self.direction = 'right'
        if keys[pygame.K_w]:
            dy -= PLAYER_SPEED
            self.direction = 'up'
        if keys[pygame.K_s]:
            dy += PLAYER_SPEED
            self.direction = 'down'

        world_width = 2213
        world_height = 2924
        self.rect.x = max(0, min(self.rect.x, world_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, world_height - self.rect.height)) 
        #uncomment for player location
        #print(self.rect.x,self.rect.y)

        # Attempt to move in the X direction
        new_x = self.rect.x + dx
        # Temporarily move player's rect
        old_x = self.rect.x
        self.rect.x = new_x
        # Check for collisions
        collision = any(self.rect.colliderect(enemy.hitbox) for enemy in enemies)
        # If collision occurred, reset x
        if collision:
            self.rect.x = old_x
        # Attempt to move in the Y direction
        new_y = self.rect.y + dy
        # Temporarily move player's rect
        old_y = self.rect.y
        self.rect.y = new_y

        # Check for collisions
        collision_with_enemy = any(self.rect.colliderect(enemy.hitbox) for enemy in enemies)
        collision_with_wall = any(self.rect.colliderect(wall.rect) for wall in walls)

        # If collision occurred, reset position
        if collision_with_enemy or collision_with_wall:
            self.rect.x = old_x
            self.rect.y = old_y

        self.hitbox.center = self.rect.center

        is_attacking = keys[pygame.K_q] or keys[pygame.K_e] or keys[pygame.K_r] or keys[pygame.K_f]
        is_moving = keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]

        if self.is_dead:
            if self.current_animation.current_frame == len(self.current_animation.frames) - 1:
                self.kill()
            else:
                self.current_animation.update(True)
        else:
            if keys[pygame.K_q]:
                self.current_animation = self.animations['swing'][self.direction]
            elif keys[pygame.K_e]:
           
                self.current_animation = self.animations['shoot'][self.direction]
            elif keys[pygame.K_r]:
          
                self.current_animation = self.animations['cast'][self.direction]
            elif keys[pygame.K_f]:
                self.current_animation = self.animations['thrust'][self.direction]
            elif is_moving:
                self.current_animation = self.animations['walk'][self.direction]
            else:
                self.current_animation.update(False)  # Update with is_moving = False

            if self.health <= 0:
                self.is_dead = True
                self.current_animation = self.animations['death']['die']

            self.current_animation.update(is_moving or is_attacking) 

        self.image = self.current_animation.frames[self.current_animation.current_frame]
        self.rect = self.image.get_rect(center=self.rect.center)

    
        
    #def draw(self, surface):
        #surface.blit(self.image, self.rect)
        #pygame.draw.rect(surface,RED, self.hitbox,2)

    def draw(self, surface, offset_x, offset_y):
        
        surface.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))
        #pygame.draw.rect(surface, YELLOW, self.hitbox.move(offset_x, offset_y), 2)
    