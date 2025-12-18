from enum import Enum

class AlienType(Enum):
    """The AlienType enum can be used to differentiate between different types of aliens in the game."""
    # What does each Alien look like, how many points is it worth, and what is its scale?
    TOP = ("assets/Sprite-AlienTop.png", 30, 0.95)
    MID = ("assets/SpaceInvadersMidAlien1.png", 20, 1)
    BOTTOM = ("assets/Sprite-AlienBottom.png", 10, 1.25)

    def __init__(self, texture_path: str, score: int, scale: float):
        self.texture_path = texture_path
        self.score = score
        self.scale = scale