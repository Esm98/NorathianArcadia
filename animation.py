import pygame

# Constants
SPRITE_SHEET_PATH = 'defaultChar.png'  # Replace with your sprite sheet path
SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64

# Load the sprite sheet


class Animation:
    def __init__(self, spritesheet, column, row, num_frames,frame_delay=20):
        self.frames = [self.get_sprite(column + i, row, spritesheet) for i in range(num_frames)]
        self.current_frame = 0
        self.frame_delay = frame_delay
        self.tick_count = 0

    def get_sprite(self, x, y, spritesheet):
        rect = pygame.Rect(x * SPRITE_WIDTH, y * SPRITE_HEIGHT, SPRITE_WIDTH, SPRITE_HEIGHT)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)  # Use SRCALPHA to preserve transparency
        image.blit(spritesheet, (0, 0), rect)

        scaled_image = pygame.transform.scale(image, (SPRITE_WIDTH, SPRITE_HEIGHT))  # 2 is the scaling factor

        return scaled_image


    def update(self,is_moving):
        if self.tick_count % self.frame_delay == 0:  # only update frame after frame_delay ticks
            if is_moving:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
            else:
                self.current_frame = 0  # Reset to the first frame if not moving
        self.tick_count += 1  


    def draw(self, surface, x, y):
        surface.blit(self.frames[self.current_frame], (x, y))

   

