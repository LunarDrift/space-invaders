import random
import arcade
from sprites.player import Player
from sprites.alien import Alien
from enums.alien_type import AlienType
from sprites.ufo import UFO
from sprites.hitsplat import HitSplat

from settings import *



class GameView(arcade.View):
    """Main game class."""

    def __init__(self):
        super().__init__()

        # ------------ Sprite lists ------------ #
        self.player_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.alien_bullet_list = arcade.SpriteList()
        self.ufo_list = arcade.SpriteList()
        self.hitsplat_list = arcade.SpriteList()

        # ------------ Set up the player info ------------ #
        self.player_sprite = None
        self.score = 0

        # ------------ Alien Fleet info ------------ #
        self.fleet_direction = 1    # 1 = right; -1 = left
        self.fleet_speed = ALIEN_SPEED       # pixels per second
        self.fleet_drop = ALIEN_DROP        # pixels to drop when changing direction
        self.alien_shoot_timer = ALIEN_SHOOT_COOLDOWN
        self.initial_alien_count = 0
        self.current_fleet_speed = self.fleet_speed

        # ----------- Input tracking ------------ #
        self.left_pressed = False
        self.right_pressed = False

        # ----------- Load background image ------------ #
        self.background_img = arcade.load_texture("assets/bg.jpg")

        # ----------- Load lives icon texture ------------ #
        self.lives_texture = arcade.load_texture("assets/Sprite-Ship.png")


    def setup(self):
        """Set up the game and initialize the player and alien fleet."""
        # ------------ Clear existing sprites ------------ #
        self.player_list.clear()
        self.alien_list.clear()
        self.player_bullet_list.clear()
        self.alien_bullet_list.clear()
        self.ufo_list.clear()
        self.hitsplat_list.clear()

        # ------------ Set up player ------------ #
        self.player_sprite = Player()
        self.player_sprite.center_x = WINDOW_WIDTH // 2
        self.player_sprite.center_y = 60
        self.player_list.append(self.player_sprite)


        # ------------ Set up aliens ------------ #
        self.create_fleet()


    def on_draw(self):
        """Render the screen."""
        # ------------ Clear the screen ------------ #
        self.clear()

        # ------------ Draw the background image ------------ #
        arcade.draw_texture_rect(
            self.background_img,
            arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
            alpha=120,
        )

        # ------------ Draw the score and lives ------------ #
        # Using Text objects for better performance
        # lives = arcade.Text(
        #     "LIVES:",
        #     3,
        #     10,
        #     arcade.color.WHITE,
        #     10,
        #     font_name="Pixeled",
        # )

        # Draw ship icons to represent lives
        for i in range(self.player_sprite.lives):
            x = 20 + i * (32 * LIVES_ICON_SCALING + 5) # 32 is the original width of the ship sprite + 5 pixels spacing
            y = 15
            arcade.draw_texture_rect(
                self.lives_texture,
                arcade.XYWH(x, y, 32 * LIVES_ICON_SCALING, 32 * LIVES_ICON_SCALING)
            )

        score = arcade.Text(
            f"SCORE: {self.score}",
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT - 30,
            arcade.color.WHITE,
            10,
            font_name="Pixeled",
            anchor_x="center",
        )
        # lives.draw()
        score.draw()

        # ------------ Draw all the sprites ------------ #
        self.player_list.draw(pixelated=True)
        self.alien_list.draw(pixelated=True)
        self.player_bullet_list.draw(pixelated=True)
        self.alien_bullet_list.draw(pixelated=True)
        self.ufo_list.draw(pixelated=True)
        self.hitsplat_list.draw(pixelated=True)


    def update_player_direction(self):
        """Update the player's horizontal direction based on keys pressed.
        - `-1` = left
        - `1` = right
        - `0` = no movement"""
        # ------------ Calculate direction based on the keys pressed ------------ #
        # change_x: -1 = left; 1 = right
        self.player_sprite.change_x = 0
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -1
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = 1


    def on_update(self, delta_time):
        """Movement and game logic."""
        # ------------ Update all sprites ------------ #
        self.player_list.update()
        self.player_bullet_list.update()
        self.alien_list.update()
        self.alien_bullet_list.update()
        self.hitsplat_list.update()


# ------------ Player Bullet Movement --------------#
        for bullet in self.player_bullet_list:
            bullet.center_y += bullet.speed * delta_time
            # Remove bullet if off-screen
            if bullet.bottom > WINDOW_HEIGHT:
                bullet.remove_from_sprite_lists()
                continue

        if len(self.alien_list) == 0:
            # All aliens destroyed, reset fleet and clear bullets
            self.reset()
        
        # Check for collisions
        self.check_collisions()

# ------------ Alien Fleet Movement and Shooting --------------#
        self.update_fleet(delta_time)

        # Randomly spawn a UFO occasionally
        if random.random() < 0.001:  # Adjust probability as needed
            self.spawn_ufo()
        self.ufo_list.update()

        # ------------ Check for alien invasion ------------ #
        self.invasion()


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        # ------------ Handle player movement ------------ #
        if key == arcade.key.A:
            self.left_pressed = True
            self.update_player_direction()
        elif key == arcade.key.D:
            self.right_pressed = True
            self.update_player_direction()

        # ------------ Handle shooting ------------ #
        elif key == arcade.key.SPACE:
            # Add the bullet to the player's bullet list
            bullet = self.player_sprite.shoot_bullet()
            if bullet:
                self.player_bullet_list.append(bullet)
        
        # ------------ Handle quitting the game ------------ #
        if key == arcade.key.ESCAPE:
            arcade.close_window()


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        # ------------ Handle player movement ------------ #
        if key == arcade.key.A:
            self.left_pressed = False
            self.update_player_direction()
        elif key == arcade.key.D:
            self.right_pressed = False
            self.update_player_direction()


    #------------------- Helper Methods -------------------#    
    def create_fleet(self):
        """Create the alien fleet."""
        for col in range(ALIEN_COLUMNS):
            for row in range(ALIEN_ROWS):
                # Determine alien type based on row
                if row < TOP_ALIEN_ROWS:
                    alien_type = AlienType.TOP
                elif row < TOP_ALIEN_ROWS + MID_ALIEN_ROWS:
                    alien_type = AlienType.MID
                else:
                    alien_type = AlienType.BOTTOM
                # Create and position alien
                alien = Alien(alien_type)
                alien.center_x = ALIEN_START_X + col * ALIEN_X_SPACING
                alien.center_y = ALIEN_START_Y - row * ALIEN_Y_SPACING
                self.alien_list.append(alien)

        self.initial_alien_count = len(self.alien_list)


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
        """Update the alien fleet movement and shooting.

        - Move the fleet horizontally and drop when it reaches screen edges.
        - Update alien shooting timer and handle shooting.
        - Move alien bullets and check for collisions with the player."""

        # Update fleet speed based on remaining aliens
        self.update_fleet_speed()
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

    
    def update_fleet_speed(self):
        """Recalculate the fleet speed dynamically based on remaining aliens."""
        if len(self.alien_list) > 0:
            self.current_fleet_speed = min(self.fleet_speed * (self.initial_alien_count / len(self.alien_list)), MAX_FLEET_SPEED)
        else:
            self.current_fleet_speed = 0


    def invasion(self):
        """Handle alien invasion (aliens reaching the bottom)."""
        # If an alien reaches the bottom, end the game
        for alien in self.alien_list:
            if alien.bottom <= 0:
                self.window.show_game_over()
                break

    def reset(self):
        """Reset the alien fleet to its initial state and clears existing bullets.
        Called when all aliens are destroyed."""
        self.alien_list.clear()
        self.player_bullet_list.clear()
        self.alien_bullet_list.clear()
        
        # Recreate the alien fleet
        self.create_fleet()

        # Reset fleet parameters
        self.fleet_direction = 1
        self.update_fleet_speed()

        # Reset alien shoot timer
        self.alien_shoot_timer = ALIEN_SHOOT_COOLDOWN

    def spawn_ufo(self):
        """Spawn a UFO that moves across the top of the screen."""
        direction = random.choice([-1, 1])
        ufo = UFO(direction)
        self.ufo_list.append(ufo)


    def check_collisions(self):
        # Player bullet collision with aliens
        for bullet in self.player_bullet_list:
                hits = arcade.check_for_collision_with_list(bullet, self.alien_list)
                for alien in hits:
                    # Increase score based on alien type
                    self.score += alien.alien_type.score
                    # Hitsplat at alien position
                    hitsplat = HitSplat(alien.center_x, alien.center_y)
                    self.hitsplat_list.append(hitsplat)

                    alien.remove_from_sprite_lists()
                    bullet.remove_from_sprite_lists()
                    break  # Bullet can only hit one alien

                # Check for UFO collision
                ufo_hits = arcade.check_for_collision_with_list(bullet, self.ufo_list)
                for ufo in ufo_hits:
                    self.score += 100  # UFO gives more points
                    # Hitsplat at UFO position
                    self.hitsplat_list.append(HitSplat(ufo.center_x, ufo.center_y))
                    ufo.remove_from_sprite_lists()
                    bullet.remove_from_sprite_lists()
                    break  # Bullet can only hit one UFO

        # Alien bullets vs player
        for bullet in self.alien_bullet_list:
            if arcade.check_for_collision(bullet, self.player_sprite):
                    bullet.remove_from_sprite_lists()
                    # Show hitsplat at player position
                    hitsplat = HitSplat(self.player_sprite.center_x, self.player_sprite.center_y)
                    self.hitsplat_list.append(hitsplat)
                    # Reduce player lives
                    self.player_sprite.lives -= 1
                    if self.player_sprite.lives <= 0:
                        self.window.show_game_over()

        # Player vs aliens
        if arcade.check_for_collision_with_list(self.player_sprite, self.alien_list):
                # Reduce player lives
                    self.player_sprite.lives -= 1
                    if self.player_sprite.lives <= 0:
                        self.window.show_game_over()