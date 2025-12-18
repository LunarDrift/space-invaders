import arcade
from sprites.bullet import Bullet
from settings import ALIEN_SCALING, ALIEN_BULLET_SPEED


class Alien(arcade.Sprite):
    """Alien enemy sprite."""
    def __init__(self):
        super().__init__("assets/Sprite-Alien.png", scale=ALIEN_SCALING)

    def shoot(self):
        """Alien shoots a bullet downward towards the player."""
        bullet = Bullet(self.center_x, self.bottom)
        bullet.speed = -ALIEN_BULLET_SPEED  # Move downward
        return bullet