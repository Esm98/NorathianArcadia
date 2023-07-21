import pygame
from constants import*
from player import Player
from enemy import Enemy
from sword import Sword
from drop import Drop
from utils import draw_text

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    swords = pygame.sprite.Group()  
    drops = pygame.sprite.Group()  # New group for drops

    spritesheet = pygame.image.load('defaultChar.png')
    player = Player(spritesheet)
    all_sprites.add(player)

    enemy_timer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press space to attack
                    sword = Sword(player)
                    all_sprites.add(sword)
                    swords.add(sword)  # Add sword to swords group

        # Spawn enemies
        enemy_timer += 1
        if enemy_timer >= ENEMY_SPAWN_RATE:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            enemy_timer = 0

        all_sprites.update()

        # Check for collisions between player and enemies
        if pygame.sprite.spritecollide(player, enemies, True):  # True means the enemy sprite will be deleted upon collision
            player.health -= 10  # Arbitrary number, replace with enemy's attack strength minus player's defense, for example
        hits = pygame.sprite.groupcollide(swords, enemies, True, True)
        for hit in hits:
           # When an enemy is hit, it drops a loot item
            drop = Drop(hit.rect.x, hit.rect.y)
            all_sprites.add(drop)
            drops.add(drop) 
        # Check player's health
        if player.health <= 0:
            draw_text(screen, "YOU DIED", 50, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        # Draw everything
        screen.fill((255, 255, 255))
        for sprite in all_sprites:
            sprite.draw(screen)


        # Draw health bar
        pygame.draw.rect(screen, GREEN, (20, 20, player.health, 20))
        pygame.draw.rect(screen, WHITE, (20, 20, PLAYER_HEALTH, 20), 2)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()