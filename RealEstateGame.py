# Author: Maya D'Souza
# GitHub Username: mayacdsouza
# Date: 5/28/2022
# Description: Simplified version of Monopoly called Real Estate Game.


class RealEstateGame:
    """
    RealEstateGame stores data on the current status of the game. It's responsibilities are to create the spaces
    in the game, add players to the game, return the account balance and position of players, move players, allow
    players to purchase spaces, and check if the game is over.

    RealEstateGame communicates with the Player class to add players to the game, check and update their account
    balance/position/owned spaces, and check if the game is over based on player account balances. It also
    communicates with the Space class to set and check rent of each space and to check if a space is owned when
    a player wants to buy it.
    """

    def __init__(self):
        """Initializes game with a list of Space objects with rent = 0, a value of money received
        for passing or landing on go, and an empty list to store Player objects in the game."""
        space_names = ["GO"]
        for number in range(1, 25):
            space_names.append(str(number))
        self._spaces = []
        for index in range(0, 25):
            self._spaces.append(Space(space_names[index], index, 0))
        self._players = []
        self._go_money = 0

    def create_spaces(self, go_money, rent_array):
        """
        Updates rent of 25 Space objects stored in self._spaces. The initial space is named GO and has rent = 0.
        The following 24 Spaces have unique rent values initialized by rent_array. Every space excluding GO can be
        purchased for 5x rent.
        """
        self._go_money = go_money
        for index in range(1, 25):
            self._spaces[index].set_rent(rent_array[index-1])

    def create_player(self, name, account_balance):
        """
        Creates a Player object with name and account_balance (value of input parameters).
        """
        self._players.append(Player(name, account_balance))

    def get_player_account_balance(self, name):
        """
        Returns account balance of player with the given name.
        """
        for player in self._players:
            if player.get_name() == name:
                return player.get_account_balance()

    def get_space(self, space_index):
        """Returns space with given index"""
        return self._spaces[space_index]

    def get_player_current_position(self, name):
        """
        Returns current position of player with the given name as an integer. GO
        is position zero, and the following spaces are numbered 1 to 24.
        """
        for player in self._players:
            if player.get_name() == name:
                return player.get_position()

    def buy_space(self, name):
        """
        Checks to make sure player has a high enough account balance to purchase
        the space and that the space is unowned. If player can purchase space,
        the purchase price of the space is deducted from the player's account.
        They are then set as owner of the space. The method will return True
         or False to indicate if player could purchase the space.
        """
        for player in self._players:
            if player.get_name() == name:  # finds player using name
                if player.get_position() == 0:  # player cannot buy GO
                    return False
                space = self._spaces[player.get_position()]
                rent = space.get_rent()
                if player.get_account_balance() < 5*rent or space.get_is_owned():  # space owned, player can't afford it
                    return False
                player.set_account_balance(-5*rent)
                player.add_owned_space(space)
                return True

    def move_player(self, name, number):
        """
        If player has account balance of 0, method returns immediately.

        Otherwise, player will be moved number spaces forward (number is a value from 1-6).
        Player will receive GO amount of money if they land on or pass it.

        If necessary, player will pay rent for new space occupied (player doesn't play rent
        if they are on GO, nobody owns the space, or they own the space). They will pay their
        account balance or the rent for the space, whichever is less. This money will be deducted
        from their account and deposited into the game space owner's account.

        If the player's account balance becomes 0, they have lost and no longer own any spaces.
        """
        # finds current player by checking player names, stores as current_player
        current_player = None
        for player in self._players:
            if player.get_name() == name:
                current_player = player

        # doesn't allow player to move if they've already lost
        if current_player.get_account_balance() == 0:
            return

        # updates player position, gives them money if they passed or landed on go
        position_0 = current_player.get_position()
        current_player.set_position(number)
        position_1 = current_player.get_position()
        if position_0 > position_1:
            current_player.set_account_balance(self._go_money)

        # ends player turn if they landed on go
        if position_1 == 0:
            return

        # checks if player needs to pay rent
        space_index = current_player.get_position()
        current_space = self._spaces[space_index]

        if current_space.get_is_owned():
            # player doesn't pay if they own space
            for space in current_player.get_owned_spaces():
                if space == current_space:
                    return

            # player pays if someone else owns space
            for potential_space_owner in self._players:
                for space in potential_space_owner.get_owned_spaces():
                    if space.get_index() == space_index:
                        if current_player.get_account_balance() > current_space.get_rent():  # can pay full rent
                            current_player.set_account_balance(-1*current_space.get_rent())
                            potential_space_owner.set_account_balance(current_space.get_rent())
                            return
                        else:  # can't pay full rent, so pay remaining money and lose game
                            account_balance = current_player.get_account_balance()
                            potential_space_owner.set_account_balance(account_balance)
                            current_player.set_account_balance(-1 * account_balance)
                            for owned_space in current_player.get_owned_spaces():
                                owned_space.set_is_owned()
                                current_player.remove_owned_space(owned_space)
                            return

    def check_game_over(self):
        """
        Game over if only one player has a nonzero account balance.
        Method returns winner's name if game is over and an empty string
        if not.
        """
        players_in_game = 0
        result = ""
        for player in self._players:
            if player.get_account_balance() > 0:
                players_in_game += 1
                result = player.get_name()
        if players_in_game == 1:
            return result
        else:
            return ""


class Player:
    """
    Player with a name, account balance, list of spaces they own, and position. This class will be used by
    the RealEstateGame class. It communicates with the Space class to set the is_owned value of a space to
    True or False when a player buys a space or loses the game. The user can find out the player's
    name/account_balance/owned_spaces/position with get methods, change their account_balance/position with
    set methods, and update their owned_spaces with add/remove methods.
    """

    def __init__(self, name, account_balance):
        """
        Initializes name, account balance, owned spaces, and position. self._owned_spaces
        starts as an empty list because player begins with no spaces and self._position starts as
        0 because the player begins at go.
        """
        self._name = name
        self._account_balance = account_balance
        self._owned_spaces = []
        self._position = 0

    def get_name(self):
        """Returns player name"""
        return self._name

    def get_account_balance(self):
        """Returns account balance"""
        return self._account_balance

    def get_owned_spaces(self):
        """Returns spaces owned by player"""
        return self._owned_spaces

    def get_position(self):
        """Return player position."""
        return self._position

    def set_account_balance(self, new_balance):
        """Adds new_balance to account balance"""
        self._account_balance += new_balance

    def add_owned_space(self, space):
        """Adds Space object to player's list of owned spaces and changes
        is_owned parameter of Space object to True."""
        self._owned_spaces.append(space)
        space.set_is_owned()

    def remove_owned_space(self, space_index):
        """Removes space object from player's list of owned space and changes
        is_owned parameter of Space object to False."""
        for space in self._owned_spaces:
            if space.get_index() == space_index:
                space.set_is_owned()
                self._owned_spaces.remove(space)

    def set_position(self, dice_roll):
        """Updates position to reflect player moving dice_roll spaces"""
        self._position = (self._position + dice_roll) % 25


class Space:
    """
    Space with a name, rent value, index, and is_owned value that tracks if someone owns a space.
    It allows user to initialize a Space object. This class will be used by the RealEstateGame and Player
    classes. Space has get methods for the name, index, rent, and is_owned parameters. It also has set methods
    to change the is_owned parameter between True and False and to set the rent of the space.
    """
    def __init__(self, name, index, rent):
        """Initializes name, index, and rent of space."""
        self._name = name
        self._index = index
        self._rent = rent
        self._is_owned = False

    def get_index(self):
        """Returns index of space"""
        return self._index

    def get_name(self):
        """Returns name of space"""
        return self._name

    def get_rent(self):
        """Returns rent cost of space"""
        return self._rent

    def get_is_owned(self):
        """Returns True or False based on if space is owned."""
        return self._is_owned

    def set_is_owned(self):
        """Flips is_owned value (from True to False or False to True)."""
        self._is_owned = not self._is_owned

    def set_rent(self, rent):
        """Sets rent cost of space"""
        self._rent = rent
