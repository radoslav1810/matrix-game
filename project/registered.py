import re
from project.database import Database


class Registration:
    def __init__(self):
        self.email = None
        self.password = None
        self.database = Database()
        self.database.load_reg_data()
        self.is_registered = False

    def get_info(self):
        self.email = input("Please enter your email address: ")
        self.password = input("Please enter your password (it must be at least 6 characters long): ")

    def validate_email(self):
        pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
        match = re.match(pattern, self.email)
        if not match:
            raise ValueError("Invalid email format")

        if self.email in self.database.registration:
            raise ValueError("This email is already registered")

    def validate_password(self):
        if len(self.password) < 6:
            raise ValueError("Password must be at least 6 characters long")

    def register_user(self):
        try:
            self.get_info()
            self.validate_email()
            self.validate_password()
            self.database.registration[self.email] = self.password
            self.database.store_reg_data()
            print("User is successfully saved")
            self.is_registered = True
        except ValueError as e:
            print(f"Error: {e}")
