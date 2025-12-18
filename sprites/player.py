import arcade
from sprites.bullet import Bullet
from settings import *


class Player(arcade.Sprite):
    """Player spaceship at the bottom of the screen."""
    def __init__(self):
        super().__init__("assets/Sprite-Ship.png", scale=PLAYER_SCALING)
        # Shoot cooldown timer
        self.shoot_cooldown = 0 # start at 0 so player can shoot immediately
        self.can_shoot = True
        self.speed = MOVEMENT_SPEED

        self.lives = PLAYER_LIVES

    def update(self, delta_time: float = 1/60):
        # Player movement
        self.center_x += self.change_x * self.speed * delta_time
        self.clamp_player_to_screen()
        # Update shoot cooldown timer
        if not self.can_shoot:
            self.shoot_cooldown -= delta_time
            if self.shoot_cooldown <= 0:
                self.can_shoot = True

    
    def shoot_bullet(self):
        """Shoot a bullet from player ship."""
        if self.can_shoot:
            # Create a bullet instance
            bullet = Bullet(self.center_x, self.top)
            # Reset shoot cooldown
            self.can_shoot = False
            self.shoot_cooldown = SHOOT_COOLDOWN
            return bullet
        else:
            return None
        
    def clamp_player_to_screen(self):
        """Keep the player on the screen."""
        if self.left < 0:
            self.left = 0
        elif self.right > WINDOW_WIDTH:
            self.right = WINDOW_WIDTH