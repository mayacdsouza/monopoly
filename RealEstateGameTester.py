import unittest
from RealEstateGame import RealEstateGame, Player, Space


class TestRealEstateGame(unittest.TestCase):
    """
    Unit tests for RealEstateGame
    """
    def setUp(self):
        pass

    def test_1(self):
        """Tests the init, get, and set methods for Space class"""
        space = Space("Cat", 2, 789)
        self.assertEqual(space.get_name(), 'Cat')
        self.assertEqual(space.get_index(), 2)
        self.assertEqual(space.get_rent(), 789)
        self.assertIs(space.get_is_owned(), False)
        space.set_is_owned()
        self.assertIs(space.get_is_owned(), True)
        space.set_rent(37)
        self.assertEqual(space.get_rent(), 37)

    def test_2(self):
        """Tests the init, get, and set methods for the Player class"""
        player1 = Player("Sarah", 900)
        self.assertEqual(player1.get_name(), 'Sarah')
        self.assertEqual(player1.get_account_balance(), 900)
        self.assertEqual(player1.get_owned_spaces(), [])
        self.assertEqual(player1.get_position(), 0)
        player1.set_account_balance(97)
        self.assertEqual(player1.get_account_balance(), 997)
        player1.set_position(5)
        self.assertEqual(player1.get_position(), 5)
        space1 = Space("Cat", 2, 789)
        space2 = Space("Dog", 5, 781)
        player1.add_owned_space(space1)
        player1.add_owned_space(space2)
        self.assertIs(space1.get_is_owned(), True)
        self.assertIs(space2.get_is_owned(), True)
        self.assertEqual(player1.get_owned_spaces(), [space1, space2])
        player1.remove_owned_space(2)
        self.assertIs(space1.get_is_owned(), False)
        self.assertIs(space2.get_is_owned(), True)
        self.assertEqual(player1.get_owned_spaces(), [space2])

    def test_3(self):
        """Tests the init/create/get methods for the RealEstateGame class"""
        game = RealEstateGame()

        rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350,
                 350, 350]
        game.create_spaces(50, rents)

        game.create_player("Player 1", 1000)
        game.create_player("Player 2", 1100)
        game.create_player("Player 3", 1200)
        self.assertEqual(1000, game.get_player_account_balance("Player 1"))
        space = game.get_space(4)
        self.assertEqual(4, space.get_index())
        self.assertEqual(75, space.get_rent())
        self.assertEqual(0, game.get_player_current_position("Player 2"))

    def test_4(self):
        """Tests game over"""
        game = RealEstateGame()

        rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350,
                 350, 350]
        game.create_spaces(50, rents)

        game.create_player("Player 1", 1000)
        game.create_player("Player 2", 1000)
        game.create_player("Player 3", 1000)
        string1 = game.check_game_over()

        game = RealEstateGame()

        rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350,
                 350, 350]
        game.create_spaces(50, rents)

        game.create_player("Player 1", 0)
        game.create_player("Player 2", 1000)
        game.create_player("Player 3", 0)
        string2 = game.check_game_over()

        self.assertEqual("", string1)
        self.assertEqual("Player 2", string2)

    def test_5(self):
        """Checks buy space"""

        #case where space is owned, done

        #case where space is go
        game = RealEstateGame()

        rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350,
                 350, 350]
        game.create_spaces(50, rents)

        game.create_player("Player 1", 1000)
        game.create_player("Player 2", 1000)
        game.create_player("Player 3", 1000)
        self.assertIs(False, game.buy_space("Player 1"))

        #case where player can afford space, done

        #case where player cannot afford space, done

    def test_6(self):
        """Tests move space"""
        #checks does nothing if account balance is 0, done
        #checks player is moved proper number of spaces, done
        #checks player gets money if they pass go, done
        #checks player doesn't get money if they don't pass go, done
        #checks player doesn't pay rent if they land on go or space unowned or they own space, done
        #checks player account balance and owner account balance if they can afford rent
        #checks player account balance and owned spaced and owner account balance if they can't afford rent