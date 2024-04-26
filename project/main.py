import sys

from project.registered import Registration
from project.login import Login
from project.database import Database
from project.player_profile import Player_Profile_data
from project.game_menu import Menu
from project.matrix import Matrix

reg = Registration()
log = Login()
database = Database()
player = Player_Profile_data()
menu = Menu()
is_in_profile = False
is_new_profile = False
if_is_logged = False
current_email = ""
while True:
    options = ["yes", "no"]
    command = input("Do you have profile (yes/no): ").lower()
    if command in options:
        break

if command == "no":
    while True:
        reg.register_user()
        if reg.is_registered:
            current_email = reg.email
            is_new_profile = True
            is_in_profile = True
            break
else:
    while True:
        log.validate_login_credentials()
        if not log.is_logged:
            user_input = input("Forgotten password (yes/no): ").lower()
            while True:
                if user_input in ["yes", "no"]:
                    break
            if user_input == "yes":
                log.forgotten_password()
            if log.changed_password:
                print("Now you must enter your email and new password to log in your account")
        if log.is_logged:
            current_email = log.email
            break

if is_new_profile:
    player.making_profile(current_email)

while True:
    menu.choose_menu_options()
    menu.handle_selected_option(current_email)

    if menu.selected_option == "EXIT":
        print("GOODBYE")
        sys.exit()

    if menu.selected_option != "Go to main menu" and menu.selected_option != "START THE GAME":
        while True:
            go_back = input("Do you want to go to the main menu (yes/no): ").lower()
            if go_back in ["yes", "no"]:
                break
            else:
                print("You must choose between yes/no")

        if go_back == "no":
            while True:
                user_input = input("Do you want to exit the game (yes/no): ").lower()
                if user_input in ["yes", "no"]:
                    break
                else:
                    print("You must choose between yes/no")
            if user_input == "yes":
                print("GOODBYE")
                sys.exit()
            else:
                print("Okay, you will be redirected to the main menu")
                continue

    if menu.selected_option == "START THE GAME":
        Matrix_game = Matrix()
        Matrix_game.place_object_on_invisible_matrix()
        matrix_for_player = Matrix_game.visible_matrix
        matrix = Matrix_game.invisible_matrix
        player_row, player_col = Matrix_game.check_player_position()
        matrix_for_player[player_row][player_col] = "X"

        while True:
            matrix_for_player[player_row][player_col] = "X"
            matrix[player_row][player_col] = "X"
            for row in matrix_for_player:
                print("|".join(row))

            matrix_for_player[player_row][player_col] = "*_*"
            matrix[player_row][player_col] = "*_*"

            direction = Matrix_game.get_player_movement().upper()
            movement_result = Matrix_game.movement(direction)

            if movement_result:
                player_row, player_col = movement_result

            result = Matrix_game.check_game_result()
            if result:
                print(result)
                if Matrix_game.game_over:
                    break

        print(Matrix_game.check_for_best_score(current_email))
