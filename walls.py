import pygame
from constants import *

class Wall(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height):
        super().__init__()
        self.rect = pygame.Rect(left, top, width, height)
        # Fill with color for visibility, this can be removed later
        self.image = pygame.Surface((width, height))
        self.image.fill(YELLOW)

    def draw(self, surface, offset_x, offset_y):
        surface.blit(self.image, self.rect.move(offset_x, offset_y))

    @staticmethod
    def create_walls():
        walls = pygame.sprite.Group()

        #left = 1171
         #top = 2912
        #width = 2113 - 1171  # right - left
        #height = 5  # since the top and bottom y-coordinate is the same
        #wall2 = Wall(x2, y2, width2, height2)  # Substitute with real values
        # Create Wall instances
        wall1 = Wall(1171, 2915, 2210 - 1235, 1)
        wall2 = Wall(1770, 2650, 2149-1747, 135)  # Substitute with real values
        # Add more walls as needed...
        wall3 = Wall(1810, 2377,1,220)
        wall4 = Wall(1813, 2377,261+45,1)
        wall5 = Wall(1507,0,1,2700)
        wall6 = Wall(2119,2377,1,80)
        wall6 = Wall(1813,2560+64,2113-1813,1)
        wall6 = Wall(1813,2560+64,2160-1813,1)
        wall7 = Wall(2120,2503,1,2584-2503)
        wall8 = Wall(2120,2380,1,50)
        wall9 = Wall(1804, 2191, 2149-1747, 120)
        wall10 = Wall(1171, 2650, 1519-1174+20, 135)  
        wall11 = Wall(1510,1924,1000,1)
        wall12 = Wall(2210, 0, 1, 3000) 
        wall13 = Wall(1171, 2750, 1, 150)
        # Add to the walls group
        walls.add(wall1)
        walls.add(wall2)
        walls.add(wall3)
        walls.add(wall4)
        walls.add(wall5)
        walls.add(wall6)
        walls.add(wall7)
        walls.add(wall8)
        walls.add(wall9)
        walls.add(wall10)
        walls.add(wall11)
        walls.add(wall12)
        walls.add(wall13)
        # Add more walls to the group as needed...

        return walls

