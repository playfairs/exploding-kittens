import arcade
from systems.spawner import KittenSpawner

class Game(arcade.Window):
    def __init__(self, selected_skin="black"):
        super().__init__(800, 600, "Exploding Kittens")

        self.kittens = arcade.SpriteList()
        self.spawner = KittenSpawner(selected_skin)
        self.exploded_count = 0
        self.defused_count = 0
        self.start_time = 0
        self.score = 0
        self.game_over = False
        self.MAX_EXPLODED = 3
        
        self.spawn_timer = 0
        self.spawn_interval = 3.0
        
        self.ui_text = arcade.Text(
            f"Score: {self.score} | Exploded: {self.exploded_count}/{self.MAX_EXPLODED} | Defused: {self.defused_count}",
            10, 10, arcade.color.WHITE, 16
        )
        
        self.game_over_text = arcade.Text(
            "GAME OVER",
            self.width / 2 - 80, self.height / 2,
            arcade.color.RED, 24
        )

    def setup(self):
        """Set up the game after window is created"""
        import time
        self.start_time = time.time()
        for _ in range(3):
            self.kittens.append(self.spawner.spawn(self.width, self.height))

    def on_draw(self):
        self.clear()
        self.kittens.draw()

        self.ui_text.text = f"Score: {self.score} | Exploded: {self.exploded_count}/{self.MAX_EXPLODED} | Defused: {self.defused_count}"
        self.ui_text.draw()

        if self.game_over:
            self.game_over_text.draw()

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.kittens.update(delta_time)
        
        self.spawn_timer += delta_time

        for kitten in list(self.kittens):
            if kitten.exploding:
                if kitten.explosion_frame >= 0.5:
                    self.exploded_count += 1
                    kitten.remove_from_sprite_lists()

        import time
        total_time = time.time() - self.start_time
        self.score = (self.defused_count ** 2) * total_time
        if self.exploded_count >= self.MAX_EXPLODED:
            self.game_over = True
            return

        if self.spawn_timer >= self.spawn_interval:
            if len(self.kittens) < 8:
                self.kittens.append(self.spawner.spawn(self.width, self.height))
            self.spawn_timer = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_over:
            return
            
        hit_list = arcade.get_sprites_at_point((x, y), self.kittens)
        if hit_list:
            kitten = hit_list[0]
            if not kitten.exploding and not kitten.defused:
                kitten.defused = True
                self.defused_count += 1
                kitten.remove_from_sprite_lists()
