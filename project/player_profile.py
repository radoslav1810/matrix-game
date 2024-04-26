from project.database import Database


class Player_Profile_data:
    def __init__(self):
        self.name = None
        self.score = 0
        self.database = Database()
        self.nested_dict_name_point = {}
        self.is_saved = False

    def get_info(self):
        try:
            self.database.load_user_data()
            while True:
                self.name = input("Enter your username (It must be at least 4 characters): ")
                if len(self.name) < 4:
                    print("Username must be at least 4 characters long.")
                elif self.is_username_taken(self.name):
                    print("This username is already taken. Please choose another one.")
                else:
                    break
        except ValueError as ve:
            print(f"{ve}")

    def is_username_taken(self, username):
        for profile in self.database.profile_data.values():
            if username in profile:
                return True
        return False

    def make_nested_dict(self, current_email):
        try:
            self.database.load_reg_data()

            for profile in self.database.profile_data.values():
                if self.name in profile:
                    raise ValueError("This username is already registered")

            if self.database.profile_data.get(current_email) is None:
                self.database.profile_data[current_email] = {}
            self.database.profile_data[current_email][self.name] = self.score

        except ValueError as ve:
            print(f"{ve}")

    def making_profile(self, current_email):
        try:
            self.database.load_user_data()
            self.get_info()
            # If the username doesn't meet the minimum length requirement, don't proceed
            if len(self.name) < 4:
                print("Profile not saved. Username must be at least 4 characters long.")
                return

            self.make_nested_dict(current_email)
            self.database.store_user_data()
            self.is_saved = True
            print("Your profile is done!")

        except ValueError as ve:
            print(f"{ve}")