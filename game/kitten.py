import arcade
import os
import tempfile
import random
import math
from PIL import Image

CAT_SIZE = 32

class Kitten(arcade.Sprite):
    def __init__(self, skin="black", x=0, y=0):
        super().__init__()

        sheet_path = os.path.join("assets", "sprites", "cats", f"{skin}.png")

        try:
            sheet = Image.open(sheet_path)
            sheet_width, sheet_height = sheet.size
            
            self.textures = []
            for row in range(8):
                for col in range(8):
                    x = col * CAT_SIZE
                    y = row * CAT_SIZE
                    
                    sprite_img = sheet.crop((x, y, x + CAT_SIZE, y + CAT_SIZE))
                    
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                        sprite_img.save(tmp.name)
                        texture = arcade.load_texture(tmp.name)
                        self.textures.append(texture)
                        os.unlink(tmp.name)
            
            self.anim_idle   = self.textures[0:4]
            self.anim_sleep  = self.textures[4:8]
            self.anim_roll   = self.textures[8:12]
            self.anim_walk   = self.textures[16:20]
            self.anim_scared = self.textures[24:28]
            
            self.cur_texture = 0
            self.texture = self.anim_idle[self.cur_texture]
            
        except Exception as e:
            self.texture = arcade.load_texture(sheet_path)
            self.textures = [self.texture]
            self.anim_idle = [self.texture]

        self.center_x = x
        self.center_y = y

        self.time = 0
        self.animation_speed = 0.2

        self.exploding = False
        self.time_until_explode = 3.0
        self.defused = False
        
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 50
        self.direction = random.uniform(0, 2 * 3.14159)
        self.change_direction_timer = 2.0
        self.change_direction_interval = 2.0
        
        self.current_state = "walking"
        self.explosion_frame = 0
        self.explosion_speed = 0.1

    def update_animation(self, delta_time=1/60):
        self.time_until_explode -= delta_time
        if self.time_until_explode <= 0 and not self.exploding:
            self.exploding = True
        
        self.update_movement(delta_time)
        
        if self.exploding:
            self.handle_explosion_animation(delta_time)
        else:
            self.handle_normal_animation(delta_time)
    
    def update_movement(self, delta_time):
        if self.exploding or self.defused:
            return
            
        self.change_direction_timer += delta_time
        if self.change_direction_timer >= self.change_direction_interval:
            self.change_direction_timer = 0
            self.direction = random.uniform(0, 2 * 3.14159)
            self.current_state = random.choice(["idle", "walking"])
        
        if self.current_state == "walking":
            self.velocity_x = math.cos(self.direction) * self.speed
            self.velocity_y = math.sin(self.direction) * self.speed
            
            self.center_x += self.velocity_x * delta_time
            self.center_y += self.velocity_y * delta_time
        else:
            self.velocity_x = 0
            self.velocity_y = 0
    
    def handle_normal_animation(self, delta_time):
        if hasattr(self, 'anim_idle') and len(self.anim_idle) > 1:
            self.time += delta_time
            if self.time > self.animation_speed:
                self.time = 0
                
                if self.current_state == "walking" and hasattr(self, 'anim_walk'):
                    self.cur_texture = (self.cur_texture + 1) % len(self.anim_walk)
                    self.texture = self.anim_walk[self.cur_texture]
                else:
                    self.cur_texture = (self.cur_texture + 1) % len(self.anim_idle)
                    self.texture = self.anim_idle[self.cur_texture]
    
    def handle_explosion_animation(self, delta_time):
        self.explosion_frame += delta_time
        if self.explosion_frame < 0.5:
            scale = 1.0 + (self.explosion_frame * 2)
            self.scale = scale
            self.alpha = max(0, 255 - (self.explosion_frame * 500))
