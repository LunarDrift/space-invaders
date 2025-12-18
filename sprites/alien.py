import arcade
from enums.alien_type import AlienType
from sprites.bullet import Bullet
from settings import ALIEN_SCALING, ALIEN_BULLET_SPEED


class Alien(arcade.Sprite):
    """Alien enemy sprite."""
    def __init__(self, alien_type: AlienType):
        self.alien_type = alien_type
        super().__init__(alien_type.texture_path, scale=ALIEN_SCALING * alien_type.scale)
        self.score_value = alien_type.score

    def shoot(self):
        """Alien shoots a bullet downward towards the player."""
        bullet = Bullet(self.center_x, self.bottom)
        bullet.speed = -ALIEN_BULLET_SPEED  # Move downward
        return bullet