import arcade
import random

#------------------- CONSTANTS -------------------#
# Sprite scaling factors
PLAYER_SCALING = 0.65
ALIEN_SCALING = 0.6
# Window dimensions and title
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Alien Invasion - Python Arcade"
# Player movement and shooting constants
MOVEMENT_SPEED = 300
BULLET_SPEED = 300
SHOOT_COOLDOWN = 0.2  # 0.2 seconds
# Alien fleet configuration
ALIEN_ROWS = 5
ALIEN_COLUMNS = 11
ALIEN_X_SPACING = 60
ALIEN_Y_SPACING = 60
ALIEN_START_X = 100
ALIEN_START_Y = WINDOW_HEIGHT - 70
ALIEN_BULLET_SPEED = 200
ALIEN_SHOOT_COOLDOWN = 3.0  # 3 seconds
MIN_COOLDOWN = 1.0 # Minimum cooldown for alien shooting
MAX_FLEET_SPEED = 100 


# -----------------------------------------------#

# --------------------------------------- Classes --------------------------------------- #


#------------------- Player Class -------------------#
class Player(arcade.Sprite):
    """Player spaceship at the bottom of the screen."""
    def __init__(self):
        super().__init__("assets/ship1.png", scale=PLAYER_SCALING)
        # Shoot cooldown timer
        self.shoot_cooldown = 0 # start at 0 so player can shoot immediately
        self.can_shoot = True
        self.speed = MOVEMENT_SPEED

    def update(self, delta_time: float = 1/60):
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

#-----------------------------------------------------#

#------------------- Bullet Class -------------------#
class Bullet(arcade.Sprite):
    """Bullet fired from the player ship."""
    def __init__(self, x, y):
        super().__init__("assets/bullet.png", scale=0.8)
        self.center_x = x
        self.center_y = y
        self.speed = BULLET_SPEED

#-----------------------------------------------------#

#------------------- Alien Class -------------------#
class Alien(arcade.Sprite):
    """Alien enemy sprite.
    Should be responsible for:
    - Position
    - Size/Sprite
    - Alive/Dead State
    - Drawing itself
    - Moving when told to move"""
    def __init__(self):
        super().__init__("assets/top-alien.png", scale=ALIEN_SCALING)

    def shoot(self):
        """Alien shoots a bullet downward towards the player."""
        bullet = Bullet(self.center_x, self.bottom)
        bullet.speed = -ALIEN_BULLET_SPEED  # Move downward
        return bullet

#------------------- Game View Class -------------------#
class GameView(arcade.View):
    """Main game class."""

    def __init__(self):
        # Call the parent class initializer
        super().__init__()

        # ------------ Sprite lists ------------ #
        self.player_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.alien_bullet_list = arcade.SpriteList()

        # Set up the player info
        self.player_sprite = None

        # Fleet movement info
        self.fleet_direction = 1    # 1 = right; -1 = left
        self.fleet_speed = 40       # pixels per second
        self.fleet_drop = 30        # pixels to drop when changing direction
        self.alien_shoot_timer = ALIEN_SHOOT_COOLDOWN
        self.initial_alien_count = len(self.alien_list)
        self.current_fleet_speed = self.fleet_speed * ((ALIEN_ROWS*ALIEN_COLUMNS) / len(self.alien_list)) if len(self.alien_list) > 0 else self.fleet_speed


        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False

        # Set the background image
        self.background_img = arcade.load_texture("assets/bg2.jpg")

    def setup(self):
        """Set up the game and initialize the player and alien fleet."""
        self.player_list.clear()
        self.alien_list.clear()
        self.player_bullet_list.clear()

        # ------------ Set up player ------------ #
        self.player_sprite = Player()
        self.player_sprite.center_x = WINDOW_WIDTH // 2
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)


        # ------------ Set up aliens------------ #
        for col in range(ALIEN_COLUMNS):
            for row in range(ALIEN_ROWS):
                alien = Alien()
                alien.center_x = ALIEN_START_X + col * ALIEN_X_SPACING
                alien.center_y = ALIEN_START_Y - row * ALIEN_Y_SPACING
                self.alien_list.append(alien)

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
        self.alien_bullet_list.draw()

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
        # Update all sprites
        self.player_list.update()
        self.player_bullet_list.update()
        self.alien_list.update()
        self.alien_bullet_list.update()

#-------------- Player Movement --------------#
        self.player_sprite.center_x += (
            self.player_sprite.change_x * self.player_sprite.speed * delta_time
        )
        self.clamp_player_to_screen()

#-------------- Bullet Movement and Collision --------------#
        for bullet in self.player_bullet_list:
            # Movement
            bullet.center_y += bullet.speed * delta_time

            if bullet.bottom > WINDOW_HEIGHT:
                bullet.remove_from_sprite_lists()
                continue
            # Collision with aliens
            hits = arcade.check_for_collision_with_list(bullet, self.alien_list)
            for alien in hits:
                alien.remove_from_sprite_lists()
                bullet.remove_from_sprite_lists()
                break  # Bullet can only hit one alien

#-------------- Alien Fleet Movement and Shooting --------------#
        self.update_fleet(delta_time)
        
# ----------------------------------------------------------------------------

        # Check for collision between aliens and player
        if arcade.check_for_collision_with_list(self.player_sprite, self.alien_list):
            pass # Handle player-alien collision (e.g., end game, reduce life, etc.)

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

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.A:
            self.left_pressed = False
            self.update_player_direction()
        elif key == arcade.key.D:
            self.right_pressed = False
            self.update_player_direction()

#------------------- Helper Methods -------------------#
    def clamp_player_to_screen(self):
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > WINDOW_WIDTH:
            self.player_sprite.right = WINDOW_WIDTH

    def move_fleet(self, delta_time):
        """Move the alien fleet."""
        # Determine if any alien has hit the edge
        change_direction = False
        for alien in self.alien_list:
            alien.center_x += self.fleet_direction * self.current_fleet_speed * delta_time
            if alien.right >= WINDOW_WIDTH or alien.left <= 0:
                change_direction = True

        # If we need to change direction, do so and drop the fleet down
        if change_direction:
            self.fleet_direction *= -1
            for alien in self.alien_list:
                alien.center_y -= self.fleet_drop

    def update_fleet(self, delta_time):
        """- Calculate fleet speed based on the number of remaining aliens.
        - Move the fleet horizontally and drop when it reaches screen edges.
        - Update alien shooting timer and handle shooting.
        - Move alien bullets and check for collisions with the player."""
        # Calculate fleet speed based on remaining aliens
        if len(self.alien_list) > 0:
            self.current_fleet_speed = self.fleet_speed * ((ALIEN_ROWS*ALIEN_COLUMNS) / len(self.alien_list))
            self.current_fleet_speed = min(self.current_fleet_speed, MAX_FLEET_SPEED)
        else:
            self.current_fleet_speed = 0
        # Move the fleet using updated speed
        self.move_fleet(delta_time)
        # Dynamic cooldown for alien shooting (less aliens = faster shooting)
        current_cooldown = ALIEN_SHOOT_COOLDOWN * (len(self.alien_list) / (ALIEN_COLUMNS * ALIEN_ROWS))
        current_cooldown = max(current_cooldown, MIN_COOLDOWN)
        # Update alien shooting timer
        self.alien_shoot_timer -= delta_time

        # Pick a random alien from the bottom of any column to shoot
        if self.alien_shoot_timer <= 0 and len(self.alien_list) > 0:
            # Find bottom aliens in each column
            bottom_aliens = {}
            for alien in self.alien_list:
                col = int((alien.center_x - ALIEN_START_X) // ALIEN_X_SPACING)
                if col not in bottom_aliens or alien.center_y < bottom_aliens[col].center_y:
                    bottom_aliens[col] = alien

            # Choose a random bottom alien to shoot
            shooter = random.choice(list(bottom_aliens.values()))
            bullet = shooter.shoot()
            self.alien_bullet_list.append(bullet)

            # Reset alien shoot timer
            self.alien_shoot_timer = current_cooldown

        # Update alien bullets
        for bullet in self.alien_bullet_list:
            bullet.center_y += bullet.speed * delta_time

            if bullet.top < 0:
                bullet.remove_from_sprite_lists()
                continue

            # Check for collision with player
            if arcade.check_for_collision(bullet, self.player_sprite):
                bullet.remove_from_sprite_lists()
                pass # Handle player hit (e.g., end game, reduce life, etc.)


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