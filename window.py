import arcade
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from views.game_view import GameView
from views.game_over_view import GameOverView


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    def show_game(self):
        game = GameView()
        game.setup()
        self.show_view(game)

    def show_game_over(self):
        game_over = GameOverView(final_score=self.current_view.score)
        self.show_view(game_over)
