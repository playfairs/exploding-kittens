import random
from game.kitten import Kitten

class KittenSpawner:
    def __init__(self, selected_skin="black"):
        self.selected_skin = selected_skin
        self.spawn_zones = [
            (100, 100),
            (400, 100),
            (700, 100),
            (100, 300),
            (400, 300),
            (700, 300),
            (100, 500),
            (400, 500),
            (700, 500),
        ]
        self.last_zone_index = -1

    def spawn(self, area_width, area_height):
        available_zones = [i for i in range(len(self.spawn_zones)) if i != self.last_zone_index]
        zone_index = random.choice(available_zones)
        self.last_zone_index = zone_index
        
        zone_x, zone_y = self.spawn_zones[zone_index]
        
        x = zone_x + random.randint(-80, 80)
        y = zone_y + random.randint(-80, 80)
        
        x = max(50, min(x, area_width - 50))
        y = max(50, min(y, area_height - 50))
        
        return Kitten(self.selected_skin, x, y)
