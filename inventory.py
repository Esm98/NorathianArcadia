import pygame
class Inventory:
    def __init__(self):
        self.items = []
        self.inventory_open = False
        self.inventory_screen = pygame.Surface((200,200))

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
        else:
            print("Item not found in the inventory")

    def list_items(self):
        for item in self.items:
            print(item)
            
    def get_item(self, index):
        if index < len(self.items):
            return self.items[index]
        else:
            return None
        
    def draw(self, surface):
        for i, item in enumerate(self.items):
            item_x_position = i * 64  # Assume each item is 64x64 pixels and they are arranged in a row
            item_y_position = 0
            surface.blit(item.image, (item_x_position, item_y_position))

