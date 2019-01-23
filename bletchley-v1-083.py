""" Bletchley, v1.083 """
# v1.083-improved quit game def.improved reveal solution into 1 def
# v1.082-made mp3s more effecient code and set to play infin til changed\stopped

import os
import random
import subprocess
import webbrowser
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
    messagebox,
)

import string_utils
from pygame import mixer

ROOT = Tk()
ROOT.title("Bletchley v1.083")
ROOT.geometry("225x520")

# Initialize pygame music player.
mixer.init()

user_input = []
secret_code = []
colors = ["red", "blue", "white", "yellow", "green", "plum"]


def about_menu():
    """ Display about program info if selected in drop-down menu. """
    messagebox.showinfo("About", "Bletchley V1.083 by Steve Shambles jan 2019")


def visit_blog():
    """ Visit my python blog if selected in drop-down menu. """
    webbrowser.open("https://stevepython.wordpress.com/")


def visit_bensound():
    """ Visit bensound.com blog if selected in drop-down menu. """
    webbrowser.open("https://bensound.com/")


def play_music_track1():
    """ Play background music if "play track1 " clicked in drop-down menu. """
    play_mp3 = "music\\bensound-thelounge.mp3"
    play_track(play_mp3)


def play_music_track2():
    """ Play background music if "play track 2" clicked in drop-down menu."""
    play_mp3 = "music\\bensound-onceagain.mp3"
    play_track(play_mp3)


def play_music_track3():
    """ Play background music if "play track 3" clicked in drop-down menu. """
    play_mp3 = "music\\bensound-enigmatic.mp3"
    play_track(play_mp3)


def play_music_track4():
    """ Play background music if "play track 4" clicked in drop-down menu. """
    play_mp3 = "music\\bensound-betterdays.mp3"
    play_track(play_mp3)


def play_music_all():
    """ Play all tracks, as pygame queue doesnt work,
        I just glued the 4 tracks in one. """
    play_mp3 = "music\\all.mp3"
    play_track(play_mp3)


def play_track(play_mp3):
    """ Check file exists if so Play selected music."""
    if os.path.isfile(play_mp3):
        mixer.music.load(play_mp3)
        mixer.music.play(-1)  # play indefinetly -1. 0 or () = play once.
    else:
        messagebox.showinfo("Ouch!", "File is Missing dude")
        return


def stop_music():
    """ Stop music playing if selected in drop-down menu. """
    mixer.music.stop()


def QUIT():
    """ Completely quit the game."""
    stop_music()
    ROOT.destroy()


# Drop-down menu.
MENU_BAR = Menu(ROOT)
FILE_MENU = Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label="Menu", menu=FILE_MENU)
FILE_MENU.add_command(label="Visit Blog", command=visit_blog)
FILE_MENU.add_command(label="About", command=about_menu)
FILE_MENU.add_command(label="Exit", command=QUIT)

FILE_MENU2 = Menu(MENU_BAR, tearoff=0)
MENU_BAR.add_cascade(label="Music", menu=FILE_MENU2)
FILE_MENU2.add_command(label="Play The Lounge", command=play_music_track1)
FILE_MENU2.add_command(label="Play Once Again", command=play_music_track2)
FILE_MENU2.add_command(label="Play Enigmatic", command=play_music_track3)
FILE_MENU2.add_command(label="Play Better Days", command=play_music_track4)
FILE_MENU2.add_command(label="Play All", command=play_music_all)
FILE_MENU2.add_separator()
FILE_MENU2.add_command(label="Stop music", command=stop_music)
FILE_MENU2.add_command(
    label="Free music from Bensound.com", command=visit_bensound
)
ROOT.config(menu=MENU_BAR)

# -------------classes-----------------------------------------------------
# This is the first time I have used classes and I don't really understand
# fully what's going on. I put these classes in simply to avoid the use of
# global statements, there would of been about 60 of them otherwise :-).


class Solution:
    """ Store the four colours of the secret code. """

    def __init__(self):
        """'Create the secret code.

        This code comprises 4 colours, chosen at random from the following six
        colours: 1=red, 2=blue, 3=white, 4=yellow, 5=green, 6=plum.
        """
        global secret_code
        # First, generate four randomly-chosen colors and store them in a list.
        secret_code = [colors[random.randrange(0, 6)] for x in range(4)]
        # Print out the secret code, for test purpses.
        print("secret code is ", secret_code)
        # Create the secret_code_string by joining the four elements, each
        # separated by a single space.
        self.secret_code_string = " ".join(secret_code)
        # Assign the four elements of the secret code to the four secret pegs.
        [
            self.secret_peg1,
            self.secret_peg2,
            self.secret_peg3,
            self.secret_peg4,
        ] = secret_code


class outcome:
    """ Build a string of the hint pegs that go on the yellow label. """

    def __init__(self, out_come, out_come1, out_come2, out_come3, out_come4):
        self.out_come = out_come
        self.out_come1 = out_come1
        self.out_come2 = out_come2
        self.out_come3 = out_come3
        self.out_come4 = out_come4

    def glue_outcomes_together(self):
        """ Glue outcomes together. """
        self.out_come = (
            str(self.out_come1)
            + str(self.out_come2)
            + str(self.out_come3)
            + str(self.out_come4)
        )


class button_up_row1:
    """ Variabless for button colours for row 1. """

    def __init__(
        self,
        but_col_1_1,
        current_but_col,
        but_col_1_2,
        current_but_col2,
        but_col_1_3,
        current_but_col3,
        but_col_1_4,
        current_but_col4,
    ):

        self.but_col_1_1 = but_col_1_1
        self.current_but_col = current_but_col
        self.but_col_1_2 = but_col_1_2
        self.current_but_col2 = current_but_col2
        self.but_col_1_3 = but_col_1_3
        self.current_but_col3 = current_but_col3
        self.but_col_1_4 = but_col_1_4
        self.current_but_col4 = current_but_col4
        # s1 = button_up_row1 (0,"",0,"",0,"",0,"")


class button_up_row2:
    """ Variabless for button colours for row 2. """

    def __init__(self, but_col_2_1, but_col_2_2, but_col_2_3, but_col_2_4):

        self.but_col_2_1 = but_col_2_1
        self.but_col_2_2 = but_col_2_2
        self.but_col_2_3 = but_col_2_3
        self.but_col_2_4 = but_col_2_4
        # t1 = button_up_row2 (0,0,0,0)


class button_up_row3:
    """ Variabless for button colours for row 3. """

    def __init__(self, but_col_3_1, but_col_3_2, but_col_3_3, but_col_3_4):

        self.but_col_3_1 = but_col_3_1
        self.but_col_3_2 = but_col_3_2
        self.but_col_3_3 = but_col_3_3
        self.but_col_3_4 = but_col_3_4
        # u1 = button_up_row3 (0,0,0,0)


class button_up_row4:
    """ Variabless for button colours for row 4. """

    def __init__(self, but_col_4_1, but_col_4_2, but_col_4_3, but_col_4_4):

        self.but_col_4_1 = but_col_4_1
        self.but_col_4_2 = but_col_4_2
        self.but_col_4_3 = but_col_4_3
        self.but_col_4_4 = but_col_4_4
        # v1 = button_up_row4 (0,0,0,0)


class button_up_row5:
    """ Variabless for button colours for row 5. """

    def __init__(self, but_col_5_1, but_col_5_2, but_col_5_3, but_col_5_4):

        self.but_col_5_1 = but_col_5_1
        self.but_col_5_2 = but_col_5_2
        self.but_col_5_3 = but_col_5_3
        self.but_col_5_4 = but_col_5_4
        # w1 = button_up_row5 (0,0,0,0)


class button_up_row6:
    """ Variabless for button colours for row 6. """

    def __init__(self, but_col_6_1, but_col_6_2, but_col_6_3, but_col_6_4):

        self.but_col_6_1 = but_col_6_1
        self.but_col_6_2 = but_col_6_2
        self.but_col_6_3 = but_col_6_3
        self.but_col_6_4 = but_col_6_4


# -----------------------------row 1 functions----------------------------
def decode_row1():
    """ Check result of the decode button press for row 1. """
    global user_input

    # exit if all 4 colours not entered yet
    if (
        s1.but_col_1_1 == 0
        or s1.but_col_1_2 == 0
        or s1.but_col_1_3 == 0
        or s1.but_col_1_4 == 0
    ):
        return

    # Disable decode button, so no cheating.
    BUT1_5.configure(state=DISABLED)

    # Build user_input string.
    user_input = [temp_bc1_1, temp_bc1_2, temp_bc1_3, temp_bc1_4]

    # Check user-input against secret_code.
    compare_guess_solution(user_input, secret_code)

    # Construct the outcome string for output to the yesllow label.
    r1.out_come = ""
    if black:
        r1.out_come = "*" * black
    if white:
        r1.out_come = r1.out_come + "x" * white

    if black == 0 and white == 0:
        r1.out_come = "0000"

    # rnd shuffle the out_come answer so player does not see order of results
    shuffled = string_utils.shuffle(r1.out_come)

    # display outcome in gui on yellow label
    LAB1 = Label(FRAME1, bg="yellow", text=shuffled)
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
    BUT2_5.configure(state=NORMAL)


def clk_but_1_1():
    """ Player clicked but1_1 to change its colour. """
    global temp_bc1_1

    # Select next colour 1-6.
    s1.but_col_1_1 += 1

    # If last colour+1 (6+1), then loop it to first colour.
    if s1.but_col_1_1 == 7:
        s1.but_col_1_1 = 1

    # Convert integer to actual text colour to use as button fg colour.
    bc = s1.but_col_1_1
    s1.current_but_col = str(colors[bc - 1])

    # Store colour selected for later use in disabling this button.
    temp_bc1_1 = s1.current_but_col

    # Now actually change the button colour and display
    BUT1_1 = Button(
        FRAME1, bg=s1.current_but_col, text=" ", command=clk_but_1_1
    )
    BUT1_1.grid(row=7, column=0, pady=4, padx=4)


def clk_but_1_2():
    """ Player clicked but1_2 to change its colour. """
    global temp_bc1_2

    s1.but_col_1_2 += 1

    if s1.but_col_1_2 == 7:
        s1.but_col_1_2 = 1

    bc = s1.but_col_1_2
    s1.current_but_col2 = str(colors[bc - 1])

    temp_bc1_2 = s1.current_but_col2

    BUT1_2 = Button(
        FRAME1, bg=s1.current_but_col2, text=" ", command=clk_but_1_2
    )
    BUT1_2.grid(row=7, column=1, pady=4, padx=4)


def clk_but_1_3():
    """ Player clicked but1_3 to change its colour. """
    global temp_bc1_3

    s1.but_col_1_3 += 1

    if s1.but_col_1_3 == 7:
        s1.but_col_1_3 = 1

    bc = s1.but_col_1_3
    s1.current_but_col3 = str(colors[bc - 1])

    temp_bc1_3 = s1.current_but_col3

    BUT1_3 = Button(
        FRAME1, bg=s1.current_but_col3, text=" ", command=clk_but_1_3
    )
    BUT1_3.grid(row=7, column=2, pady=4, padx=4)


def clk_but_1_4():
    """ Player clicked but1_4 to change its colour."""
    global temp_bc1_4

    s1.but_col_1_4 += 1

    if s1.but_col_1_4 == 7:
        s1.but_col_1_4 = 1

    bc = s1.but_col_1_4
    s1.current_but_col4 = str(colors[bc - 1])

    temp_bc1_4 = s1.current_but_col4

    BUT1_4 = Button(
        FRAME1, bg=s1.current_but_col4, text=" ", command=clk_but_1_4
    )
    BUT1_4.grid(row=7, column=3, pady=4, padx=4)


# -------------------------row 2-------------------------------------------


def decode_row2():
    """ Decode button for row 2 has been clicked so check input. """
    global user_input

    if (
        t1.but_col_2_1 == 0
        or t1.but_col_2_2 == 0
        or t1.but_col_2_3 == 0
        or t1.but_col_2_4 == 0
    ):
        return

    BUT2_5.configure(state=DISABLED)

    user_input = [temp_bc2_1, temp_bc2_2, temp_bc2_3, temp_bc2_4]

    compare_guess_solution(user_input, secret_code)

    r1.out_come = ""
    if black:
        r1.out_come = "*" * black
    if white:
        r1.out_come = r1.out_come + "x" * white
    if black == 0 and white == 0:
        r1.out_come = "0000"

    shuffled = string_utils.shuffle(r1.out_come)

    LAB1 = Label(FRAME2, bg="yellow", text=shuffled)
    LAB1.grid(row=8, column=4, pady=4, padx=4, sticky=W)

    BUT3_5.configure(state=NORMAL)
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


def clk_but_2_1():
    """ Player clicked but2_1 to change its colour. """
    global temp_bc2_1

    t1.but_col_2_1 += 1

    if t1.but_col_2_1 == 7:
        t1.but_col_2_1 = 1

    bc = t1.but_col_2_1
    s1.current_but_col = str(colors[bc - 1])

    BUT2_1 = Button(
        FRAME2, bg=s1.current_but_col, text=" ", command=clk_but_2_1
    )
    BUT2_1.grid(row=8, column=0, pady=4, padx=4)

    temp_bc2_1 = s1.current_but_col


def clk_but_2_2():
    """ Player clicked but2_2 to change its colour. """
    global temp_bc2_2

    t1.but_col_2_2 += 1

    if t1.but_col_2_2 == 7:
        t1.but_col_2_2 = 1

    bc = t1.but_col_2_2
    s1.current_but_col2 = str(colors[bc - 1])

    BUT2_2 = Button(
        FRAME2, bg=s1.current_but_col2, text=" ", command=clk_but_2_2
    )
    BUT2_2.grid(row=8, column=1, pady=4, padx=4)

    temp_bc2_2 = s1.current_but_col2


def clk_but_2_3():
    """ Player clicked but2_3 to change its colour. """
    global temp_bc2_3

    t1.but_col_2_3 += 1

    if t1.but_col_2_3 == 7:
        t1.but_col_2_3 = 1

    bc = t1.but_col_2_3
    s1.current_but_col3 = str(colors[bc - 1])

    BUT2_3 = Button(
        FRAME2, bg=s1.current_but_col3, text=" ", command=clk_but_2_3
    )
    BUT2_3.grid(row=8, column=2, pady=4, padx=4)

    temp_bc2_3 = s1.current_but_col3


def clk_but_2_4():
    """ Player clicked but2_4 to change its colour. """
    global temp_bc2_4

    t1.but_col_2_4 += 1

    if t1.but_col_2_4 == 7:
        t1.but_col_2_4 = 1

    bc = t1.but_col_2_4
    s1.current_but_col4 = str(colors[bc - 1])

    BUT2_4 = Button(
        FRAME2, bg=s1.current_but_col4, text=" ", command=clk_but_2_4
    )
    BUT2_4.grid(row=8, column=3, pady=4, padx=4)

    temp_bc2_4 = s1.current_but_col4


# -------------------------row 3------------------------------------------------


def decode_row3():
    """ Decode button for row 3 has been clicked so check input. """
    global user_input

    if (
        u1.but_col_3_1 == 0
        or u1.but_col_3_2 == 0
        or u1.but_col_3_3 == 0
        or u1.but_col_3_4 == 0
    ):
        return

    BUT3_5.configure(state=DISABLED)
    user_input = [temp_bc3_1, temp_bc3_2, temp_bc3_3, temp_bc3_4]

    compare_guess_solution(user_input, secret_code)

    r1.out_come = ""
    if black:
        r1.out_come = "*" * black
    if white:
        r1.out_come = r1.out_come + "x" * white
    if black == 0 and white == 0:
        r1.out_come = "0000"

    shuffled = string_utils.shuffle(r1.out_come)

    LAB1 = Label(FRAME3, bg="yellow", text=shuffled)
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

    BUT4_5.configure(state=NORMAL)


def clk_but_3_1():
    """ Player clicked but3_1 to change its colour. """
    global temp_bc3_1

    u1.but_col_3_1 += 1

    if u1.but_col_3_1 == 7:
        u1.but_col_3_1 = 1

    bc = u1.but_col_3_1
    s1.current_but_col = str(colors[bc - 1])

    BUT3_1 = Button(
        FRAME3, bg=s1.current_but_col, text=" ", command=clk_but_3_1
    )
    BUT3_1.grid(row=9, column=0, pady=4, padx=4)

    temp_bc3_1 = s1.current_but_col


def clk_but_3_2():
    """ Player clicked but3_2 to change its colour. """
    global temp_bc3_2

    u1.but_col_3_2 += 1

    if u1.but_col_3_2 == 7:
        u1.but_col_3_2 = 1

    bc = u1.but_col_3_2
    s1.current_but_col2 = str(colors[bc - 1])

    BUT3_2 = Button(
        FRAME3, bg=s1.current_but_col2, text=" ", command=clk_but_3_2
    )
    BUT3_2.grid(row=9, column=1, pady=4, padx=4)

    temp_bc3_2 = s1.current_but_col2


def clk_but_3_3():
    """ Player clicked but3_3 to change its colour. """
    global temp_bc3_3

    u1.but_col_3_3 += 1

    if u1.but_col_3_3 == 7:
        u1.but_col_3_3 = 1

    bc = u1.but_col_3_3
    s1.current_but_col3 = str(colors[bc - 1])

    BUT3_3 = Button(
        FRAME3, bg=s1.current_but_col3, text=" ", command=clk_but_3_3
    )
    BUT3_3.grid(row=9, column=2, pady=4, padx=4)

    temp_bc3_3 = s1.current_but_col3


def clk_but_3_4():
    """ Player clicked but 3_4 to change its colour. """
    global temp_bc3_4

    u1.but_col_3_4 += 1

    if u1.but_col_3_4 == 7:
        u1.but_col_3_4 = 1

    bc = u1.but_col_3_4
    s1.current_but_col4 = str(colors[bc - 1])

    BUT3_4 = Button(
        FRAME3, bg=s1.current_but_col4, text=" ", command=clk_but_3_4
    )
    BUT3_4.grid(row=9, column=3, pady=4, padx=4)

    temp_bc3_4 = s1.current_but_col4


# --------------------------start row 4----------------------------------------


def decode_row4():
    """ Decode button for row 4 has been clicked so check input. """
    global user_input

    if (
        v1.but_col_4_1 == 0
        or v1.but_col_4_2 == 0
        or v1.but_col_4_3 == 0
        or v1.but_col_4_4 == 0
    ):
        return

    BUT4_5.configure(state=DISABLED)
    user_input = [temp_bc4_1, temp_bc4_2, temp_bc4_3, temp_bc4_4]

    compare_guess_solution(user_input, secret_code)

    r1.out_come = ""
    if black:
        r1.out_come = "*" * black
    if white:
        r1.out_come = r1.out_come + "x" * white
    if black == 0 and white == 0:
        r1.out_come = "0000"

    shuffled = string_utils.shuffle(r1.out_come)

    LAB1 = Label(FRAME4, bg="yellow", text=shuffled)
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

    BUT5_5.configure(state=NORMAL)


def clk_but_4_1():
    """ Player clicked but4_1 to change its colour. """
    global temp_bc4_1

    v1.but_col_4_1 += 1

    if v1.but_col_4_1 == 7:
        v1.but_col_4_1 = 1

    bc = v1.but_col_4_1
    s1.current_but_col = str(colors[bc - 1])

    BUT4_1 = Button(
        FRAME4, bg=s1.current_but_col, text=" ", command=clk_but_4_1
    )
    BUT4_1.grid(row=10, column=0, pady=4, padx=4)

    temp_bc4_1 = s1.current_but_col


def clk_but_4_2():
    """ Player clicked but4_2 to change its colour. """

    global temp_bc4_2

    v1.but_col_4_2 += 1

    if v1.but_col_4_2 == 7:
        v1.but_col_4_2 = 1

    bc = v1.but_col_4_2
    s1.current_but_col2 = str(colors[bc - 1])

    BUT4_2 = Button(
        FRAME4, bg=s1.current_but_col2, text=" ", command=clk_but_4_2
    )
    BUT4_2.grid(row=10, column=1, pady=4, padx=4)

    temp_bc4_2 = s1.current_but_col2


def clk_but_4_3():
    """ Player clicked but4_3 to change its colour. """
    global temp_bc4_3

    v1.but_col_4_3 += 1

    if v1.but_col_4_3 == 7:
        v1.but_col_4_3 = 1

    bc = v1.but_col_4_3
    s1.current_but_col3 = str(colors[bc - 1])

    BUT4_3 = Button(
        FRAME4, bg=s1.current_but_col3, text=" ", command=clk_but_4_3
    )
    BUT4_3.grid(row=10, column=2, pady=4, padx=4)

    temp_bc4_3 = s1.current_but_col3


def clk_but_4_4():
    """ Player clicked but4_4 to change its colour. """
    global temp_bc4_4

    v1.but_col_4_4 += 1

    if v1.but_col_4_4 == 7:
        v1.but_col_4_4 = 1

    bc = v1.but_col_4_4
    s1.current_but_col4 = str(colors[bc - 1])

    BUT4_4 = Button(
        FRAME4, bg=s1.current_but_col4, text=" ", command=clk_but_4_4
    )
    BUT4_4.grid(row=10, column=3, pady=4, padx=4)

    temp_bc4_4 = s1.current_but_col4


# ---------------------------start row 5----------------------------------------
def decode_row5():
    """ Decode button for row 5 has been clicked so check input. """
    global user_input

    if (
        w1.but_col_5_1 == 0
        or w1.but_col_5_2 == 0
        or w1.but_col_5_3 == 0
        or w1.but_col_5_4 == 0
    ):
        return

    BUT5_5.configure(state=DISABLED)

    user_input = [temp_bc5_1, temp_bc5_2, temp_bc5_3, temp_bc5_4]

    compare_guess_solution(user_input, secret_code)

    r1.out_come = ""
    if black:
        r1.out_come = "*" * black
    if white:
        r1.out_come = r1.out_come + "x" * white
    if black == 0 and white == 0:
        r1.out_come = "0000"

    shuffled = string_utils.shuffle(r1.out_come)

    LAB5 = Label(FRAME5, bg="yellow", text=shuffled)
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

    BUT6_5.configure(state=NORMAL)


def clk_but_5_1():
    """ Player clicked but5_1 to change its colour. """
    global temp_bc5_1

    w1.but_col_5_1 += 1

    if w1.but_col_5_1 == 7:
        w1.but_col_5_1 = 1

    bc = w1.but_col_5_1
    s1.current_but_col = str(colors[bc - 1])

    BUT5_1 = Button(
        FRAME5, bg=s1.current_but_col, text=" ", command=clk_but_5_1
    )
    BUT5_1.grid(row=11, column=0, pady=4, padx=4)

    temp_bc5_1 = s1.current_but_col


def clk_but_5_2():
    """ Player clicked but5_2 to change its colour. """
    global temp_bc5_2

    w1.but_col_5_2 += 1

    if w1.but_col_5_2 == 7:
        w1.but_col_5_2 = 1

    bc = w1.but_col_5_2
    s1.current_but_col2 = str(colors[bc - 1])

    BUT5_2 = Button(
        FRAME5, bg=s1.current_but_col2, text=" ", command=clk_but_5_2
    )
    BUT5_2.grid(row=11, column=1, pady=4, padx=4)

    temp_bc5_2 = s1.current_but_col2


def clk_but_5_3():
    """ Player clicked but5_3 to change its colour. """
    global temp_bc5_3

    w1.but_col_5_3 += 1

    if w1.but_col_5_3 == 7:
        w1.but_col_5_3 = 1

    bc = w1.but_col_5_3
    s1.current_but_col3 = str(colors[bc - 1])

    BUT5_3 = Button(
        FRAME5, bg=s1.current_but_col3, text=" ", command=clk_but_5_3
    )
    BUT5_3.grid(row=11, column=2, pady=4, padx=4)

    temp_bc5_3 = s1.current_but_col3


def clk_but_5_4():
    """ Player clicked but5_4 to change its colour. """
    global temp_bc5_4

    w1.but_col_5_4 += 1

    if w1.but_col_5_4 == 7:
        w1.but_col_5_4 = 1

    bc = w1.but_col_5_4
    s1.current_but_col4 = str(colors[bc - 1])

    BUT5_4 = Button(
        FRAME5, bg=s1.current_but_col4, text=" ", command=clk_but_5_4
    )
    BUT5_4.grid(row=11, column=3, pady=4, padx=4)

    temp_bc5_4 = s1.current_but_col4


# ---start row 6----------------------------------------------------------------


def decode_row6():
    """ Decode button for row 6 has been clicked so check input. """
    global user_input

    if (
        x1.but_col_6_1 == 0
        or x1.but_col_6_2 == 0
        or x1.but_col_6_3 == 0
        or x1.but_col_6_4 == 0
    ):
        return

    BUT6_5.configure(state=DISABLED)
    user_input = [temp_bc6_1, temp_bc6_2, temp_bc6_3, temp_bc6_4]

    compare_guess_solution(user_input, secret_code)

    r1.out_come = ""
    if black:
        r1.out_come = "*" * black
    if white:
        r1.out_come = r1.out_come + "x" * white
    if black == 0 and white == 0:
        r1.out_come = "0000"

    shuffled = string_utils.shuffle(r1.out_come)
    LAB6 = Label(FRAME6, bg="yellow", text=shuffled)
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


def clk_but_6_1():
    """ Player clicked but6_1 to change its colour. """
    global temp_bc6_1

    x1.but_col_6_1 += 1

    if x1.but_col_6_1 == 7:
        x1.but_col_6_1 = 1

    bc = x1.but_col_6_1
    s1.current_but_col = str(colors[bc - 1])

    BUT6_1 = Button(
        FRAME6, bg=s1.current_but_col, text=" ", command=clk_but_6_1
    )
    BUT6_1.grid(row=12, column=0, pady=4, padx=4)

    temp_bc6_1 = s1.current_but_col


def clk_but_6_2():
    """ Player clicked but6_2 to change its colour. """
    global temp_bc6_2

    x1.but_col_6_2 += 1

    if x1.but_col_6_2 == 7:
        x1.but_col_6_2 = 1

    bc = x1.but_col_6_2
    s1.current_but_col2 = str(colors[bc - 1])

    BUT6_2 = Button(
        FRAME6, bg=s1.current_but_col2, text=" ", command=clk_but_6_2
    )
    BUT6_2.grid(row=12, column=1, pady=4, padx=4)

    temp_bc6_2 = s1.current_but_col2


def clk_but_6_3():
    """ Player clicked but6_3 to change its colour."""
    global temp_bc6_3

    x1.but_col_6_3 += 1

    if x1.but_col_6_3 == 7:
        x1.but_col_6_3 = 1

    bc = x1.but_col_6_3
    s1.current_but_col3 = str(colors[bc - 1])

    BUT6_3 = Button(
        FRAME6, bg=s1.current_but_col3, text=" ", command=clk_but_6_3
    )
    BUT6_3.grid(row=12, column=2, pady=4, padx=4)

    temp_bc6_3 = s1.current_but_col3


def clk_but_6_4():
    """ Player clicked but6_4 to change its colour."""
    global temp_bc6_4

    x1.but_col_6_4 += 1

    if x1.but_col_6_4 == 7:
        x1.but_col_6_4 = 1

    bc = x1.but_col_6_4
    s1.current_but_col4 = str(colors[bc - 1])

    BUT6_4 = Button(
        FRAME6, bg=s1.current_but_col4, text=" ", command=clk_but_6_4
    )
    BUT6_4.grid(row=12, column=3, pady=4, padx=4)

    temp_bc6_4 = s1.current_but_col4


# -----------------------------end row 6---------------------------------------


def game_over_man():
    """ Game over, player guessed incorrectly. """

    messagebox.showinfo("Bletchley", "G A M E  O V E R  M A N\n\n")
    # subprocess.Popen("bletchley-v1-03.exe")
    QUIT()


def display_solution():
    BUT_SECRET1 = Button(FRAME9, bg=p1.secret_peg1)
    BUT_SECRET1.grid(row=0, column=4, pady=4, padx=4)
    BUT_SECRET2 = Button(FRAME9, bg=p1.secret_peg2)
    BUT_SECRET2.grid(row=0, column=5, pady=4, padx=4)
    BUT_SECRET3 = Button(FRAME9, bg=p1.secret_peg3)
    BUT_SECRET3.grid(row=0, column=6, pady=4, padx=4)
    BUT_SECRET3 = Button(FRAME9, bg=p1.secret_peg4)
    BUT_SECRET3.grid(row=0, column=7, pady=4, padx=4)


def check_victory():
    """ Player has cracked code. """
    global black

    if black < 4:
        return

    # Remove the "REVEAL" button to reveal secret code.
    BUT3_9.destroy()
    display_solution()
    ROOT.update()

    messagebox.showinfo(
        "Bletchley",
        "You genius, " "you cracked the code.\n\n Alan would be proud of you!",
    )
    # subprocess.Popen("bletchley-v1-03.exe")
    QUIT()


def reveal_solution():
    """ Reveal button has been clicked, so show secret_code. """
    # Remove the "REVEAL" button to reveal secret code.
    BUT3_9.destroy()
    display_solution()
    game_over_man()


def compare_guess_solution(user_input, secret_code):
    """ Check what player pegs match secret code. """
    global black
    global white
    black = 0
    white = 0
    secret_copy = secret_code[:]
    user_copy = user_input[:]

    for index, input in enumerate(user_copy):
        if input == secret_copy[index]:
            black += 1
            secret_copy[index] = "checked solution"
            user_copy[index] = "checked user"

    for index, input in enumerate(user_copy):
        for i, p in enumerate(secret_copy):
            if p == input:
                white += 1
                secret_copy[i] = "checked solution"
                break

    check_victory()


# game Message.
FRAME0 = LabelFrame(ROOT, fg="blue", text="Bletchley", relief=SUNKEN)
FRAME0.grid(padx=1, pady=1)

FRAME10 = LabelFrame(ROOT, fg="blue", text="Bletchley v1.083", relief=SUNKEN)
FRAME10.grid()
LAB10 = Label(
    FRAME10,
    text="Can you crack the code?\n\n"
    "* = Correct colour and position.\n x = Correct colour, wrong position.\n"
    "0000 = No colours in code",
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
BUT1_5 = Button(FRAME1, bg="green2", text="DECODE", command=decode_row1)
BUT1_5.grid(row=7, column=5, pady=4, padx=4)

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
BUT2_5 = Button(FRAME2, bg="green2", text="DECODE", command=decode_row2)
BUT2_5.grid(row=8, column=5, pady=4, padx=4)

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
BUT3_5 = Button(FRAME3, bg="green2", text="DECODE", command=decode_row3)
BUT3_5.grid(row=9, column=5, pady=4, padx=4)

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
BUT4_5 = Button(FRAME4, bg="green2", text="DECODE", command=decode_row4)
BUT4_5.grid(row=10, column=5, pady=4, padx=4)

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
BUT5_5 = Button(FRAME5, bg="green2", text="DECODE", command=decode_row5)
BUT5_5.grid(row=11, column=5, pady=4, padx=4)

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
BUT6_5 = Button(FRAME6, bg="green2", text="DECODE", command=decode_row6)
BUT6_5.grid(row=12, column=5, pady=4, padx=4)

# Initiaize classes.
# p1 ect. is just a name we can make up to reference the class
# and pass the initial state of the variables to it.
p1 = Solution()
r1 = outcome(0, 0, 0, 0, 0)
s1 = button_up_row1(0, "", 0, "", 0, "", 0, "")
t1 = button_up_row2(0, 0, 0, 0)
u1 = button_up_row3(0, 0, 0, 0)
v1 = button_up_row4(0, 0, 0, 0)
w1 = button_up_row5(0, 0, 0, 0)
x1 = button_up_row6(0, 0, 0, 0)

# Make sure player can only decode row 1 to start with
# by disabling all other decode buttons.
BUT2_5.configure(state=DISABLED)
BUT3_5.configure(state=DISABLED)
BUT4_5.configure(state=DISABLED)
BUT5_5.configure(state=DISABLED)
BUT6_5.configure(state=DISABLED)

# cover up secret code with a button.
FRAME9 = LabelFrame(ROOT, fg="blue", text="solution", relief=SUNKEN)
FRAME9.grid()
BUT3_9 = Button(FRAME9, bg="gold", text="REVEAL", command=reveal_solution)
BUT3_9.grid(row=9, column=5, pady=4, padx=4)

# ---Now program control is waiting for button clicks to commence game.-------

ROOT.mainloop()
