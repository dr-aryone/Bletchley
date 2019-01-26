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

    def generate_peg_string(self, user_guess):
        """Return a string representing the outcome of the user's guess."""
        perfect = 0  # How many perfect matches were in the user's guess?
        partial = 0  # How many partial matches were in the user's guess?
        # Generate temporary lists to contain the non-matches.
        code_remainder = list()
        user_remainder = list()
        # Check for perfect matches.
        for index in range(len(self.secret_code)):
            if user_guess[index] == self.secret_code[index]:
                # The index was a perfect match.
                perfect += 1
            else:
                # The index wasn't a perfect match. Append the colors at this
                # index to the code_ and user_remainder variables.
                code_remainder.append(self.secret_code[index])
                user_remainder.append(user_guess[index])
        # Check for partial matches.
        for color in code_remainder:
            # Here we're going to attempt to remove each sequential color in
            # code_remainder from the user_remainder list.
            try:
                # Get the index of the color in the user_remainder list. If the
                # color is not in the user_remainder list, this will raise a
                # ValueError exception.
                index = user_remainder.index(color)
                # If we reach this point in the code, the color exists in the
                # user_remainder list. Increment the 'partial' variable, then
                # remove the first instance of this color from the
                # user_remainder list. By removing the index, we prevent
                # accidentally counting the same user_remainder color twice.
                partial += 1
                user_remainder.pop(index)
            except ValueError as e:
                # The color was not in the user_remainder list. Move on to the
                # next color in code_remainder.
                pass
        # Assemble the peg string. It doesn't need to be randomized, because
        # there's no way to know which pegs were perfect and which were partial
        # just by looking at the order, since the order will always be perfect
        # before partial.
        peg_string = "*" * perfect + "x" * partial
        # Return the peg string.
        return peg_string

    def correct_solution(self, user_guess):
        """Check to see whether the user's guess is the correct solution."""
        if(self.generate_peg_string(user_guess) == "****"):
            # Their solution is correct.
            return True
        # Their solution is incorrect.
        return False
