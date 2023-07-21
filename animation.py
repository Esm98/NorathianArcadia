import pygame

# Constants
SPRITE_SHEET_PATH = 'defaultChar.png'  # Replace with your sprite sheet path
SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64

# Load the sprite sheet


class Animation:
    def __init__(self, spritesheet, column, row, num_frames):
        self.frames = [self.get_sprite(column + i, row, spritesheet) for i in range(num_frames)]
        self.current_frame = 0
        self.frame_delay = 0

    def get_sprite(self, x, y, spritesheet):
        rect = pygame.Rect(x * SPRITE_WIDTH, y * SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)  # Use SRCALPHA to preserve transparency
        image.blit(spritesheet, (0, 0), rect)

        scaled_image = pygame.transform.scale(image, (SPRITE_WIDTH*1.5, SPRITE_HEIGHT*1.5))  # 2 is the scaling factor

        return scaled_image


    def update(self,is_moving):
        self.frame_delay = (self.frame_delay + 1) % 5  # Update frame every 5 calls
        if self.frame_delay == 0:
            if is_moving:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
            else:
                self.current_frame = 0  # Reset to the first frame if not moving


    def draw(self, surface, x, y):
        surface.blit(self.frames[self.current_frame], (x, y))

   

