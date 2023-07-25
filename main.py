import pygame
from constants import*
from player import Player
from enemy import Enemy
from sword import Sword
from drop import Drop
from utils import draw_text
from weapon import Weapon
from enemy import Undead
from camera import Camera


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





def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    
    start_screen(screen)

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    swords = pygame.sprite.Group()  
    drops = pygame.sprite.Group()
    weapons = pygame.sprite.Group()
    undeads = pygame.sprite.Group()  # New group for drops

    spritesheet = pygame.image.load('defaultChar.png')
    player = Player(spritesheet)
    player.equipped_weapon = Sword
    all_sprites.add(player)

    undead_spritesheet = pygame.image.load('decayingSkeleton.png')
    undead = Undead(undead_spritesheet, 100, 100, player)
    undead.player = player
    all_sprites.add(undead)
    enemies.add(undead)

    enemy_timer = 0




     
    camera = Camera(512, 512)
    background = pygame.image.load('dungeonFloorTest.png')

    running = True
    while running:
        camera.update(player)
        screen.blit(background,(0,0))
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
            undead_spritesheet = pygame.image.load('decayingSkeleton.png')
            enemy = Undead(undead_spritesheet,100,100,player)
            undead.player = player
            all_sprites.add(undead)
            enemies.add(undead)
            enemy_timer = 0

        player.update(enemies)
        for sprite in all_sprites:
            if sprite == player:
                sprite.update(enemies)
            else:
                sprite.update()

        # Check for collisions between player and enemies
        collisions = pygame.sprite.spritecollide(player, enemies, False)
        for enemy in collisions:
            if enemy.state == 'attack':
                enemy.attack(player)

        hits = pygame.sprite.groupcollide(weapons, enemies, True, True)
        for hit in hits:
           # When an enemy is hit, it drops a loot item
            drop = Drop(hit.rect.x, hit.rect.y)
            all_sprites.add(drop)
            drops.add(drop) 
        # Check player's health
        if player.health <= 0 and not player.is_dead:
                player.is_dead = True
                player.current_animation = player.animations['death']['die'] 


        if player.is_dead:
            player.current_animation.update(True)


        # Draw everything
        #screen.fill((255, 255, 255))
        for sprite in all_sprites:
            sprite.draw(screen)
            
            
        # Draw health bar
        pygame.draw.rect(screen, GREEN, (20, 20, player.health, 20))
        pygame.draw.rect(screen, WHITE, (20, 20, PLAYER_HEALTH, 20), 2)

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