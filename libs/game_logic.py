"""Define the Bletchley game logic.

This file defines how the Bletchley game is played and provides functions for
instantiating, playing, and resolving the game.
"""

import random

class BletchleyGame(object):
    """Define the BletchleyGame class."""

    colors = ["red", "blue", "white", "yellow", "green", "plum"]

    def __init__(self):
        """Initialize the game."""
        self.new_game()

    def new_game(self):
        """Reset the game with a new solution."""
        # Generate a new four-color secret code.
        self.secret_code = [
            self.colors[random.randrange(0, 6)] for x in range(4)
        ]
        # DEBUG: Print the secret code to the console.
        print("secret code is ", self.secret_code)
