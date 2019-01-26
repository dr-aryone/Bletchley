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

user_guess = []
secret_code = []
colors = ["red", "blue", "white", "yellow", "green", "plum"]


def open_browser(website_url):
    """Open the specified URL in a browser window."""
    webbrowser.open(website_url)


def QUIT():
    """Completely quit the game."""
    tunes.stop_music()
    ROOT.destroy()


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

# -------------classes-----------------------------------------------------
# This is the first time I have used classes and I don't really understand
# I put these classes in simply to avoid the use of
# global statements, there would of been about 60 of them otherwise :-).

# Create current_buttons list with four empty elements.
current_buttons = [None] * 4


class button_up_row:
    """Variables for button colours for a button row."""

    def __init__(self, button_1, button_2, button_3, button_4):
        """Initialize the button_up_row class."""
        self.button_1 = button_1
        self.button_2 = button_2
        self.button_3 = button_3
        self.button_4 = button_4


# -----------------------------row 1 functions----------------------------
def decode_robutton_row_5():
    """Check result of the decode button press for row 1."""
    global user_guess

    # exit if all 4 colours not entered yet
    if (
        button_row_1.button_1 == 0
        or button_row_1.button_2 == 0
        or button_row_1.button_3 == 0
        or button_row_1.button_4 == 0
    ):
        return

    # Disable decode button, so no cheating.
    DECODE_BUTTON_1.configure(state=DISABLED)

    # Build user_guess string.
    user_guess = [temp_bc1_1, temp_bc1_2, temp_bc1_3, temp_bc1_4]

    # Construct the outcome string for output to the yesllow label.
    peg_string = game.generate_peg_string(user_guess)

    # rnd shuffle the out_come answer so player does not see order of results

    # display outcome in gui on yellow label
    LAB1 = Label(FRAME1, bg="yellow", text=peg_string)
    LAB1.grid(row=7, column=4, pady=4, padx=4, sticky=W)

    # Disable row 1 buttons, so cant now be changed by user.
    # for some reason have to rebuild the button first,
    # without the call, and with its user selected colour
    # otherwise colour selected by user is lost and can still click
    # and change the button colours, which is not good.
    BUT1_1 = Button(FRAME1, bg=temp_bc1_1, text=" ")
    BUT1_1.grid(row=7, column=0, pady=4, padx=4)
    BUT1_1.configure(state=DISABLED)
    BUT1_2 = Button(FRAME1, bg=temp_bc1_2, text=" ")
    BUT1_2.grid(row=7, column=1, pady=4, padx=4)
    BUT1_2.configure(state=DISABLED)
    BUT1_3 = Button(FRAME1, bg=temp_bc1_3, text=" ")
    BUT1_3.grid(row=7, column=2, pady=4, padx=4)
    BUT1_3.configure(state=DISABLED)
    BUT1_4 = Button(FRAME1, bg=temp_bc1_4, text=" ")
    BUT1_4.grid(row=7, column=3, pady=4, padx=4)
    BUT1_4.configure(state=DISABLED)

    # Now need to enable row2's decode button
    DECODE_BUTTON_2.configure(state=NORMAL)

    # Check user-input against secret_code.
    compare_guess_solution(user_guess)


def clk_but_1_1():
    """Player clicked but1_1 to change its colour."""
    global temp_bc1_1

    # Select next colour 1-6.
    button_row_1.button_1 += 1

    # If last colour+1 (6+1), then loop it to first colour.
    if button_row_1.button_1 == 7:
        button_row_1.button_1 = 1

    # Convert integer to actual text colour to use as button fg colour.
    bc = button_row_1.button_1
    current_buttons[0] = str(colors[bc - 1])

    # Store colour selected for later use in disabling this button.
    temp_bc1_1 = current_buttons[0]

    # Now actually change the button colour and display
    BUT1_1 = Button(
        FRAME1, bg=current_buttons[0], text=" ", command=clk_but_1_1
    )
    BUT1_1.grid(row=7, column=0, pady=4, padx=4)


def clk_but_1_2():
    """Player clicked but1_2 to change its colour."""
    global temp_bc1_2

    button_row_1.button_2 += 1

    if button_row_1.button_2 == 7:
        button_row_1.button_2 = 1

    bc = button_row_1.button_2
    current_buttons[1] = str(colors[bc - 1])

    temp_bc1_2 = current_buttons[1]

    BUT1_2 = Button(
        FRAME1, bg=current_buttons[1], text=" ", command=clk_but_1_2
    )
    BUT1_2.grid(row=7, column=1, pady=4, padx=4)


def clk_but_1_3():
    """Player clicked but1_3 to change its colour."""
    global temp_bc1_3

    button_row_1.button_3 += 1

    if button_row_1.button_3 == 7:
        button_row_1.button_3 = 1

    bc = button_row_1.button_3
    current_buttons[2] = str(colors[bc - 1])

    temp_bc1_3 = current_buttons[2]

    BUT1_3 = Button(
        FRAME1, bg=current_buttons[2], text=" ", command=clk_but_1_3
    )
    BUT1_3.grid(row=7, column=2, pady=4, padx=4)


def clk_but_1_4():
    """Player clicked but1_4 to change its colour."""
    global temp_bc1_4

    button_row_1.button_4 += 1

    if button_row_1.button_4 == 7:
        button_row_1.button_4 = 1

    bc = button_row_1.button_4
    current_buttons[3] = str(colors[bc - 1])

    temp_bc1_4 = current_buttons[3]

    BUT1_4 = Button(
        FRAME1, bg=current_buttons[3], text=" ", command=clk_but_1_4
    )
    BUT1_4.grid(row=7, column=3, pady=4, padx=4)


# -------------------------row 2-------------------------------------------


def decode_row2():
    """Decode button for row 2 has been clicked so check input."""
    global user_guess

    if (
        button_row_2.button_1 == 0
        or button_row_2.button_2 == 0
        or button_row_2.button_3 == 0
        or button_row_2.button_4 == 0
    ):
        return

    DECODE_BUTTON_2.configure(state=DISABLED)

    user_guess = [temp_bc2_1, temp_bc2_2, temp_bc2_3, temp_bc2_4]

    peg_string = game.generate_peg_string(user_guess)

    LAB1 = Label(FRAME2, bg="yellow", text=peg_string)
    LAB1.grid(row=8, column=4, pady=4, padx=4, sticky=W)

    DECODE_BUTTON_3.configure(state=NORMAL)
    BUT2_1 = Button(FRAME2, bg=temp_bc2_1, text=" ")
    BUT2_1.grid(row=8, column=0, pady=4, padx=4)
    BUT2_1.configure(state=DISABLED)
    BUT2_2 = Button(FRAME2, bg=temp_bc2_2, text=" ")
    BUT2_2.grid(row=8, column=1, pady=4, padx=4)
    BUT2_2.configure(state=DISABLED)
    BUT2_3 = Button(FRAME2, bg=temp_bc2_3, text=" ")
    BUT2_3.grid(row=8, column=2, pady=4, padx=4)
    BUT2_3.configure(state=DISABLED)
    BUT2_4 = Button(FRAME2, bg=temp_bc2_4, text=" ")
    BUT2_4.grid(row=8, column=3, pady=4, padx=4)

    BUT2_4.configure(state=DISABLED)

    compare_guess_solution(user_guess)


def clk_but_2_1():
    """Player clicked but2_1 to change its colour."""
    global temp_bc2_1

    button_row_2.button_1 += 1

    if button_row_2.button_1 == 7:
        button_row_2.button_1 = 1

    bc = button_row_2.button_1
    current_buttons[0] = str(colors[bc - 1])

    BUT2_1 = Button(
        FRAME2, bg=current_buttons[0], text=" ", command=clk_but_2_1
    )
    BUT2_1.grid(row=8, column=0, pady=4, padx=4)

    temp_bc2_1 = current_buttons[0]


def clk_but_2_2():
    """Player clicked but2_2 to change its colour."""
    global temp_bc2_2

    button_row_2.button_2 += 1

    if button_row_2.button_2 == 7:
        button_row_2.button_2 = 1

    bc = button_row_2.button_2
    current_buttons[1] = str(colors[bc - 1])

    BUT2_2 = Button(
        FRAME2, bg=current_buttons[1], text=" ", command=clk_but_2_2
    )
    BUT2_2.grid(row=8, column=1, pady=4, padx=4)

    temp_bc2_2 = current_buttons[1]


def clk_but_2_3():
    """Player clicked but2_3 to change its colour."""
    global temp_bc2_3

    button_row_2.button_3 += 1

    if button_row_2.button_3 == 7:
        button_row_2.button_3 = 1

    bc = button_row_2.button_3
    current_buttons[2] = str(colors[bc - 1])

    BUT2_3 = Button(
        FRAME2, bg=current_buttons[2], text=" ", command=clk_but_2_3
    )
    BUT2_3.grid(row=8, column=2, pady=4, padx=4)

    temp_bc2_3 = current_buttons[2]


def clk_but_2_4():
    """Player clicked but2_4 to change its colour."""
    global temp_bc2_4

    button_row_2.button_4 += 1

    if button_row_2.button_4 == 7:
        button_row_2.button_4 = 1

    bc = button_row_2.button_4
    current_buttons[3] = str(colors[bc - 1])

    BUT2_4 = Button(
        FRAME2, bg=current_buttons[3], text=" ", command=clk_but_2_4
    )
    BUT2_4.grid(row=8, column=3, pady=4, padx=4)

    temp_bc2_4 = current_buttons[3]


# -------------------------row 3-----------------------------------------------


def decode_row3():
    """Decode button for row 3 has been clicked so check input."""
    global user_guess

    if (
        button_row_3.button_1 == 0
        or button_row_3.button_2 == 0
        or button_row_3.button_3 == 0
        or button_row_3.button_4 == 0
    ):
        return

    DECODE_BUTTON_3.configure(state=DISABLED)
    user_guess = [temp_bc3_1, temp_bc3_2, temp_bc3_3, temp_bc3_4]

    peg_string = game.generate_peg_string(user_guess)

    LAB1 = Label(FRAME3, bg="yellow", text=peg_string)
    LAB1.grid(row=9, column=4, pady=4, padx=4, sticky=W)

    BUT3_1 = Button(FRAME3, bg=temp_bc3_1, text=" ")
    BUT3_1.grid(row=9, column=0, pady=4, padx=4)
    BUT3_1.configure(state=DISABLED)
    BUT3_2 = Button(FRAME3, bg=temp_bc3_2, text=" ")
    BUT3_2.grid(row=9, column=1, pady=4, padx=4)
    BUT3_2.configure(state=DISABLED)
    BUT3_3 = Button(FRAME3, bg=temp_bc3_3, text=" ")
    BUT3_3.grid(row=9, column=2, pady=4, padx=4)
    BUT3_3.configure(state=DISABLED)
    BUT3_4 = Button(FRAME3, bg=temp_bc3_4, text=" ")
    BUT3_4.grid(row=9, column=3, pady=4, padx=4)
    BUT3_4.configure(state=DISABLED)

    DECODE_BUTTON_4.configure(state=NORMAL)

    compare_guess_solution(user_guess)


def clk_but_3_1():
    """Player clicked but3_1 to change its colour."""
    global temp_bc3_1

    button_row_3.button_1 += 1

    if button_row_3.button_1 == 7:
        button_row_3.button_1 = 1

    bc = button_row_3.button_1
    current_buttons[0] = str(colors[bc - 1])

    BUT3_1 = Button(
        FRAME3, bg=current_buttons[0], text=" ", command=clk_but_3_1
    )
    BUT3_1.grid(row=9, column=0, pady=4, padx=4)

    temp_bc3_1 = current_buttons[0]


def clk_but_3_2():
    """Player clicked but3_2 to change its colour."""
    global temp_bc3_2

    button_row_3.button_2 += 1

    if button_row_3.button_2 == 7:
        button_row_3.button_2 = 1

    bc = button_row_3.button_2
    current_buttons[1] = str(colors[bc - 1])

    BUT3_2 = Button(
        FRAME3, bg=current_buttons[1], text=" ", command=clk_but_3_2
    )
    BUT3_2.grid(row=9, column=1, pady=4, padx=4)

    temp_bc3_2 = current_buttons[1]


def clk_but_3_3():
    """Player clicked but3_3 to change its colour."""
    global temp_bc3_3

    button_row_3.button_3 += 1

    if button_row_3.button_3 == 7:
        button_row_3.button_3 = 1

    bc = button_row_3.button_3
    current_buttons[2] = str(colors[bc - 1])

    BUT3_3 = Button(
        FRAME3, bg=current_buttons[2], text=" ", command=clk_but_3_3
    )
    BUT3_3.grid(row=9, column=2, pady=4, padx=4)

    temp_bc3_3 = current_buttons[2]


def clk_but_3_4():
    """Player clicked but 3_4 to change its colour."""
    global temp_bc3_4

    button_row_3.button_4 += 1

    if button_row_3.button_4 == 7:
        button_row_3.button_4 = 1

    bc = button_row_3.button_4
    current_buttons[3] = str(colors[bc - 1])

    BUT3_4 = Button(
        FRAME3, bg=current_buttons[3], text=" ", command=clk_but_3_4
    )
    BUT3_4.grid(row=9, column=3, pady=4, padx=4)

    temp_bc3_4 = current_buttons[3]


# --------------------------start row 4----------------------------------------


def decode_row4():
    """Decode button for row 4 has been clicked so check input."""
    global user_guess

    if (
        button_row_4.button_1 == 0
        or button_row_4.button_2 == 0
        or button_row_4.button_3 == 0
        or button_row_4.button_4 == 0
    ):
        return

    DECODE_BUTTON_4.configure(state=DISABLED)
    user_guess = [temp_bc4_1, temp_bc4_2, temp_bc4_3, temp_bc4_4]

    peg_string = game.generate_peg_string(user_guess)

    LAB1 = Label(FRAME4, bg="yellow", text=peg_string)
    LAB1.grid(row=10, column=4, pady=4, padx=4, sticky=W)
    BUT4_1 = Button(FRAME4, bg=temp_bc4_1, text=" ")
    BUT4_1.grid(row=10, column=0, pady=4, padx=4)
    BUT4_1.configure(state=DISABLED)
    BUT4_2 = Button(FRAME4, bg=temp_bc4_2, text=" ")
    BUT4_2.grid(row=10, column=1, pady=4, padx=4)
    BUT4_2.configure(state=DISABLED)
    BUT4_3 = Button(FRAME4, bg=temp_bc4_3, text=" ")
    BUT4_3.grid(row=10, column=2, pady=4, padx=4)
    BUT4_3.configure(state=DISABLED)
    BUT4_4 = Button(FRAME4, bg=temp_bc4_4, text=" ")
    BUT4_4.grid(row=10, column=3, pady=4, padx=4)
    BUT4_4.configure(state=DISABLED)

    DECODE_BUTTON_5.configure(state=NORMAL)

    compare_guess_solution(user_guess)


def clk_but_4_1():
    """Player clicked but4_1 to change its colour."""
    global temp_bc4_1

    button_row_4.button_1 += 1

    if button_row_4.button_1 == 7:
        button_row_4.button_1 = 1

    bc = button_row_4.button_1
    current_buttons[0] = str(colors[bc - 1])

    BUT4_1 = Button(
        FRAME4, bg=current_buttons[0], text=" ", command=clk_but_4_1
    )
    BUT4_1.grid(row=10, column=0, pady=4, padx=4)

    temp_bc4_1 = current_buttons[0]


def clk_but_4_2():
    """Player clicked but4_2 to change its colour."""
    global temp_bc4_2

    button_row_4.button_2 += 1

    if button_row_4.button_2 == 7:
        button_row_4.button_2 = 1

    bc = button_row_4.button_2
    current_buttons[1] = str(colors[bc - 1])

    BUT4_2 = Button(
        FRAME4, bg=current_buttons[1], text=" ", command=clk_but_4_2
    )
    BUT4_2.grid(row=10, column=1, pady=4, padx=4)

    temp_bc4_2 = current_buttons[1]


def clk_but_4_3():
    """Player clicked but4_3 to change its colour."""
    global temp_bc4_3

    button_row_4.button_3 += 1

    if button_row_4.button_3 == 7:
        button_row_4.button_3 = 1

    bc = button_row_4.button_3
    current_buttons[2] = str(colors[bc - 1])

    BUT4_3 = Button(
        FRAME4, bg=current_buttons[2], text=" ", command=clk_but_4_3
    )
    BUT4_3.grid(row=10, column=2, pady=4, padx=4)

    temp_bc4_3 = current_buttons[2]


def clk_but_4_4():
    """Player clicked but4_4 to change its colour."""
    global temp_bc4_4

    button_row_4.button_4 += 1

    if button_row_4.button_4 == 7:
        button_row_4.button_4 = 1

    bc = button_row_4.button_4
    current_buttons[3] = str(colors[bc - 1])

    BUT4_4 = Button(
        FRAME4, bg=current_buttons[3], text=" ", command=clk_but_4_4
    )
    BUT4_4.grid(row=10, column=3, pady=4, padx=4)

    temp_bc4_4 = current_buttons[3]


# ---------------------------start row 5---------------------------------------
def decode_row5():
    """Decode button for row 5 has been clicked so check input."""
    global user_guess

    if (
        button_row_5.button_1 == 0
        or button_row_5.button_2 == 0
        or button_row_5.button_3 == 0
        or button_row_5.button_4 == 0
    ):
        return

    DECODE_BUTTON_5.configure(state=DISABLED)

    user_guess = [temp_bc5_1, temp_bc5_2, temp_bc5_3, temp_bc5_4]

    peg_string = game.generate_peg_string(user_guess)

    LAB5 = Label(FRAME5, bg="yellow", text=peg_string)
    LAB5.grid(row=11, column=4, pady=4, padx=4, sticky=W)

    BUT5_1 = Button(FRAME5, bg=temp_bc5_1, text=" ")
    BUT5_1.grid(row=11, column=0, pady=4, padx=4)
    BUT5_1.configure(state=DISABLED)
    BUT5_2 = Button(FRAME5, bg=temp_bc5_2, text=" ")
    BUT5_2.grid(row=11, column=1, pady=4, padx=4)
    BUT5_2.configure(state=DISABLED)
    BUT5_3 = Button(FRAME5, bg=temp_bc5_3, text=" ")
    BUT5_3.grid(row=11, column=2, pady=4, padx=4)
    BUT5_3.configure(state=DISABLED)
    BUT5_4 = Button(FRAME5, bg=temp_bc5_4, text=" ")
    BUT5_4.grid(row=11, column=3, pady=4, padx=4)
    BUT5_4.configure(state=DISABLED)

    DECODE_BUTTON_6.configure(state=NORMAL)

    compare_guess_solution(user_guess)


def clk_but_5_1():
    """Player clicked but5_1 to change its colour."""
    global temp_bc5_1

    button_row_5.button_1 += 1

    if button_row_5.button_1 == 7:
        button_row_5.button_1 = 1

    bc = button_row_5.button_1
    current_buttons[0] = str(colors[bc - 1])

    BUT5_1 = Button(
        FRAME5, bg=current_buttons[0], text=" ", command=clk_but_5_1
    )
    BUT5_1.grid(row=11, column=0, pady=4, padx=4)

    temp_bc5_1 = current_buttons[0]


def clk_but_5_2():
    """Player clicked but5_2 to change its colour."""
    global temp_bc5_2

    button_row_5.button_2 += 1

    if button_row_5.button_2 == 7:
        button_row_5.button_2 = 1

    bc = button_row_5.button_2
    current_buttons[1] = str(colors[bc - 1])

    BUT5_2 = Button(
        FRAME5, bg=current_buttons[1], text=" ", command=clk_but_5_2
    )
    BUT5_2.grid(row=11, column=1, pady=4, padx=4)

    temp_bc5_2 = current_buttons[1]


def clk_but_5_3():
    """Player clicked but5_3 to change its colour."""
    global temp_bc5_3

    button_row_5.button_3 += 1

    if button_row_5.button_3 == 7:
        button_row_5.button_3 = 1

    bc = button_row_5.button_3
    current_buttons[2] = str(colors[bc - 1])

    BUT5_3 = Button(
        FRAME5, bg=current_buttons[2], text=" ", command=clk_but_5_3
    )
    BUT5_3.grid(row=11, column=2, pady=4, padx=4)

    temp_bc5_3 = current_buttons[2]


def clk_but_5_4():
    """Player clicked but5_4 to change its colour."""
    global temp_bc5_4

    button_row_5.button_4 += 1

    if button_row_5.button_4 == 7:
        button_row_5.button_4 = 1

    bc = button_row_5.button_4
    current_buttons[3] = str(colors[bc - 1])

    BUT5_4 = Button(
        FRAME5, bg=current_buttons[3], text=" ", command=clk_but_5_4
    )
    BUT5_4.grid(row=11, column=3, pady=4, padx=4)

    temp_bc5_4 = current_buttons[3]


# ---start row 6---------------------------------------------------------------


def decode_row6():
    """Decode button for row 6 has been clicked so check input."""
    global user_guess

    if (
        button_row_6.button_1 == 0
        or button_row_6.button_2 == 0
        or button_row_6.button_3 == 0
        or button_row_6.button_4 == 0
    ):
        return

    DECODE_BUTTON_6.configure(state=DISABLED)
    user_guess = [temp_bc6_1, temp_bc6_2, temp_bc6_3, temp_bc6_4]

    peg_string = game.generate_peg_string(user_guess)

    LAB6 = Label(FRAME6, bg="yellow", text=peg_string)
    LAB6.grid(row=12, column=4, pady=4, padx=4, sticky=W)

    BUT6_1 = Button(FRAME6, bg=temp_bc6_1, text=" ")
    BUT6_1.grid(row=12, column=0, pady=4, padx=4)
    BUT6_1.configure(state=DISABLED)
    BUT6_2 = Button(FRAME6, bg=temp_bc6_2, text=" ")
    BUT6_2.grid(row=12, column=1, pady=4, padx=4)
    BUT6_2.configure(state=DISABLED)
    BUT6_3 = Button(FRAME6, bg=temp_bc6_3, text=" ")
    BUT6_3.grid(row=12, column=2, pady=4, padx=4)
    BUT6_3.configure(state=DISABLED)
    BUT6_4 = Button(FRAME6, bg=temp_bc6_4, text=" ")
    BUT6_4.grid(row=12, column=3, pady=4, padx=4)

    BUT6_4.configure(state=DISABLED)

    compare_guess_solution(user_guess)


def clk_but_6_1():
    """Player clicked but6_1 to change its colour."""
    global temp_bc6_1

    button_row_6.button_1 += 1

    if button_row_6.button_1 == 7:
        button_row_6.button_1 = 1

    bc = button_row_6.button_1
    current_buttons[0] = str(colors[bc - 1])

    BUT6_1 = Button(
        FRAME6, bg=current_buttons[0], text=" ", command=clk_but_6_1
    )
    BUT6_1.grid(row=12, column=0, pady=4, padx=4)

    temp_bc6_1 = current_buttons[0]


def clk_but_6_2():
    """Player clicked but6_2 to change its colour."""
    global temp_bc6_2

    button_row_6.button_2 += 1

    if button_row_6.button_2 == 7:
        button_row_6.button_2 = 1

    bc = button_row_6.button_2
    current_buttons[1] = str(colors[bc - 1])

    BUT6_2 = Button(
        FRAME6, bg=current_buttons[1], text=" ", command=clk_but_6_2
    )
    BUT6_2.grid(row=12, column=1, pady=4, padx=4)

    temp_bc6_2 = current_buttons[1]


def clk_but_6_3():
    """Player clicked but6_3 to change its colour."""
    global temp_bc6_3

    button_row_6.button_3 += 1

    if button_row_6.button_3 == 7:
        button_row_6.button_3 = 1

    bc = button_row_6.button_3
    current_buttons[2] = str(colors[bc - 1])

    BUT6_3 = Button(
        FRAME6, bg=current_buttons[2], text=" ", command=clk_but_6_3
    )
    BUT6_3.grid(row=12, column=2, pady=4, padx=4)

    temp_bc6_3 = current_buttons[2]


def clk_but_6_4():
    """Player clicked but6_4 to change its colour."""
    global temp_bc6_4

    button_row_6.button_4 += 1

    if button_row_6.button_4 == 7:
        button_row_6.button_4 = 1

    bc = button_row_6.button_4
    current_buttons[3] = str(colors[bc - 1])

    BUT6_4 = Button(
        FRAME6, bg=current_buttons[3], text=" ", command=clk_but_6_4
    )
    BUT6_4.grid(row=12, column=3, pady=4, padx=4)

    temp_bc6_4 = current_buttons[3]


# -----------------------------end row 6---------------------------------------


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


# game Message.
FRAME0 = LabelFrame(ROOT, fg="blue", text="Bletchley", relief=SUNKEN)
FRAME0.grid(padx=1, pady=1)

FRAME10 = LabelFrame(ROOT, fg="blue", text="Bletchley v4.083", relief=SUNKEN)
FRAME10.grid()
LAB10 = Label(
    FRAME10,
    text="Can you crack the code?\n\n"
    "* = Correct colour and position.\n x = Correct colour, wrong position.\n"
    "blank = No colours in code",
)
LAB10.grid(pady=4, padx=4)

# Attempt 1 buttons.
FRAME1 = LabelFrame(ROOT, fg="blue", text="Attempt 1", relief=SUNKEN)
FRAME1.grid()
BUT1_1 = Button(FRAME1, bg="skyblue", text=" ", command=clk_but_1_1)
BUT1_1.grid(row=7, column=0, pady=4, padx=4)
BUT1_2 = Button(FRAME1, bg="skyblue", text=" ", command=clk_but_1_2)
BUT1_2.grid(row=7, column=1, pady=4, padx=4)
BUT1_3 = Button(FRAME1, bg="skyblue", text=" ", command=clk_but_1_3)
BUT1_3.grid(row=7, column=2, pady=4, padx=4)
BUT1_4 = Button(FRAME1, bg="skyblue", text=" ", command=clk_but_1_4)
BUT1_4.grid(row=7, column=3, pady=4, padx=4)
LAB1 = Label(FRAME1, bg="yellow", text="        ")
LAB1.grid(row=7, column=4, pady=4, padx=4)
DECODE_BUTTON_1 = Button(FRAME1, bg="green2", text="DECODE", command=decode_robutton_row_5)
DECODE_BUTTON_1.grid(row=7, column=5, pady=4, padx=4)

# Attempt 2 buttons.
FRAME2 = LabelFrame(ROOT, fg="blue", text="Attempt 2", relief=SUNKEN)
FRAME2.grid()
BUT2_1 = Button(FRAME2, bg="skyblue", text=" ", command=clk_but_2_1)
BUT2_1.grid(row=8, column=0, pady=4, padx=4)
BUT2_2 = Button(FRAME2, bg="skyblue", text=" ", command=clk_but_2_2)
BUT2_2.grid(row=8, column=1, pady=4, padx=4)
BUT2_3 = Button(FRAME2, bg="skyblue", text=" ", command=clk_but_2_3)
BUT2_3.grid(row=8, column=2, pady=4, padx=4)
BUT2_4 = Button(FRAME2, bg="skyblue", text=" ", command=clk_but_2_4)
BUT2_4.grid(row=8, column=3, pady=4, padx=4)
LAB2 = Label(FRAME2, bg="yellow", text="        ")
LAB2.grid(row=8, column=4, pady=4, padx=4)
DECODE_BUTTON_2 = Button(FRAME2, bg="green2", text="DECODE", command=decode_row2)
DECODE_BUTTON_2.grid(row=8, column=5, pady=4, padx=4)

# Attempt 3 buttons.
FRAME3 = LabelFrame(ROOT, fg="blue", text="Attempt 3", relief=SUNKEN)
FRAME3.grid()
BUT3_1 = Button(FRAME3, bg="skyblue", text=" ", command=clk_but_3_1)
BUT3_1.grid(row=9, column=0, pady=4, padx=4)
BUT3_2 = Button(FRAME3, bg="skyblue", text=" ", command=clk_but_3_2)
BUT3_2.grid(row=9, column=1, pady=4, padx=4)
BUT3_3 = Button(FRAME3, bg="skyblue", text=" ", command=clk_but_3_3)
BUT3_3.grid(row=9, column=2, pady=4, padx=4)
BUT3_4 = Button(FRAME3, bg="skyblue", text=" ", command=clk_but_3_4)
BUT3_4.grid(row=9, column=3, pady=4, padx=4)
LAB3 = Label(FRAME3, bg="yellow", text="        ")
LAB3.grid(row=9, column=4, pady=4, padx=4)
DECODE_BUTTON_3 = Button(FRAME3, bg="green2", text="DECODE", command=decode_row3)
DECODE_BUTTON_3.grid(row=9, column=5, pady=4, padx=4)

# Attempt 4 buttons.
FRAME4 = LabelFrame(ROOT, fg="blue", text="Attempt 4", relief=SUNKEN)
FRAME4.grid()
BUT4_1 = Button(FRAME4, bg="skyblue", text=" ", command=clk_but_4_1)
BUT4_1.grid(row=10, column=0, pady=4, padx=4)
BUT4_2 = Button(FRAME4, bg="skyblue", text=" ", command=clk_but_4_2)
BUT4_2.grid(row=10, column=1, pady=4, padx=4)
BUT4_3 = Button(FRAME4, bg="skyblue", text=" ", command=clk_but_4_3)
BUT4_3.grid(row=10, column=2, pady=4, padx=4)
BUT4_4 = Button(FRAME4, bg="skyblue", text=" ", command=clk_but_4_4)
BUT4_4.grid(row=10, column=3, pady=4, padx=4)
LAB4 = Label(FRAME4, bg="yellow", text="        ")
LAB4.grid(row=10, column=4, pady=4, padx=4)
DECODE_BUTTON_4 = Button(FRAME4, bg="green2", text="DECODE", command=decode_row4)
DECODE_BUTTON_4.grid(row=10, column=5, pady=4, padx=4)

# Attempt 5 buttons.
FRAME5 = LabelFrame(ROOT, fg="blue", text="Attempt 5", relief=SUNKEN)
FRAME5.grid()
BUT5_1 = Button(FRAME5, bg="skyblue", text=" ", command=clk_but_5_1)
BUT5_1.grid(row=11, column=0, pady=4, padx=4)
BUT5_2 = Button(FRAME5, bg="skyblue", text=" ", command=clk_but_5_2)
BUT5_2.grid(row=11, column=1, pady=4, padx=4)
BUT5_3 = Button(FRAME5, bg="skyblue", text=" ", command=clk_but_5_3)
BUT5_3.grid(row=11, column=2, pady=4, padx=4)
BUT5_4 = Button(FRAME5, bg="skyblue", text=" ", command=clk_but_5_4)
BUT5_4.grid(row=11, column=3, pady=4, padx=4)
LAB5 = Label(FRAME5, bg="yellow", text="        ")
LAB5.grid(row=11, column=4, pady=4, padx=4)
DECODE_BUTTON_5 = Button(FRAME5, bg="green2", text="DECODE", command=decode_row5)
DECODE_BUTTON_5.grid(row=11, column=5, pady=4, padx=4)

# Attempt 6 buttons.
FRAME6 = LabelFrame(ROOT, fg="blue", text="Attempt 6", relief=SUNKEN)
FRAME6.grid()
BUT6_1 = Button(FRAME6, bg="skyblue", text=" ", command=clk_but_6_1)
BUT6_1.grid(row=12, column=0, pady=4, padx=4)
BUT6_2 = Button(FRAME6, bg="skyblue", text=" ", command=clk_but_6_2)
BUT6_2.grid(row=12, column=1, pady=4, padx=4)
BUT6_3 = Button(FRAME6, bg="skyblue", text=" ", command=clk_but_6_3)
BUT6_3.grid(row=12, column=2, pady=4, padx=4)
BUT6_4 = Button(FRAME6, bg="skyblue", text=" ", command=clk_but_6_4)
BUT6_4.grid(row=12, column=3, pady=4, padx=4)
LAB6 = Label(FRAME6, bg="yellow", text="        ")
LAB6.grid(row=12, column=4, pady=4, padx=4)
DECODE_BUTTON_6 = Button(FRAME6, bg="green2", text="DECODE", command=decode_row6)
DECODE_BUTTON_6.grid(row=12, column=5, pady=4, padx=4)

# Initiaize classes.
# game ect. is just a name we can make up to reference the class
# and pass the initial state of the variables to it.
game = BletchleyGame()
button_row_1 = button_up_row(0, 0, 0, 0)
button_row_2 = button_up_row(0, 0, 0, 0)
button_row_3 = button_up_row(0, 0, 0, 0)
button_row_4 = button_up_row(0, 0, 0, 0)
button_row_5 = button_up_row(0, 0, 0, 0)
button_row_6 = button_up_row(0, 0, 0, 0)

# Make sure player can only decode row 1 to start with
# by disabling all other decode buttons.
DECODE_BUTTON_2.configure(state=DISABLED)
DECODE_BUTTON_3.configure(state=DISABLED)
DECODE_BUTTON_4.configure(state=DISABLED)
DECODE_BUTTON_5.configure(state=DISABLED)
DECODE_BUTTON_6.configure(state=DISABLED)

# cover up secret code with a button.
SOLUTION_FRAME = LabelFrame(ROOT, fg="blue", text="solution", relief=SUNKEN)
SOLUTION_FRAME.grid()
SOLUTION_BUTTON = Button(SOLUTION_FRAME, bg="gold", text="REVEAL", command=reveal_solution)
SOLUTION_BUTTON.grid(row=9, column=5, pady=4, padx=4)

# ---Now program control is waiting for button clicks to commence game.-------

ROOT.mainloop()
