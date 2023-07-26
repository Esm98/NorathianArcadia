import pygame
from constants import *
from player import Player
from enemy import Undead
from sword import Sword
from drop import Drop
from utils import draw_text
from weapon import Weapon
from walls import Wall

world_width = 2576
world_height = 2924

def start_screen(screen):
    running = True
    while running:
        screen.fill((0,0,0))  # Fill the screen with black
        draw_text(screen, "Norathian Arcadia", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)  # Draw the title
        draw_text(screen, "Press a key to start", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Draw the instructions
        pygame.display.flip()  # Update the display

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                running = False   

def game_over_screen(screen):
    running = True
    while running:
        screen.fill((0,0,0))  # Fill the screen with black
        draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)  # Draw the game over text
        draw_text(screen, "Press a key to play again", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Draw the instructions
        pygame.display.flip()  # Update the display

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                running = False

#def camera_offset(player):
    # This will keep the player at the center of the screen
    #return -player.rect.centerx + SCREEN_WIDTH // 2, -player.rect.centery + SCREEN_HEIGHT // 2
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

    start_screen(screen)
    
    # Group for all sprites
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    weapons = pygame.sprite.Group()

    # Load images
    spritesheet = pygame.image.load('defaultChar.png')
    undead_spritesheet = pygame.image.load('decayingSkeleton.png')
    background = pygame.image.load('befallen_Beta2.png')

    # Create player and enemies
    player = Player(spritesheet)
    player.equipped_weapon = Sword
    all_sprites.add(player)

    undead = Undead(undead_spritesheet, 100, 100, player)
    undead.player = player
    all_sprites.add(undead)
    enemies.add(undead)

    left = 1171
    top = 2912
    width = 2113 - 1171  # right - left
    height = 5  # since the top and bottom y-coordinate is the same
    walls = pygame.sprite.Group()
    wall = Wall(left, top, width, height)
    walls.add(wall)



    enemy_timer = 0

    running = True
    while running:
        offset_x, offset_y = camera_offset(player)
        #screen.fill((0,0,0))
        # Apply the offset to the background
        screen.blit(background, (offset_x, offset_y))
        #screen.blit(background,(-1500,-1900))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    if player.equipped_weapon is not None:  # Press space to attack
                        weapon = player.equipped_weapon(player)
                        all_sprites.add(weapon)
                        weapons.add(weapon)  # Add sword to swords group

        # Spawn enemies
        enemy_timer += 1
        if enemy_timer >= ENEMY_SPAWN_RATE:
            enemy = Undead(undead_spritesheet, 100, 100, player)
            undead.player = player
            all_sprites.add(undead)
            enemies.add(undead)
            enemy_timer = 0

        # Update sprites
        for sprite in all_sprites:
            if sprite != player:
                sprite.update()
        player.update(enemies,walls)

        # Check for collisions between player and enemies
        collisions = pygame.sprite.spritecollide(player, enemies, False)
        for enemy in collisions:
            if enemy.state == 'attack':
                enemy.attack(player)

        # Weapon and enemies collision
        hits = pygame.sprite.groupcollide(weapons, enemies, True, True)
        for hit in hits:
           # When an enemy is hit, it drops a loot item
            drop = Drop(hit.rect.x, hit.rect.y)
            all_sprites.add(drop)

        # Check player's health
        if player.health <= 0 and not player.is_dead:
                player.is_dead = True
                player.current_animation = player.animations['death']['die'] 

        if player.is_dead:
            player.current_animation.update(True)

        # Draw everything
        for sprite in all_sprites:
            #sprite.draw(screen)
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

    game_over_screen(screen)
    pygame.quit()

if __name__ == "__main__":
    while True:
        main()
