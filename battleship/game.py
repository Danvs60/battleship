from enum import Enum
import random
from time import sleep

class CoordinateState(Enum):
    WATER = "~"
    SHIP = "S"
    HIT = "O"
    MISS = "X"

class Orientation(Enum):
    VERTICAL = 1
    HORIZONTAL = 2

class Player():
    def __init__(self, name, cpu = False):
        self.name = name
        self.cpu = cpu
        self.score = 0

class BattleshipGame:

    def __init__(self):
        self.current_player = Player("Player1")
        self.waiting_player = Player("Player2", cpu = True)
        self.board_size = 10
        self.boards = self.create_boards()
        self.ships = self.initialize_ships()

        self.winning_score = 0
        for ship_size in self.ships.values():
            self.winning_score += ship_size

    def get_players(self):
        return (self.current_player, self.waiting_player)

    def display_help_message(self):
        print("""
        Welcome to Battleship!
        The objective of the game is to sink all the opponent’s ships before they sink yours.
        Here’s how the game works:

        Game Rules:
        1. Grid: The game takes place on a grid (e.g., 10x10).
        2. Ships: Ships of varying lengths are placed randomly on the grid.
        3. Turns: You guess a grid coordinate (e.g., "B5") each turn.
        4. Hits and Misses: The game will indicate whether you hit a ship or missed.
        5. Winning: You win by hitting and sinking all of your opponent’s ships.

        Legend:
        - ~ - Water: Represents open water or an unexplored cell.
        - S - Ship: A part of a ship.
        - O - Hit: A ship was hit at this location.
        - X - Miss: You fired at this location, but there was no ship.

        How to Play:
        1. Starting the Game: You will be presented with an empty grid.
        2. Enter Coordinates: Type a coordinate (e.g., "C3") to fire a shot at that location.
        3. Feedback: After firing, you will be informed if you hit or missed.
        4. Repeat Turns: Continue until all ships are sunk or the game ends.

        Good luck, and may the best tactician win!
        """)

    def create_boards(self):
        boards = {}
        for player in self.get_players():
            board = []
            for row_index in range(self.board_size):
                current_row = []

                for column_index in range(self.board_size):
                    current_row.append(CoordinateState.WATER)

                board.append(current_row)

                boards[player] = board

        return boards

    def initialize_ships(self):
        ships = {
            'Carrier': 5,
            'Battleship': 4,
            'Cruiser': 3,
            'Submarine': 3,
            'Destroyer': 2
        }

        for player in self.get_players():
            for ship_size in ships.values():
                    placement = self.get_random_placement(ship_size, player)
                    self.place_ship(placement, ship_size, player)

        return ships

    def place_ship(self, placement, ship_size, player):
        ((start_row, start_col), orientation) = placement
        print(f"{player.name} placing ship of size {ship_size} at (row:{start_row+1}, col:{chr(ord('A') + start_col)}), orientation {orientation.name}")

        if orientation == Orientation.HORIZONTAL:
            for i in range(start_col, start_col+ship_size):
                self.boards[player][start_row][i] = CoordinateState.SHIP
        elif orientation == Orientation.VERTICAL:
            for i in range(start_row, start_row+ship_size):
                self.boards[player][i][start_col] = CoordinateState.SHIP
        else:
            # illegal (diagonal)
            return None

        self.boards[player]

    def get_random_placement(self, ship_size, player):
        found = False
        placement = None

        while not found:
            orientation = random.choice((Orientation.HORIZONTAL, Orientation.VERTICAL))

            start_row = random.randint(0, self.board_size-1)
            start_col = random.randint(0, self.board_size-1)

            found = self.is_valid_placement(start_index=(start_row, start_col), ship_size=ship_size, orientation=orientation, player=player)

            if found:
                start_index = (start_row, start_col)
                placement = (start_index, orientation)

        # return valid placement
        return placement

    def is_valid_placement(self, start_index, ship_size, orientation, player):
        start_row, start_col = start_index

        if orientation == Orientation.HORIZONTAL:
            # check within board bounds
            if start_col + ship_size > self.board_size:
                # print(f"Start_index:({start_row},{start_col}), orientation: {orientation.name}, out of bounds")
                return False

            # check overlaps
            for col in range(start_col, start_col + ship_size):
                if self.boards[player][start_row][col] != CoordinateState.WATER:
                    # print(f"Start_index:({start_row},{start_col}), orientation: {orientation.name}, overlapping")
                    return False

        elif orientation == Orientation.VERTICAL:
            if start_row + ship_size > self.board_size:
                # print(f"Start_index:({start_row},{start_col}), orientation: {orientation.name}, out of bounds")
                return False

            for row in range(start_row, start_row + ship_size):
                if self.boards[player][row][start_col] != CoordinateState.WATER:
                    # print(f"Start_index:({start_row},{start_col}), orientation: {orientation.name}, overlapping")
                    return False

        return True

    def start(self):
        self.display_help_message()

        for player in self.get_players():
            self.display_board(player, hide_ships=False)

        while True:
            print(f"It's {self.current_player.name}'s turn. Please enter your guess.")

            if not self.current_player.cpu:
                self.display_board(self.current_player, hide_ships=False)
                self.display_board(self.waiting_player)

            col, row = 0, 0
            if self.current_player.cpu:
                col = random.randint(0, self.board_size - 1)
                row = random.randint(0, self.board_size - 1)
                while not self.check_valid_guess(row, col, self.waiting_player):
                    col = random.randint(0, self.board_size - 1)
                    row = random.randint(0, self.board_size - 1)
            else:
                col = self.get_col_input()
                row = self.get_row_input() - 1
                if not self.check_valid_guess(row, col, self.waiting_player):
                    print("You have already tried that, Captain! Please, pick a valid coordinate to hit.")
                    continue

            self.hit(row, col, self.waiting_player)

            if self.check_winner():
                break;

        print(f"Congratulations {self.current_player.name}, YOU WIN!")
        for player in self.get_players():
            self.display_board(player, hide_ships=False)

    def hit(self, row, col, player_to_hit):
        print("Launching attack...")
        sleep(0.5) # the suspense!

        if self.check_hit(row, col, self.waiting_player):
            print("SUCCESS!!")
            self.current_player.score += 1
            self.boards[self.waiting_player][row][col] = CoordinateState.HIT
            # player successfully hits, so turn continues
        else:
            print("MISS!!")
            self.boards[self.waiting_player][row][col] = CoordinateState.MISS
            # next turn
            self.current_player, self.waiting_player = self.waiting_player, self.current_player

    def get_row_input(self):
            error_message = "Only whole numbers between 1 and 10 are allowed"
            while True:
                row = input("Enter the row number: ")
                try:
                    val = int(row)
                    if 1 <= val and val <= 10:
                        return val # exits loop also
                    else:
                        print(error_message)
                except ValueError:
                    print(error_message)

    def get_col_input(self):
        error_message = "Only english letters (A-J) are allowed. (*Not case-sensitive)"
        while True:
            col = input("Enter the column letter: ").upper()
            if len(col) == 1 and ord('A') <= ord(col) and ord(col) <= ord('J'):
                return ord(col) - ord('A') # exits loop also
            print(error_message)

    def display_board(self, player, hide_ships=True):
        """Prints the board for the specified player"""
        print("=" * 22)
        print(f"{player.name}'s Board:")
        print("=" * 22)
        # Print column headers (A, B, C, etc.)
        print("   " + " ".join(chr(65+i) for i in range(self.board_size)))

        # Print rows with row numbers and board states
        for row_num, row in enumerate(self.boards[player]):
            formatted_row = ""
            for state in row:
                value = state.value
                if state == CoordinateState.SHIP and hide_ships:
                    value = CoordinateState.WATER.value

                formatted_row += value + " "

            # right align the number and give it 2 decimal spaces
            # this is so the boards and their coordinates are aligned
            print(f"{1+row_num:2d} {formatted_row}")

        print()

    def check_valid_guess(self, row, col, player):
        return self.boards[player][row][col] in (CoordinateState.WATER, CoordinateState.SHIP)

    def check_hit(self, row, col, player):
        return self.boards[player][row][col] == CoordinateState.SHIP

    def check_winner(self):
        if self.current_player.score == self.winning_score:
            return self.current_player
