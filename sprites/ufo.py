import arcade
from settings import WINDOW_WIDTH, WINDOW_HEIGHT


class UFO(arcade.Sprite):
    """UFO that occasionally flies across the top of the screen."""
    def __init__(self, direction):
        super().__init__("assets/Sprite-UFO.png", scale=1)
        self.speed = 100  # Speed of UFO
        self.direction = direction  # 1 for right, -1 for left

        if direction == 1:
            self.center_x = 0  # Start from left
        else:
            self.center_x = WINDOW_WIDTH  # Start from right
        self.center_y = WINDOW_HEIGHT - 40  # Near top of screen

    def update(self, delta_time: float = 1/60):
        """Move the UFO across the screen."""
        self.center_x += self.direction * self.speed * delta_time
        # Remove UFO if it goes off-screen
        if self.direction == 1 and self.left > WINDOW_WIDTH:
            self.remove_from_sprite_lists()
        elif self.direction == -1 and self.right < 0:
            self.remove_from_sprite_lists()
