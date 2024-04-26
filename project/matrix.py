import random
from project.player_profile import Player_Profile_data
from project.database import Database


class Matrix:
    Movement = ["W", "S", "D", "A"]

    def __init__(self):
        self.row = 5
        self.col = 5
        self.player_row = 0
        self.player_col = 0
        self.visible_matrix = self.make_matrix()
        self.invisible_matrix = self.place_object_on_invisible_matrix()
        self.player = Player_Profile_data()
        self.game_points = []
        self.game_over = False
        self.new_game = False
        self.database = Database()
        self.new_score = 0

    def make_matrix(self):
        matrix = [["*_*" for col in range(self.col)] for row in range(self.row)]
        return matrix

    def print_matrix(self):
        matrix = self.make_matrix()
        for row in matrix:
            return " +_+ ".join(row)

    def place_object_on_invisible_matrix(self):
        invisible_matrix = self.make_matrix()
        points_count = 15
        while points_count > 0:
            row = random.randint(0, self.row - 1)
            col = random.randint(0, self.col - 1)
            if invisible_matrix[row][col] == "*_*":
                invisible_matrix[row][col] = str(random.randint(1, 500))
                points_count -= 1
        while True:
            row = random.randint(0, self.row - 1)
            col = random.randint(0, self.col - 1)
            if invisible_matrix[row][col] == "*_*":
                invisible_matrix[row][col] = "Bomb"
                break

        while True:
            row = random.randint(0, self.row - 1)
            col = random.randint(0, self.col - 1)
            if invisible_matrix[row][col] == "*_*":
                invisible_matrix[row][col] = "X"
                break
        return invisible_matrix

    def check_player_position(self):
        for row in range(len(self.invisible_matrix)):
            for col in range(len(self.invisible_matrix[row])):
                if self.invisible_matrix[row][col] == "X":
                    self.player_row = row
                    self.player_col = col
                    return self.player_row, self.player_col

    def get_player_movement(self):
        player_input = input("Choose Your Direction: ").upper()
        if player_input not in self.Movement:
            return ""
        return player_input

    def movement(self, direction):

        if direction == "W" and self.player_row > 0:
            self.player_row -= 1
        elif direction == "S" and self.player_row < self.row - 1:
            self.player_row += 1
        elif direction == "A" and self.player_col > 0:
            self.player_col -= 1
        elif direction == "D" and self.player_col < self.col - 1:
            self.player_col += 1
        else:
            print("You cannot go out of the map!")
            return None

        return self.player_row, self.player_col

    def check_game_result(self):
        current_row = self.player_row
        current_col = self.player_col
        cell_value = self.invisible_matrix[current_row][current_col]

        if cell_value == "Bomb":
            self.game_over = True
            self.new_score = sum(self.game_points)
            return "Oops, you lose the game!"
        elif cell_value.isdigit():
            point_value = int(cell_value)
            self.game_points.append(point_value)
            if len(self.game_points) == 15:
                self.new_score = sum(self.game_points)
                self.game_over = True
                return f"Congratulations, you collected all points without stepping on the bomb!\nYour score: {self.new_score}"
            else:
                return f"You collected {point_value} points!"

    def check_for_best_score(self, current_email):
        self.database.load_user_data()
        data = self.database.profile_data[current_email]
        for username, value in data.items():
            if self.new_score > value:
                data[username] = self.new_score
                self.database.store_user_data()
                return f"Congratulations you made you personal new high score of {self.new_score}"
            return f"You made score of {self.new_score}"
