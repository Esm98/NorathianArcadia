import pygame
class Inventory:
    def __init__(self):
        self.items = []
        self.inventory_open = False
        self.inventory_screen = pygame.Surface((400,200))
        self.columns = 5  # the number of columns in the inventory
        self.margin = 5  # the space between the edge of the inventory screen and the grid
        self.item_size = 64  # the size of each inventory slot, set to match your inventory item images
        self.spacing = 5  # the space between each inventory slot

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
        for index, item in enumerate(self.items):
            column = index % self.columns
            row = index // self.columns
        
            # Calculate position of the item
            item_x_position = self.margin + (self.item_size + self.spacing) * column
            item_y_position = self.margin + (self.item_size + self.spacing) * row
            surface.blit(item.image, (item_x_position, item_y_position))

