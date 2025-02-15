import unittest
from battleship.game import BattleshipGame, CoordinateState, Orientation

class TestBattleshipGame(unittest.TestCase):

    def setUp(self):
        self.game = BattleshipGame()

    def test_initialization(self):
        self.assertEqual(self.game.board_size, 10)
        self.assertEqual(len(self.game.boards), 2)
        self.assertEqual(sum(self.game.ships.values()), self.game.winning_score)

    def test_create_boards(self):
        boards = self.game.create_boards()
        for player in self.game.get_players():
            self.assertEqual(len(boards[player]), 10)
            for row in boards[player]:
                self.assertEqual(len(row), 10)
                for cell in row:
                    self.assertEqual(cell, CoordinateState.WATER)

    def test_initialize_ships(self):
        ships = self.game.initialize_ships()
        self.assertEqual(ships, {
            'Carrier': 5,
            'Battleship': 4,
            'Cruiser': 3,
            'Submarine': 3,
            'Destroyer': 2
        })

    def test_is_valid_placement(self):
        player = self.game.current_player
        self.assertTrue(self.game.is_valid_placement(start_index=(0, 0), ship_size=3, orientation=Orientation.HORIZONTAL, player=player))
        self.assertFalse(self.game.is_valid_placement(start_index=(9, 9), ship_size=3, orientation=Orientation.HORIZONTAL, player=player))

    def test_place_ship(self):
        player = self.game.current_player
        self.game.place_ship(((0, 0), Orientation.HORIZONTAL), 3, player)
        self.assertEqual(self.game.boards[player][0][0], CoordinateState.SHIP)
        self.assertEqual(self.game.boards[player][0][1], CoordinateState.SHIP)
        self.assertEqual(self.game.boards[player][0][2], CoordinateState.SHIP)

    def test_check_valid_guess(self):
        player = self.game.current_player
        self.assertTrue(self.game.check_valid_guess(0, 0, player))
        self.game.boards[player][0][0] = CoordinateState.HIT
        self.assertFalse(self.game.check_valid_guess(0, 0, player))

    def test_check_hit(self):
        player = self.game.current_player
        self.game.boards[player][0][0] = CoordinateState.SHIP
        self.assertTrue(self.game.check_hit(0, 0, player))
        self.game.boards[player][0][0] = CoordinateState.WATER
        self.assertFalse(self.game.check_hit(0, 0, player))

    def test_check_winner(self):
        self.game.current_player.score = self.game.winning_score
        self.assertEqual(self.game.check_winner(), self.game.current_player)

if __name__ == '__main__':
    unittest.main()
