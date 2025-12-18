import arcade


class HitSplat(arcade.Sprite):
    """Class to represent a hitsplat when an enemy or player is hit."""

    def __init__(self, position_x, position_y):
        """Initialize the hitsplat"""
        # Call the parent Sprite constructor
        super().__init__("assets/Sprite-Hitsplat.png", scale=1)

        # Set the position
        self.center_x = position_x
        self.center_y = position_y

        # Set a timer for how long the hitsplat should be visible
        self.lifetime = 0.06  # seconds
        self.elapsed_time = 0.0

    def update(self, delta_time: float = 1 / 60):
        """Update the hitsplat's lifetime"""
        self.elapsed_time += delta_time
        if self.elapsed_time >= self.lifetime:
            self.remove_from_sprite_lists()