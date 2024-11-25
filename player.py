import psycopg2
import json
import os
import pygame
from database_manager import DatabaseManager


SOUNDS_CONFIG_FILE = "sounds_config.json"


class SoundPlayer:
    def __init__(self):
        self.sounds_config = self.load_sounds_config()
        self.sound_list = {num: category for num, category in enumerate(self.sounds_config.keys(), 1)}
        self.db = DatabaseManager()
        self.db.setup_database()
        pygame.mixer.init()  # Initialize the pygame mixer for playing sounds

    @staticmethod
    def load_sounds_config():
        """Load the sound configuration from JSON."""
        if not os.path.exists(SOUNDS_CONFIG_FILE):
            print(f"Error: {SOUNDS_CONFIG_FILE} not found!")
            return {}
        with open(SOUNDS_CONFIG_FILE, 'r') as file:
            return json.load(file)

    def play_sound(self, sound):
        """Play a sound based on the given type."""
        sound_file = self.sounds_config.get(sound)
        if sound_file and os.path.exists(sound_file):
            try:
                print(f"Playing {sound} sounds: {sound_file}")
                pygame.mixer.music.load(sound_file)  # Load the sound file
                pygame.mixer.music.play(-1)  # Play the sound on a loop
                input("Press Enter to stop playback.")  # Allow the user to stop playback
                pygame.mixer.music.stop()  # Stop the sound
            except pygame.error as e:
                print(f"Error playing sound: {e}")
        else:
            print(f"No sound configured for: {sound}")

    def save_favorite_sound(self, username, sound):
        """Save a sound to the user's favorites."""
        self.db.save_favorite_sound(username, sound)

    def get_favorite_sound(self, username):
        """Get user's favorite sound."""
        return self.db.get_favorite_sound(username)

    def get_user(self, username):
        """Retrieve the user's favorite sounds from the database."""
        return self.db.get_user(username)
    
    def create_user(self, username, first_name, last_name):
        """Creates a user in the database"""
        self.db.create_user(username, first_name, last_name)

    def remove_favorite_sound(self, username, sound):
        """Remove a sound from the user's favorites."""
        self.db.remove_favorite_sound(username, sound)