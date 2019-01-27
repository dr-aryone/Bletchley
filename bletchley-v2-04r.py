'''

Bletchley, V2.04r

By Steve Shambles, 27th Jan 2019.

With thanks for lots of help from CMSteffen from Github and Reddit.
I couldn't of finished this game properly without Steffen's enormous effort
to help sort out my code.

For more Python projects:
https://stevepython.wordpress.com/

'''
# changes\additions made by shambles for v2.04r
#-----------------------------------------------
# Bug found and fixed line 117
#
# if self.button_rows[row_index].count(None) == 4 :
#            return None
#
# This caused a crash if player did not enter all four colours.
# as thecolour count went from 3 to 0 in this case I removed
# the '== 4' that way it check ed for a non zer value and returned if true
# appears to have fixed it.

import random
import webbrowser
from functools import partial
from tkinter import (
    DISABLED,
    NORMAL,
    SUNKEN,
    Button,
    Label,
    LabelFrame,
    Menu,
    Tk,
    W,
)
from tkinter.messagebox import showinfo

from libs import music
from libs.game_logic import BletchleyGame

# Define the game title.
game_title = "Bletchley V2.04r"

# Define the available song filenames.
available_songs = {
    "The Lounge": "bensound-thelounge.mp3",
    "Once Again": "bensound-onceagain.mp3",
    "Enigmatic": "bensound-enigmatic.mp3",
    "Better Days": "bensound-betterdays.mp3",
    "All Tracks": "all.mp3",
}

# Define the available colors.
colors = ["red", "blue", "white", "yellow", "green", "plum"]


# Class Definitions


class GameWindow(object):
    """Define the game window and its functionality."""

    def __init__(self):
        """Initialize a new instance of the GameWindow."""
        self.new_game()

    def click_button(self, row_index, button_index):
        """Register the user's button-click by changing this button's color."""
        try:
            # Select the next color.
            current_value = self.button_rows[row_index][button_index] + 1
        except Exception as e:
            # There was no color set (this is the first click). Set to 0.
            current_value = 0
        # Set the new color. If we've run through the colors, loop back around.
        self.button_rows[row_index][button_index] = (
            current_value if current_value < 6 else 0
        )
        # Get the textual color value of the button.
        button_color = colors[self.button_rows[row_index][button_index]]
        # Set the button's color and assign it to the self.BUTTON_GUESSES dict.
        self.BUTTON_GUESSES[row_index][button_index] = Button(
            self.BUTTON_FRAMES[row_index],
            bg=button_color,
            text=" ",
            command=partial(self.click_button, row_index, button_index),
        )
        self.BUTTON_GUESSES[row_index][button_index].grid(
            row=(7 + row_index), column=button_index, pady=4, padx=4
        )

    def compare_guess_solution(self, user_guess):
        """Check the player's guess."""
        # Check to see if their guess was correct.
        if not self.game.correct_solution(user_guess):
            # Their guess was incorrect.
            return False

        # Their solution was correct.
        # Reveal the secret code.
        self.SOLUTION_BUTTON.destroy()
        self.display_solution()
        self.ROOT.update()

        # Let them know they've won.
        showinfo(
            "Bletchley",
            "You genius, "
            "you cracked the code.\n\n Alan would be proud of you!",
        )
        self.new_game()

    def decode_row(self, row_index):
        """Check result of the decode button press for row 1."""
        # Ensure that all four colors have been guessed.
        if self.button_rows[row_index].count(None):
            return None

        # Disable decode button, so no cheating.
        self.DECODE_BUTTONS[row_index].configure(state=DISABLED)

        # Build user_guess string.
        this_row = self.button_rows[row_index]
        user_guess = [colors[item] for item in this_row]

        # Construct the outcome string for output to the yesllow label.
        peg_string = self.game.generate_peg_string(user_guess)

        # display outcome in gui on yellow label
        self.BUTTON_FRAME_LABELS[row_index] = Label(
            self.BUTTON_FRAMES[row_index], bg="yellow", text=peg_string
        )
        self.BUTTON_FRAME_LABELS[row_index].grid(
            row=(7 + row_index), column=4, pady=4, padx=4, sticky=W
        )

        # Disable the buttons in this row.
        for button_index in range(4):
            self.BUTTON_GUESSES[row_index][button_index].configure(
                state=DISABLED
            )

        # Enable the next row's DECODE_BUTTON if it isn't in the last row.
        if row_index != 5:
            self.DECODE_BUTTONS[row_index + 1].configure(state=NORMAL)

        # Check to see if their solution was correct.
        correct = self.compare_guess_solution(user_guess)
        # Check to see if the game is over.
        if row_index == 5 and not correct:
            # If this is the last guess and they're wrong, reveal the solution
            # and tell the user they've lost.
            self.reveal_solution()

    def display_solution(self):
        """Reveal the solution to the player."""
        secret_buttons = list()
        # Generate the four buttons that display the secret code.
        for index in range(len(self.game.secret_code)):
            # Create a button.
            secret_button = Button(
                self.SOLUTION_FRAME, bg=self.game.secret_code[index]
            )
            # Assign its position.
            secret_button.grid(row=0, column=(4 + index), pady=4, padx=4)
            # Add it to the secret_buttons list.
            secret_buttons.append(secret_button)

    def new_game(self):
        """Reset the GameWindow and start a new game."""
        # Attempt to destroy the ROOT window if it exists.
        try:
            self.ROOT.destroy()
        except Exception as e:
            pass

        # Initialize a new Bletchley Game.
        self.game = BletchleyGame()

        # Initialize the Tunes class.
        self.tunes = music.Tunes(available_songs)

        # Initialize the dictionary that stores the user's guesses per-row.
        self.button_rows = dict()
        for row in range(6):
            self.button_rows[row] = [None] * 4

        # Construct the main window.
        self.ROOT = Tk()
        self.ROOT.title(game_title)
        self.ROOT.geometry("240x544")
        self.ROOT.resizable(False, False)

        # Construct the menu bar.
        self.MENU_BAR = Menu(self.ROOT)

        # Construct the main menu.
        self.MAIN_MENU = Menu(self.MENU_BAR, tearoff=0)
        self.MENU_BAR.add_cascade(label="Menu", menu=self.MAIN_MENU)
        self.MAIN_MENU.add_command(label="New Game", command=self.new_game)

        self.MAIN_MENU.add_command(
            label="How To play",
            command=partial(
                showinfo,
                "How To play",
                "Click on the blue pegs to change their colours.\nClick the green "  \
                "DECODE button to see if you cracked the code.\n\n"  \
                "Clues will be given on the yellow label about "  \
                "each colour you chose.\n\n"
                "'*' means correct colour and correct position.\n"
                "'X' means you have the colour correct, but in the wrong position.\n"
                "'0000' means you have no colours at all in the hidden code.\n\n"
                "Try to work out what the secret code is within six attempts to win."
                "\nYou can give in by clicking on the reveal button at any time.",
            ),
        )


        self.MAIN_MENU.add_command(
            label="Visit Blog",
            command=partial(
                self.open_browser, "https://stevepython.wordpress.com/"
            ),
        )
        self.MAIN_MENU.add_command(
            label="About",
            command=partial(
                showinfo,
                "About",
                "Bletchley V2.04r by Steve Shambles jan 2019",
            ),
        )
        self.MAIN_MENU.add_command(label="Exit", command=self.QUIT)


        # Construct the music menu.
        self.MUSIC_MENU = Menu(self.MENU_BAR, tearoff=0)
        self.MENU_BAR.add_cascade(label="Music", menu=self.MUSIC_MENU)
        # Add the menu items for each of the available songs.
        for song_name, song_file in self.tunes.track_list():
            self.MUSIC_MENU.add_command(
                # Define the menu item label.
                label="Play {}".format(song_name),
                # Call the function to play the appropriate song.
                command=partial(self.tunes.play_track, song_file),
            )
        self.MUSIC_MENU.add_separator()
        self.MUSIC_MENU.add_command(
            label="Stop music", command=self.tunes.stop_music
        )
        self.MUSIC_MENU.add_command(
            label="Free music from Bensound.com",
            command=partial(self.open_browser, "https://bensound.com/"),
        )

        # Add the menu bar to the ROOT window.
        self.ROOT.config(menu=self.MENU_BAR)

        # Construct the header.
        self.HEADER_FRAME = LabelFrame(
            self.ROOT, fg="blue", text="Bletchley V2.04r"
        )
        self.HEADER_FRAME.grid(padx=10)
        self.HEADER_LABEL = Label(
            self.HEADER_FRAME,
            text="Can you crack the code?\n\n"
            "* = Correct colour and position.\n"
            "x = Correct colour, wrong position.\n"
            "0000 = No colours in code",
        )
        self.HEADER_LABEL.grid(pady=10, padx=4)

        # Create the lists and dict that will store the various elements of
        # each row.
        self.BUTTON_FRAMES = list()
        self.BUTTON_FRAME_LABELS = list()
        self.DECODE_BUTTONS = list()
        self.BUTTON_GUESSES = dict()
        # Construct each row.
        for row_index in range(6):
            # Create the frame.
            BUTTON_FRAME = LabelFrame(
                self.ROOT,
                fg="blue",
                text="Attempt {}".format(row_index + 1),
                relief=SUNKEN
            )
            BUTTON_FRAME.grid()
            # Add the frame to the list.
            self.BUTTON_FRAMES.append(BUTTON_FRAME)

            # Create the empty buttons list.
            BUTTON_GUESS_LIST = [None] * 4
            for button_index in range(4):
                # Craft all four buttons.
                BUTTON = Button(
                    BUTTON_FRAME,
                    bg="skyblue",
                    text=" ",
                    command=partial(
                        self.click_button, row_index, button_index
                    ),
                )
                BUTTON.grid(
                    row=(7 + row_index), column=button_index, pady=4, padx=4
                )
                BUTTON_GUESS_LIST[button_index] = BUTTON
            # Assign the button list to the button dictionary.
            self.BUTTON_GUESSES[row_index] = BUTTON_GUESS_LIST[:]

            # Create the solution frame's label.
            FRAME_LABEL = Label(BUTTON_FRAME, bg="yellow", text="        ")
            FRAME_LABEL.grid(row=(7 + row_index), column=4, pady=4, padx=4)
            # Append the label to the label list.
            self.BUTTON_FRAME_LABELS.append(FRAME_LABEL)

            # Create the decode button.
            DECODE_BUTTON = Button(
                BUTTON_FRAME,
                bg="green2",
                text="DECODE",
                command=partial(self.decode_row, row_index),
            )
            DECODE_BUTTON.grid(row=(7 + row_index), column=5, pady=4, padx=4)
            # Append the decode button to the list.
            self.DECODE_BUTTONS.append(DECODE_BUTTON)

        # Make sure player can only decode row 1 to start with
        # by disabling all other decode buttons.
        for index in range(1, 6):
            self.DECODE_BUTTONS[index].configure(state=DISABLED)

        # cover up secret code with a button.
        self.SOLUTION_FRAME = LabelFrame(
            self.ROOT, fg="blue", text="Solution", relief=SUNKEN, padx=4, pady=6
        )
        self.SOLUTION_FRAME.grid()
        self.SOLUTION_BUTTON = Button(
            self.SOLUTION_FRAME,
            bg="gold",
            text="CLICK TO REVEAL SECRET CODE",
            command=self.reveal_solution,
        )
        self.SOLUTION_BUTTON.grid(row=9, column=5, pady=4, padx=4)

        # Run the main loop.
        self.run()

    def open_browser(self, website_url):
        """Open the specified URL in a browser window."""
        webbrowser.open(website_url)

    def QUIT(self):
        """Completely quit the game."""
        self.tunes.stop_music()
        self.ROOT.destroy()

    def reveal_solution(self):
        """Reveal button has been clicked, so show secret_code."""
        # Reveal the secret code.
        self.SOLUTION_BUTTON.destroy()
        self.display_solution()
        # Let them know they've lost.
        showinfo("Bletchley", "G A M E  O V E R  M A N\n\n")
        self.new_game()

    def run(self):
        """Start the main loop."""
        self.ROOT.mainloop()


# Initialize the GameWindow class, thereby starting a new game.
game_window = GameWindow()
