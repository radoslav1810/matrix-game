from project.database import Database
from project.player_profile import Player_Profile_data
from project.login import Login
from project.registered import Registration


class Menu:
    def __init__(self):
        self.menu_options = ["START THE GAME", "OPTIONS(HOW TO PLAY)", "PROFILE", "BEST SCORES", "MORE ABOUT US",
                             "EXIT"]
        self.user_input = ""
        self.database = Database()
        self.login = Login()
        self.player = Player_Profile_data()
        self.registration = Registration()
        self.selected_option = ""

    def get_info(self):
        self.user_input = input("Enter your choice: ")
        if not self.user_input.isdigit():
            raise ValueError("Please enter a valid number.")

    def check_for_correct_command(self, lst):
        try:
            user_input = int(self.user_input)
            if 0 <= user_input < len(lst):
                self.selected_option = lst[user_input]
                return f"You selected: {self.selected_option}"

            return "Invalid option!"
        except ValueError:
            print("Invalid input! Please enter a number.")

    @staticmethod
    def enumerate_list(lst):
        print("Select an option:")
        for index, value in enumerate(lst):
            print(f"Press {index} for {value}")

    def choose_menu_options(self):
        self.enumerate_list(self.menu_options)
        self.get_info()
        self.check_for_correct_command(self.menu_options)

    def options(self):
        rules_and_options = ["How to play", "Options", "Go to main menu"]
        try:
            self.enumerate_list(rules_and_options)
            self.get_info()
            self.check_for_correct_command(rules_and_options)
        except ValueError as ve:
            print(f"{ve}")

    @staticmethod
    def how_to_play():
        return """When you start the game you will see many stupid faces on the map, but that should not reassure 
        you. You can walk on the map but be careful, because under the map you have many points to collect, 
        but also a bomb that can kill you. You must trust your instinct and hope for good luck."""

    @staticmethod
    def view_how_to_move():
        return "You can move with 'W' for up, 'S' for down, 'A' for left and 'D' for right"

    def profile(self):
        profile_options = ["Change my password", "Change my username", "See Profile info", "Go to main menu"]
        try:
            self.enumerate_list(profile_options)
            self.get_info()
            return self.check_for_correct_command(profile_options)
        except ValueError as ve:
            print(f"{ve}")

    def see_my_profile(self, current_email):
        self.database.load_user_data()
        data = self.database.profile_data.get(current_email)
        if data:
            for username, best_score in data.items():
                return f"Username: {username}, Best score: {best_score}"
        else:
            print(f"Profile not found for email: {current_email}")

    @staticmethod
    def validate_password(password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")

    def change_my_password(self, current_email):
        try:
            self.database.load_reg_data()
            if current_email in self.database.registration:
                new_password = input("Enter your new password: ")
                self.validate_password(new_password)
                self.database.registration[current_email] = new_password
                self.database.store_reg_data()
                return "Password updated successfully!"
        except ValueError as ve:
            print(f"{ve}")

    def change_my_username(self, current_email):
        try:
            self.database.load_user_data()
            data = self.database.profile_data.get(current_email)
            for username, value in data.items():
                new_username = input("Enter your new username: ")
                if len(new_username) < 4:
                    raise ValueError("Username must be at least 4 characters long.")
                new_data = {new_username: data.pop(username)}  # Remove the existing entry and create a new one
                self.database.profile_data[current_email] = new_data
                self.database.store_user_data()
                return "You change your username successfully"
        except ValueError as ve:
            print(f"{ve}")

    @staticmethod
    def information_about_me():
        return "This is a small project for fun. I made it for educational purposes and to learn some new techniques."

    def view_best_score(self):
        self.database.load_user_data()
        data = self.database.profile_data

        max_numb = 0
        best_username = ""
        if data:
            for email, value in data.items():
                for username, score in value.items():
                    if score > max_numb:
                        max_numb = score
                        best_username = username
            return f"Username with the best score: {best_username}, Score: {max_numb}"
        else:
            return "No player profiles found."

    def go_to_main_menu(self):
        self.selected_option = ""

    def handle_selected_option(self, current_email):
        if self.selected_option == "":
            self.choose_menu_options()
        elif self.selected_option == "OPTIONS(HOW TO PLAY)":
            self.options()
            if self.selected_option == "How to play":
                print(self.how_to_play())
            elif self.selected_option == "Options":
                print(self.view_how_to_move())
        elif self.selected_option == "PROFILE":
            print(self.profile())
            if self.selected_option == "Change my password":
                print(self.change_my_password(current_email))
            elif self.selected_option == "Change my username":
                print(self.change_my_username(current_email))
            elif self.selected_option == "See Profile info":
                print(self.see_my_profile(current_email))
        elif self.selected_option == "BEST SCORES":
            print(self.view_best_score())
        elif self.selected_option == "MORE ABOUT US":
            print(self.information_about_me())
