import arcade
from settings import WINDOW_WIDTH, WINDOW_HEIGHT


class GameOverView(arcade.View):
    """View to show when the game is over."""
    def __init__(self, final_score):
        super().__init__()
        self.score = final_score

    def on_show(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the game over screen."""
        self.clear()
        # Using Text objects for better performance
        game_over = arcade.Text(
            "GAME OVER",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 + 50,
            arcade.color.RED,
            font_size=40,
            font_name="Pixeled",
            anchor_x="center",
        )
        instruction = arcade.Text(
            "PRESS ESC TO QUIT OR R TO RESTART",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 - 100,
            arcade.color.WHITE,
            font_size=16,
            font_name="Pixeled",
            anchor_x="center",
        )
        
        final_score = arcade.Text(
            f"FINAL SCORE: {self.score}",
            WINDOW_WIDTH / 2,
            WINDOW_HEIGHT / 2 - 10,
            arcade.color.WHITE,
            font_size=20,
            font_name="Pixeled",
            anchor_x="center",
        )

        arcade.draw_texture_rect(
            arcade.load_texture("assets/bg.jpg"),
            arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
            alpha=120,
        )
        game_over.draw()
        instruction.draw()
        final_score.draw()

    def on_key_press(self, key, modifiers):
        """Handle key presses."""
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        elif key == arcade.key.R:
            from .game_view import GameView
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)