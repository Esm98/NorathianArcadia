import pygame
from constants import *
from player import Player
from enemy import Undead
from sword import Sword
from drop import Drop
from utils import draw_text
from weapon import Weapon
from walls import Wall
class GameStateManager:
    def __init__(self, screen):
        self.screen = screen
        self.state = 'start'  # The initial state of the game

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def update(self):
        if self.state == 'start':
            self.start_screen()
        elif self.state == 'game_over':
            self.game_over_screen()
        # Add additional states as needed

    def start_screen(self):
        
        running = True
        while running:
            self.screen.fill((0,0,0))  # Fill the screen with black
            draw_text(self.screen, "Norathian Arcadia", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)  # Draw the title
            draw_text(self.screen, "Press a key to start", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Draw the instructions
            pygame.display.flip()  # Update the display

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    running = False
                    self.state = 'play'  # Change to the 'play' state when a key is pressed

    def game_over_screen(self):
        running = True
        while running:
            self.screen.fill((0,0,0))  # Fill the screen with black
            draw_text(self.screen, "GAME OVER", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)  # Draw the game over text
            draw_text(self.screen, "Press a key to play again", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Draw the instructions
            pygame.display.flip()  # Update the display

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    running = False
                    self.state = 'start'  # Change back to the 'start' state when a key is pressed