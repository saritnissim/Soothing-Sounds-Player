from player import SoundPlayer


class RelaxingSoundApp:
    def __init__(self):
        self.sound_player = SoundPlayer()
        self.username = input("Enter username: ")
        user = self.sound_player.get_user(self.username)
        if user:
            self.first_name = user[1]
        else: 
            print("Welcome new user!")  
            self.first_name = input("Please enter your first name ")
            last_name = input("Please enter your last name ")   
            self.sound_player.create_user(self.username, self.first_name, last_name)

    def main_menu(self):
        """Display the main menu and handle user choices."""
        
        print(f"Welcome to the Relaxing Sound Player {self.first_name}!")
        
        while True:
            print("\nMenu:")
            print("1. Choose a sound")
            print("2. Save favorite sound")
            print("3. Play favorite sound")
            print("4. Exit")

            choice = input("Choose an option: ")
            if choice == "1":
                self.get_sound()
            elif choice == "2":
                self.save_favorite()
            elif choice == "3":
                self.play_favorite()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    
    def get_sound(self):
        """Get user selection for sound"""
        while True:  # Keep prompting until valid input is given
            try:
                # Display available sounds
                print("Available sounds:")
                for num, category in self.sound_player.sound_list.items():
                    print(f"{num}. {category}")
                
                # Get user input
                user_input = input("Please enter the number of the sound you wish to listen to: ")
                
                # Validate input
                index = int(user_input)
                if index not in self.sound_player.sound_list:
                    print("Invalid selection. Please choose a valid number.")
                    continue
                
                # Play the selected sound
                sound = self.sound_player.sound_list[index]
                self.sound_player.play_sound(sound)
                break  # Exit the loop after successful playback

            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break  # Exit the loop on unexpected errors


    def save_favorite(self):
        """Save a favorite sound type."""
        while True:
            favorite_sound = input("Enter your favorite sound condition: ").lower()
            if favorite_sound not in self.sound_player.sounds_config:
                    print("Invalid sound type. Please choose from the available sounds.")
                    continue
            self.sound_player.save_favorite_sound(self.username, favorite_sound)
            break

    def play_favorite(self):
        """Play the user's favorite sound."""
        favorite_sound = self.sound_player.get_favorite_sound(self.username)
        if favorite_sound:
            self.sound_player.play_sound(favorite_sound)
        else:
            print("No favorite sound saved yet.")


if __name__ == "__main__":
    app = RelaxingSoundApp()
    app.main_menu()
