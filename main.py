import sys
import arcade

#------------------- CONSTANTS -------------------#

PLAYER_SCALING = 0.65
ALIEN_SCALING = 0.6

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Alien Invasion - Python Arcade"

MOVEMENT_SPEED = 300
BULLET_SPEED = 300

# -----------------------------------------------#

# --------------------------------------- Classes --------------------------------------- #


#------------------- Player Class -------------------#
class Player(arcade.Sprite):
    """Player spaceship at the bottom of the screen."""
    def __init__(self, image, scale):
        super().__init__(image, scale)
        # Shoot cooldown timer
        self.shoot_cooldown = 0
        self.can_shoot = True

    def update(self, delta_time: float = 1/60):
        """Move the player ship and keep it on screen."""
        # Move player.
        self.center_x += self.change_x * MOVEMENT_SPEED * delta_time
        
        # Update shoot cooldown timer
        if not self.can_shoot:
            self.shoot_cooldown -= delta_time
            if self.shoot_cooldown <= 0:
                self.can_shoot = True

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > WINDOW_WIDTH - 1:
            self.right = WINDOW_WIDTH - 1

    
    def shoot_bullet(self):
        """Shoot a bullet from player ship."""
        if self.can_shoot:
            # Create a bullet instance
            bullet = Bullet(self.center_x, self.top)
            # Reset shoot cooldown
            self.can_shoot = False
            self.shoot_cooldown = 0.3  # 0.3 seconds between shots
            return bullet
        else:
            return None

#-----------------------------------------------------#

#------------------- Bullet Class -------------------#
class Bullet(arcade.Sprite):
    """Bullet fired from the player ship."""
    def __init__(self, x, y):
        super().__init__("assets/bullet.png", scale=0.8)
        self.center_x = x
        self.center_y = y
        self.change_y = BULLET_SPEED

    def update(self, delta_time: float = 1/60):
        """Move the bullet upwards and remove it if it goes off screen."""
        self.center_y += self.change_y * delta_time

        # Remove the bullet if it goes off screen
        if self.bottom > WINDOW_HEIGHT:
            self.remove_from_sprite_lists()

#-----------------------------------------------------#

#------------------- Game View Class -------------------#
class GameView(arcade.View):
    """Main game class."""

    def __init__(self):
        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists
        self.player_list = None
        self.alien_list = None
        self.player_bullet_list = None

        # Set up the player info
        self.player_sprite = None
        # Set up the alien info
        self.alien_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False

        # Set the background image
        self.background_img = arcade.load_texture("assets/bg2.jpg")

    def setup(self):
        """Set up the game and initialize the player and alien fleet."""

        # ------------ Sprite lists ------------ #
        self.player_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()

        # ------------ Set up player sprite ------------ #
        self.player_sprite = Player(
            "assets/ship1.png",
            scale=PLAYER_SCALING,
        )
        self.player_sprite.center_x = WINDOW_WIDTH // 2
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)


        # ------------ Set up alien sprite ------------ #
        self.alien_sprite = arcade.Sprite("assets/top-alien.png", scale=ALIEN_SCALING)
        self.alien_sprite.center_x = WINDOW_WIDTH // 2
        self.alien_sprite.center_y = WINDOW_HEIGHT // 2
        self.alien_list.append(self.alien_sprite)

    def on_draw(self):
        """Render the screen."""
        # Clear the screen
        self.clear()

        # Draw the background image
        arcade.draw_texture_rect(
            self.background_img,
            arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
            alpha=135,
        )
        # Draw all the sprites.
        self.player_list.draw()
        self.alien_list.draw()
        self.player_bullet_list.draw()

    def update_player_direction(self):
        """Update the player's horizontal direction based on keys pressed.
        - `-1` = left
        - `1` = right
        - `0` = no movement"""
        # Calculate speed based on the keys pressed
        # change_x = direction, -1 = left; 1 = right
        self.player_sprite.change_x = 0

        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -1
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = 1

    def on_update(self, delta_time):
        """Movement and game logic"""
        # Call update to move the sprite
        # If using a physics engine, call update player to rely on physics engine
        # for movement, and call physics engine here.
        self.player_list.update(delta_time)
        self.player_bullet_list.update(delta_time)
        for bullet in self.player_bullet_list:
            hits = arcade.check_for_collision_with_list(bullet, self.alien_list)
            for alien in hits:
                alien.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        # ---- Handle player movement ---- #
        if key == arcade.key.A:
            self.left_pressed = True
            self.update_player_direction()
        elif key == arcade.key.D:
            self.right_pressed = True
            self.update_player_direction()

        # ---- Handle shooting ---- #
        elif key == arcade.key.SPACE:
            # Add the bullet to the player's bullet list
            bullet = self.player_sprite.shoot_bullet()
            if bullet:
                self.player_bullet_list.append(bullet)
        
        # ---- Handle quitting the game ---- #
        if key == arcade.key.ESCAPE:
            arcade.close_window()
            sys.exit()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.A:
            self.left_pressed = False
            self.update_player_direction()
        elif key == arcade.key.D:
            self.right_pressed = False
            self.update_player_direction()

# -----------------------------------------------------------------------#


# ------------------- Main Function -------------------#
def main():
    """Main function"""
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create and setup the GameView
    game = GameView()
    game.setup()

    # Show GameView on screen
    window.show_view(game)

    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()