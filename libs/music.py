"""The Music Library

This library enables us to play music from within the Bletchley application.
"""

import os
from pygame import mixer
from tkinter import messagebox

class Tunes(object):
    """A music-playing class."""

    def __init__(self, available_songs):
        """Initialize the Tunes class.

        The `available_songs` dictionary defines the song names and filenames
        of the various tunes available to this class. These are defined within
        the main Bletchley source code.
        """
        # Initialize pygame music player.
        self.mixer = mixer
        self.mixer.init()
        self.song_list = available_songs

    def play_track(self, song_file):
        """Play the user-selected music track from the drop-down menu.

        The `song_file` variable defines which track will be played, from the
        options defined in the above `available_songs` dictionary.
        """
        # Set the path to the specified music track. We're using os.path.join here
        # so that this function will work with any OS, not just Windows.
        track_file = os.path.join("music", song_file)
        # Check to ensure the track exists.
        if os.path.isfile(track_file):
            # If so, load the track...
            self.mixer.music.load(track_file)
            # Then play the track.
            #   self.mixer.music.play(-1): play indefinitely.
            #   self.mixer.music.play(0) or (): play once.
            self.mixer.music.play(-1)
        else:
            # The track doesn't exist. Let the user know.
            messagebox.showinfo("Ouch!", "File is missing dude!")
            #return

    def stop_music(self):
        """Stop music playing if selected in drop-down menu."""
        self.mixer.music.stop()

    def track_list(self):
        """Return the song list dictionary items."""
        return self.song_list.items()
