'''
Bletchley, V2.015r

By Steve Shambles, 1st Feb 2019.

With thanks for lots of help from CMSteffen.
I couldn't of finished this game properly without
Steffen's enormous effort to help refactor my code.

For more Python projects:
https://stevepython.wordpress.com/
'''

## changes\additions made by shambles for V2.15r
##---------------------------------------------------------
# Added centre_gui function to centre the game on screen

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
    messagebox,
    Tk,
    W,
)
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import os
from libs import music
from libs.game_logic import BletchleyGame

# Define the game title.
game_title = "Bletchley V2.15r"

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

        # store what row player is on for points purposes if wins
        self.attempt = row_index
        #add 1 as row_index ordered from 0-5 not 1-6
        self.attempt += 1

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

        PlayerStats.played += 1
        PlayerStats.wins += 1
        self.calc_points_won()
        self.calc_win_rate()
        self.save_stats()

        # Let them know they've won.
        showinfo(
            "Bletchley",
            "You genius, "
            "you cracked the code.\n\n    Alan would be proud of you!"
            "\n\nYou earned "+str(self.points)+" points for that win.",
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
        """Reset the GameWindow and start a new game, and build gui"""
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
        self.button_rows = {
            i: [None] * 4 for i in range(6)
        }

        # Construct the main window.
        self.ROOT = Tk()
        self.ROOT.title(game_title)
        self.ROOT.geometry("252x576")
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
                "Bletchley V2.15r by Steve Shambles Feb 2019",
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

        # Add stats menu
        self.STATS_MENU = Menu(self.MENU_BAR, tearoff=0)
        self.MENU_BAR.add_cascade(label="Stats", menu=self.STATS_MENU)
        self.STATS_MENU.add_command(
            label="View Your Stats", command=self.view_stats
        )
        self.STATS_MENU.add_command(
            label="Reset Your Stats", command=self.reset_stats
        )


        # Add the menu bar to the ROOT window.
        self.ROOT.config(menu=self.MENU_BAR)

        # Create frame for the image
        FRAME0 = LabelFrame(self.ROOT)
        FRAME0.grid(padx=18, pady=18)

        if not os.path.isfile("blt-panel-v2.png"):
            messagebox.showinfo("Player Stats",  \
            "The file 'blt-panel-v2.png' is missing\n"  \
            "from the current directory. Please replace it.")
            self.QUIT()

        IMAGE = Image.open('blt-panel-v2.png')
        PHOTO = ImageTk.PhotoImage(IMAGE)
        LABEL = Label(FRAME0, image=PHOTO)
        LABEL.IMAGE = PHOTO
        LABEL.grid(padx=2, pady=2)


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
            text="      REVEAL SECRET CODE      ",
            command=self.reveal_solution,
        )
        self.SOLUTION_BUTTON.grid(row=9, column=5, pady=4, padx=4)

        # Run the main loop.
        self.centre_gui()
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
        showinfo("Bletchley", "        G A M E  O V E R  M A N\n\n"  \
                 "     You can do better than that!\n\n"  \
                 "Try again to improve your game stats.")

        PlayerStats.played += 1
        PlayerStats.lost += 1
        self.calc_win_rate()
        self.save_stats()

        self.new_game()


    def view_stats(self):
        '''create an  info msg box'''
        messagebox.showinfo("Player Stats", "Games Played: "  \
        +str(PlayerStats.played)+"\n"+"  Games Won: "+str(PlayerStats.wins)  \
        +"\n"+"   Games Lost: "+str(PlayerStats.lost)  \
        +"\n"+"   Points Won: "+str(PlayerStats.points)  \
        +"\n"+"        Win rate: "+str(PlayerStats.win_rate)+"%")


    def reset_stats(self):
        '''Msbox asks to confirm or not, if so then resets stats to zero.'''
        QUEST = messagebox.askyesno('Really?', 'Are you sure you want '  \
        'to reset all your stats to zero?')

        if QUEST is False:
            return
        self.zero_all_stats()

    def zero_all_stats(self):
        '''Reset all stt to zero, either from menu by user or if stats
        file not found and new one created with zero stats'''
        all_stats = []
        PlayerStats.played = 0
        PlayerStats.wins = 0
        PlayerStats.lost = 0
        PlayerStats.points = 0
        PlayerStats.win_rate = 0
        self.save_stats()

    def calc_points_won(self):
        '''Do simple calc for points won depending on how many
           tries it took to win.'''

        pts = self.attempt * 10
        self.points = 70 - pts
        PlayerStats.points = PlayerStats.points + self.points

    def calc_win_rate(self):
        '''calculate percent wins to games ratio'''
        PlayerStats.win_rate = PlayerStats.wins  / PlayerStats.played *100

    def save_stats(self):
        '''Save playing history to a text file'''

        with open("bletchley.blt", 'w') as contents:

            save_string = str(PlayerStats.played)+str("\n")
            contents.write(save_string)
            save_string = str(PlayerStats.wins)+str("\n")
            contents.write(save_string)
            save_string = str(PlayerStats.lost)+str("\n")
            contents.write(save_string)
            save_string = str(PlayerStats.points)+str("\n")
            contents.write(save_string)
            save_string = str(PlayerStats.win_rate)+str("\n")
            contents.write(save_string)

    def check_stats_exists(self):
        '''Test that bletchley.blt file is there, if not creates new one.'''
        if not os.path.isfile("bletchley.blt"):
            with open("bletchley.blt", "w"):
                self.zero_all_stats()

    def load_stats(self):
        '''Load players playing history from text file.
           The info is stored one variable valueon each new line'''
        self.check_stats_exists()

        with open("bletchley.blt", 'r') as contents:

            SAVED_STATS = contents.read().split('\n')
            all_stats = (SAVED_STATS)

            PlayerStats.played = int((all_stats[0]))
            PlayerStats.wins = int((all_stats[1]))
            PlayerStats.lost = int((all_stats[2]))
            PlayerStats.points = int((all_stats[3]))
            PlayerStats.win_rate = float((all_stats[4]))
            PlayerStats.win_rate = round(PlayerStats.win_rate, 1)

    def centre_gui(self):
        '''Not my code, found on net somewhere, credit to unknown author
           It should centre the game on any screen, but on my 19 inch monitor
           it was too low so had to add -200 to POSITIONDOWN, no idea why.'''
        # Get values of the height and width of gui.
        WINDOWWIDTH = self.ROOT.winfo_reqwidth()
        WINDOWHEIGHT = self.ROOT.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        POSITIONRIGHT = int(self.ROOT.winfo_screenwidth()/2 - WINDOWWIDTH/2)
        POSITIONDOWN = int(self.ROOT.winfo_screenheight()/2 - WINDOWHEIGHT/2)

        # Positions the window in the center of the page.
        self.ROOT.geometry("+{}+{}".format(POSITIONRIGHT,POSITIONDOWN-200))

    def run(self):
        """Start the main loop."""
        self.load_stats()
        self.ROOT.mainloop()

class PlayerStats:
    '''Keep stats of games played by player, and store in a text file'''

    def __init__(self, played, wins, lost, points, win_rate):

        self.played = played
        self.wins = wins
        self.lost = lost
        self.points = points
        self.win_rate = win_rate



# Initialize the GameWindow class, thereby starting a new game.
game_window = GameWindow()





