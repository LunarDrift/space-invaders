import arcade
from window import GameWindow


def main():
    window = GameWindow()
    window.show_game()
    # Start the arcade game loop
    arcade.run()


if __name__ == "__main__":
    main()