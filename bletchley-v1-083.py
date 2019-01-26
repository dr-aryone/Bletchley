"""Bletchley, github version."""

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

# Define the available song filenames.
available_songs = {
    "The Lounge": "bensound-thelounge.mp3",
    "Once Again": "bensound-onceagain.mp3",
    "Enigmatic": "bensound-enigmatic.mp3",
    "Better Days": "bensound-betterdays.mp3",
    "All Tracks": "all.mp3",
}
# Initialize the Tunes class.
tunes = music.Tunes(available_songs)

# Initiaize the BletchleyGame class.
game = BletchleyGame()

# Initialize the dictionary that stores the user's guesses per-row.
button_rows = dict()
for row in range(6):
    button_rows[row] = [None] * 4

# Define the available colors.
colors = ["red", "blue", "white", "yellow", "green", "plum"]


# Function Definitions


def open_browser(website_url):
    """Open the specified URL in a browser window."""
    webbrowser.open(website_url)


def QUIT():
    """Completely quit the game."""
    tunes.stop_music()
    ROOT.destroy()


def decode_row(row_index):
    """Check result of the decode button press for row 1."""
    global user_guess

    # Ensure that all four colors have been guessed.
    if button_rows[row_index].count(None) == 4:
        return None

    # Disable decode button, so no cheating.
    DECODE_BUTTONS[row_index].configure(state=DISABLED)

    # Build user_guess string.
    this_row = button_rows[row_index]
    user_guess = [colors[item] for item in this_row]

    # Construct the outcome string for output to the yesllow label.
    peg_string = game.generate_peg_string(user_guess)

    # display outcome in gui on yellow label
    BUTTON_FRAME_LABELS[row_index] = Label(
        BUTTON_FRAMES[row_index], bg="yellow", text=peg_string
    )
    BUTTON_FRAME_LABELS[row_index].grid(
        row=(7 + row_index), column=4, pady=4, padx=4, sticky=W
    )

    # Disable the buttons in this row.
    for button_index in range(4):
        BUTTON_GUESSES[row_index][button_index].configure(state=DISABLED)

    # Enable the next row's DECODE_BUTTON if it isn't in the last row.
    if row_index != 5:
        DECODE_BUTTONS[row_index + 1].configure(state=NORMAL)

    # Check user-input against secret_code.
    compare_guess_solution(user_guess)


def click_button(row_index, button_index):
    """Register the user's button-click by changing this button's color."""
    try:
        # Select the next color.
        current_value = button_rows[row_index][button_index] + 1
    except Exception as e:
        # There was no color set (this is the first click). Set to 0.
        current_value = 0
    # Set the new color. If we've run through the colors, go back to the first.
    button_rows[row_index][button_index] = (
        current_value if current_value < 6 else 0
    )
    # Get the textual color value of the button.
    button_color = colors[button_rows[row_index][button_index]]
    # Set the button's color and assign it to the BUTTON_GUESSES dictionary.
    BUTTON_GUESSES[row_index][button_index] = Button(
        BUTTON_FRAMES[row_index],
        bg=button_color,
        text=" ",
        command=partial(click_button, row_index, button_index),
    )
    BUTTON_GUESSES[row_index][button_index].grid(
        row=(7 + row_index), column=button_index, pady=4, padx=4
    )


def display_solution():
    """Reveal the solution to the player."""
    secret_buttons = list()
    # Generate the four buttons that display the secret code.
    for index in range(len(game.secret_code)):
        # Create a button.
        secret_button = Button(SOLUTION_FRAME, bg=game.secret_code[index])
        # Assign its position.
        secret_button.grid(row=0, column=(4 + index), pady=4, padx=4)
        # Add it to the secret_buttons list.
        secret_buttons.append(secret_button)


def compare_guess_solution(user_guess):
    """Check what player pegs match secret code."""
    # Check to see if their guess was correct.
    if not game.correct_solution(user_guess):
        # Their guess was incorrect.
        return None

    # Their solution was correct.
    # Reveal the secret code.
    SOLUTION_BUTTON.destroy()
    display_solution()
    ROOT.update()

    # Let them know they've won.
    showinfo(
        "Bletchley",
        "You genius, " "you cracked the code.\n\n Alan would be proud of you!",
    )
    QUIT()


def reveal_solution():
    """Reveal button has been clicked, so show secret_code."""
    # Reveal the secret code.
    SOLUTION_BUTTON.destroy()
    display_solution()
    # Let them know they've lost.
    showinfo("Bletchley", "G A M E  O V E R  M A N\n\n")
    QUIT()


ROOT = Tk()
ROOT.title("Bletchley v4.083")
ROOT.geometry("225x520")

# Drop-down menu.
MENU_BAR = Menu(ROOT)
FILE_MENU = Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label="Menu", menu=FILE_MENU)
FILE_MENU.add_command(
    label="Visit Blog",
    command=partial(open_browser, "https://stevepython.wordpress.com/"),
)
FILE_MENU.add_command(
    label="About",
    command=partial(
        showinfo, "About", "Bletchley V1.083 by Steve Shambles jan 2019"
    ),
)
FILE_MENU.add_command(label="Exit", command=QUIT)

FILE_MENU2 = Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label="Music", menu=FILE_MENU2)
# Add the menu items for each of the available songs.
for song_name, song_file in tunes.track_list():
    FILE_MENU2.add_command(
        # Define the menu item label.
        label="Play {}".format(song_name),
        # Call the function to play the appropriate song.
        command=partial(tunes.play_track, song_file),
    )
FILE_MENU2.add_separator()
FILE_MENU2.add_command(label="Stop music", command=tunes.stop_music)
FILE_MENU2.add_command(
    label="Free music from Bensound.com",
    command=partial(open_browser, "https://bensound.com/"),
)
ROOT.config(menu=MENU_BAR)


# Header messages.
HEADER_FRAME = LabelFrame(
    ROOT, fg="blue", text="Bletchley v4.083", relief=SUNKEN
)
HEADER_FRAME.grid()
HEADER_LABEL = Label(
    HEADER_FRAME,
    text="Can you crack the code?\n\n"
    "* = Correct colour and position.\n"
    "x = Correct colour, wrong position.\n"
    "blank = No colours in code",
)
HEADER_LABEL.grid(pady=4, padx=4)

# Create the lists and dict that will store the various elements of each row.
BUTTON_FRAMES = list()
BUTTON_FRAME_LABELS = list()
DECODE_BUTTONS = list()
BUTTON_GUESSES = dict()
# Construct each row.
for row_index in range(6):
    # Create the frame.
    BUTTON_FRAME = LabelFrame(
        ROOT, fg="blue", text="Attempt {}".format(row_index + 1), relief=SUNKEN
    )
    BUTTON_FRAME.grid()
    # Add the frame to the list.
    BUTTON_FRAMES.append(BUTTON_FRAME)

    # Create the empty buttons list.
    BUTTON_GUESS_LIST = [None] * 4
    for button_index in range(4):
        # Craft all four buttons.
        BUTTON = Button(
            BUTTON_FRAME,
            bg="skyblue",
            text=" ",
            command=partial(click_button, row_index, button_index),
        )
        BUTTON.grid(row=(7 + row_index), column=button_index, pady=4, padx=4)
        BUTTON_GUESS_LIST[button_index] = BUTTON
    # Assign the button list to the button dictionary.
    BUTTON_GUESSES[row_index] = BUTTON_GUESS_LIST[:]

    # Create the solution frame's label.
    FRAME_LABEL = Label(BUTTON_FRAME, bg="yellow", text="        ")
    FRAME_LABEL.grid(row=(7 + row_index), column=4, pady=4, padx=4)
    # Append the label to the label list.
    BUTTON_FRAME_LABELS.append(FRAME_LABEL)

    # Create the decode button.
    DECODE_BUTTON = Button(
        BUTTON_FRAME,
        bg="green2",
        text="DECODE",
        command=partial(decode_row, row_index),
    )
    DECODE_BUTTON.grid(row=(7 + row_index), column=5, pady=4, padx=4)
    # Append the decode button to the list.
    DECODE_BUTTONS.append(DECODE_BUTTON)

# Make sure player can only decode row 1 to start with
# by disabling all other decode buttons.
for index in range(1, 6):
    DECODE_BUTTONS[index].configure(state=DISABLED)

# cover up secret code with a button.
SOLUTION_FRAME = LabelFrame(ROOT, fg="blue", text="solution", relief=SUNKEN)
SOLUTION_FRAME.grid()
SOLUTION_BUTTON = Button(
    SOLUTION_FRAME, bg="gold", text="REVEAL", command=reveal_solution
)
SOLUTION_BUTTON.grid(row=9, column=5, pady=4, padx=4)


# Start the application.
ROOT.mainloop()
