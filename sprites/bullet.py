import arcade
from settings import BULLET_SPEED

class Bullet(arcade.Sprite):
    """Bullet fired from the player ship."""
    def __init__(self, x, y):
        super().__init__("assets/bullet.png", scale=1)
        self.center_x = x
        self.center_y = y
        self.speed = BULLET_SPEED