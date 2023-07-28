import pygame
from constants import *
from player import Player
from enemy import Undead
from sword import Sword
from drop import Drop
from utils import draw_text
from weapon import Weapon
from walls import Wall
from GameStateManager import GameStateManager
from inventory import Inventory
import pygame_gui
world_width = 2576
world_height = 2924



def camera_offset(player):
    # This will keep the player at the center of the screen
    offset_x = -player.rect.centerx + SCREEN_WIDTH // 2
    offset_y = -player.rect.centery + SCREEN_HEIGHT // 2
    
    # Check if the camera is out of the world's bounds and adjust it if necessary
    offset_x = min(0, offset_x)  # left side
    offset_y = min(0, offset_y)  # top side
    offset_x = max(-(world_width - SCREEN_WIDTH), offset_x)  # right side
    offset_y = max(-(world_height - SCREEN_HEIGHT), offset_y)  # bottom side

    return offset_x, offset_y


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    game_state_manager = GameStateManager(screen)
    game_state_manager.start_screen()

    inventory = Inventory()
    # Group for all sprites
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    weapons = pygame.sprite.Group()
    drops = pygame.sprite.Group()
    

    # Load images
    spritesheet = pygame.image.load('defaultChar.png')
    undead_spritesheet = pygame.image.load('decayingSkeleton.png')
    background = pygame.image.load('befallen_Beta2.png')
    item_spritesheet = pygame.image.load('items.png')

    
    player = Player(spritesheet)
    player.equipped_weapon = Sword
    all_sprites.add(player)

    undead = Undead.create_undeads(player,undead_spritesheet)
    undead.player = player
    all_sprites.add(undead)
    enemies.add(undead)

   
    walls = Wall.create_walls()
    all_sprites.add(walls)

   

    enemy_timer = 0

    running = True
    pygame.mixer.init()
    audio_file_path = 'E:/gameMusic/NGGYU.wav'
    pygame.mixer.music.load(audio_file_path)

# Set the volume of the music to 25% of its current volume
    pygame.mixer.music.set_volume(0.10)

# Play the music
    pygame.mixer.music.play()
    
    while running:
        events = pygame.event.get()  # store the events in a variable
        game_state_manager.handle_events(pygame.event.get())
        offset_x, offset_y = camera_offset(player)
        
        screen.blit(background, (offset_x, offset_y))
        
        if inventory.inventory_open:
            inventory.inventory_screen.fill((0, 0, 0, 128))  # Clear the inventory screen and fill with a semi-transparent black color
            player.inventory.draw(inventory.inventory_screen)  # Draw the inventory
            screen.blit(inventory.inventory_screen, (0, SCREEN_HEIGHT-inventory.inventory_screen.get_height()))  # Draw the inventory screen over the game screen
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if player.equipped_weapon is not None:  # Press space to attack
                        weapon = player.equipped_weapon(player)
                        all_sprites.add(weapon)
                        weapons.add(weapon)  # Add sword to swords group
                if event.key == pygame.K_i:
                    inventory.inventory_open = not inventory.inventory_open
            if event.type == pygame.MOUSEBUTTONDOWN and inventory.inventory_open:
            # Get the clicked item
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_item_index = mouse_x // 64  # Get the index of the clicked item (assuming items are 64x64 pixels)
                clicked_item = player.inventory.get_item(clicked_item_index)
                if clicked_item is not None:
                    player.equip(clicked_item)
          
        # Spawn enemies
        enemy_timer += 1
        if enemy_timer >= ENEMY_SPAWN_RATE:
            if len(enemies) == 0:  # Check if all enemies have been destroyed
                undead = Undead.create_undeads(player,undead_spritesheet)
                undead.player = player  # Set the player for each undead
                all_sprites.add(undead)  # Add each undead to all_sprites
                enemies.add(undead)  # Add each undead to enemies
            enemy_timer = 0

        
        # Update sprites
        for sprite in all_sprites:
            if isinstance(sprite, Undead):
                sprite.update(walls=walls, enemies=enemies)
            elif sprite != player:
                sprite.update()
        player.update(enemies,walls)


        drop_collisions = pygame.sprite.spritecollide(player,drops,False)
        for drop in drop_collisions:
            distance = pygame.math.Vector2(drop.rect.center).distance_to(player.rect.center)
            if distance < 10:  # PICKUP_RADIUS is the distance within which the player can pick up drops
                player.pick_up(drop)
        # Check for collisions between player and enemies
        collisions = pygame.sprite.spritecollide(player, enemies, False)
        for enemy in collisions:
            if enemy.state == 'attack':
                enemy.attack(player)
            

        # Weapon and enemies collision
        hits = pygame.sprite.groupcollide(weapons, enemies, True, True)
        for hit in hits:
            drop = Drop(hit.rect.x, hit.rect.y)
            all_sprites.add(drop)
            drops.add(drop)  # Add drop to drops group

        # Check player's health
        if player.health <= 0 and not player.is_dead:
                player.is_dead = True
                player.current_animation = player.animations['death']['die'] 

        if player.is_dead:
            player.current_animation.update(True)

        # Draw everything
        for sprite in all_sprites:
            if inventory.inventory_open:
                screen.blit(inventory.inventory_screen, (0, SCREEN_HEIGHT-inventory.inventory_screen.get_height()))
            sprite.draw(screen, offset_x, offset_y)
        # Draw health bar
        health_bar_width = PLAYER_HEALTH * 2
        pygame.draw.rect(screen, GREEN, (20, 20, player.health*2, 20))
        pygame.draw.rect(screen, WHITE, (20, 20, PLAYER_HEALTH * 2, 20), 2)

        pygame.display.flip()
        clock.tick(FPS)

        if player.is_dead and player.is_death_animation_finished():
            draw_text(screen, "YOU DIED",50,SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

    game_state_manager.game_over_screen()
    pygame.quit()

if __name__ == "__main__":
    while True:
        main()
