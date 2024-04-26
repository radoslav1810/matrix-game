from project.database import Database


class Login:
    def __init__(self):
        self.email = None
        self.password = None
        self.database = Database()
        self.is_logged = False
        self.changed_password = False

    def get_input(self):
        self.email = input("Please enter your email: ")
        self.password = input("Please enter your password: ")

    def validate_email(self):
        if self.email not in self.database.registration:
            raise ValueError("We do have user with this email address")

    def validate_password(self):
        if self.database.registration.get(self.email) != self.password:
            raise ValueError("Incorrect password please try again")

    def validate_login_credentials(self):
        try:
            self.database.load_reg_data()
            self.get_input()
            self.validate_email()
            self.validate_password()
            self.is_logged = True
            print("Successfully login in your profile")

        except ValueError as e:
            print(f"Error: {e}")

    def forgotten_password(self):
        self.email = input("Enter your email: ")
        self.database.load_reg_data()
        if self.email in self.database.registration:
            self.password = input("Enter your new password: ")
            self.database.registration[self.email] = self.password
            self.changed_password = True
            self.database.store_reg_data()
            print("Password updated successfully!")
        else:
            print("Email not found. Please register first.")
