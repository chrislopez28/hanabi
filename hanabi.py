"""Module for Hanabi Card Game."""

import random

class Card:
    """Class for a Hanabi playing card."""
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val
        self.hints = []

    def __repr__(self):
        return "{} {}".format(self.suit, self.value)

    def show(self):
        """Prints card value and suit."""
        print("{} {}. Hints: {}".format(self.suit, self.value, self.hints))

    def show_hints(self):
        """Print hints."""
        print("???"" ?. Hints: {}".format(self.hints))

    def next(self):
        """Print out the next card in the suit if there is one."""
        if self.value < 5:
            print("The next card is the {} {}.".format(self.suit, self.value + 1))
        else:
            print("This is the last {} card.".format(self.suit))

    def add_hint(self, hint):
        """Adds a hint to card."""
        self.hints.append(hint)

class Deck:
    """Class for the playing card deck."""
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """Generates a complete deck of Hanabi cards."""
        for suit in ["Blue", "Green", "Red", "White", "Yellow"]:
            for val in range(1, 6):
                self.cards.append(Card(suit, val))
                if val != 5:
                    self.cards.append(Card(suit, val))
                if val == 1:
                    self.cards.append(Card(suit, val))

    def show(self):
        """Prints cards in the deck object."""
        for card in self.cards:
            card.show()

    def shuffle(self):
        """Randomizes the order of cards in the deck."""
        for i in range(len(self.cards) - 1, 0, -1):
            selected = random.randint(0, i)
            self.cards[i], self.cards[selected] = self.cards[selected], self.cards[i]

    def draw_card(self):
        """Pops top card from the deck."""
        if self.cards:
            return self.cards.pop()

    def card_count(self):
        """Return number of cards remaining in deck"""
        return len(self.cards)

class Board:
    """Class for the game board."""
    def __init__(self):
        self.blue = []
        self.green = []
        self.red = []
        self.white = []
        self.yellow = []
        self.discard = []
        self.chances = 3
        self.hints = 8

    def show_board(self):
        """Print board attributes."""
        print("Blue:", self.blue)
        print("Green:", self.green)
        print("Red:", self.red)
        print("White:", self.white)
        print("Yellow:", self.yellow)
        print("Chances: {} / Hints Remaining: {}".format(self.chances, self.hints))
        print("Discard Pile:", self.discard)

    def take_discard(self, card):
        """Add card to discard pile."""
        self.discard.append(card)
        self.hints += 1

    def check_play(self, card):
        """Return true if card can be played on the board."""
        if card.suit == "Blue":
            suit = self.blue
        if card.suit == "Green":
            suit = self.green
        if card.suit == "Red":
            suit = self.red
        if card.suit == "White":
            suit = self.white
        if card.suit == "Yellow":
            suit = self.yellow
        return self.check_next(suit, card.value)

    def add(self, card):
        """Add card to the board."""
        if self.check_play(card):
            if card.suit == "Blue":
                self.blue.append(card)
            if card.suit == "Green":
                self.green.append(card)
            if card.suit == "Red":
                self.red.append(card)
            if card.suit == "White":
                self.white.append(card)
            if card.suit == "Yellow":
                self.yellow.append(card)
        else:
            self.chances -= 1
            print("\nKaboom! You set off the wrong firework ({})".format(card))
            print("\nYou now have {} chances remaining".format(self.chances))

    def check_complete(self):
        """Returns true if all fireworks are complete (one through five)."""
        if (len(self.blue) == 5) and (len(self.green) == 5) and (len(self.red) == 5) and \
            (len(self.white) == 5) and (len(self.yellow) == 5):
            return True
        return False

    def check_next(self, lst, val):
        """Check if card is the next card for the suit"""
        if not lst:
            return val == 1
        if val == lst[-1].value + 1:
            return (val <= 5) & (val > 1)
        return False

class Player:
    """Class for a player."""
    def __init__(self, name):
        self.name = name
        self.position = int()
        self.hand = []

    def draw(self, deck):
        """Draw a card from the deck into a player's hand."""
        self.hand.append(deck.draw_card())
        return self

    def show_hand(self):
        """Print cards in a player's hand."""
        for card in self.hand:
            card.show()

    def show_concealed_hand(self):
        """Print hints in a player's hand."""
        for card in self.hand:
            card.show_hints()

    def card_count(self):
        """Return the number of cards in a player's hand."""
        return len(self.hand)

    def give_hint(self, board, receiver, hint):
        """Give hint to another player."""
        if board.hints < 1:
            return None
        if hint in ["Blue", "Green", "Red", "White", "Yellow"]:
            for card in receiver.hand:
                if card.suit == hint:
                    card.hints.append("{}".format(hint))
                else:
                    card.hints.append("Not {}".format(hint))
        if hint in ["1", "2", "3", "4", "5"]:
            for card in receiver.hand:
                if card.value == int(hint):
                    card.hints.append("{}".format(hint))
                else:
                    card.hints.append("Not {}".format(hint))
        board.hints -= 1
        return board

    def play_card(self, board, deck, card_num):
        """Play a card to the board."""
        board.add(self.hand.pop(card_num))
        self.hand.append(deck.draw_card())

    def discard_card(self, board, deck, card_num):
        """Discard a card to the discard pile."""
        board.take_discard(self.hand.pop(card_num))
        self.hand.append(deck.draw_card())

def game_view(players, current_player):
    """Prints out visible cards to current player"""
    for player in players:
        print(f"\n**Player {player.position} --- {player.name}")
        if player == current_player:
            player.show_concealed_hand()
        else:
            player.show_hand()

class Game:
    """Class for a Hanabi game."""

    def __init__(self, name=None):
        self.name = name
        self.players = [Player("P1"), Player("P2"), Player("P3")]
        self.deck = Deck()
        self.board = Board()

    def start_game(self):
        """Start a game of Hanabi."""
        print("***** HANABI *****\n")
        print("A 3 player game will be started. You will have to act for each player.\n")
        input(">> Press Enter to continue...\n")
        self.deal_game()
        print("Deck shuffled. Cards dealt.\n")
        input(">> Press Enter to continue...\n")
        self.game_loop()

    def deal_game(self):
        """Deal game to players."""
        self.deck.shuffle()
        for player in self.players:
            for i in range(5):
                player.draw(self.deck)

    def game_loop(self):
        """Loop through players' turns."""
        turn = 1
        while (self.board.chances != 0) or (not self.board.check_complete()):
            current_player = self.players[turn % 3 - 1].name
            print(f"\n********** Turn {turn}: {current_player} **********")
            self.board.show_board()
            print("Cards Remaining:", self.deck.card_count())
            self.game_view()

            deciding = True
            while deciding:
                x = input(f"\n{current_player} to act.\n>> Type one of the following commands and press Enter: 'p' - play a card, 'd' - discard a card, 'h' - give a hint.\n")
                if x == "p":
                    while True:
                        n = input("\n>> Choose a card to play (1-5).\n")
                        if n not in ("1", "2", "3", "4", "5"):
                            print("Invalid card number")
                        else:
                            n = str(int(n) + 1)
                            break
                    self.players[turn % 3 - 1].play_card(self.board, self.deck, int(n))
                    deciding = False
                elif x == "d":
                    while True:
                        n = input("\n>> Choose a card to discard (1-5).\n")
                        if n not in ("1", "2", "3", "4", "5"):
                            print("Invalid card number")
                        else:
                            str(int(n) + 1)
                            break
                    self.players[turn % 3 - 1].discard_card(self.board, self.deck, int(n))
                    deciding = False
                elif x == "h":
                    while True:
                        current_num = turn % 3
                        p = input("\n>> Choose a player to give a hint to (1-3) and press Enter. (Note: you cannot give a hint to yourself)\n")
                        if (p not in ("1", "2", "3") or (int(p) == current_num)):
                            print("invalid player")
                        else:
                            break
                    while True:
                        h = input("\n>> Choose a suit or a value (i.e. 1-5 or Blue, Green, Red, White, Yellow)\n")
                        if h not in ("1", "2", "3", "4", "5", "Blue", "Green", "Red", "White", "Yellow"):
                            print("Invalid hint")
                        else:
                            break
                    self.players[turn % 3 - 1].give_hint(self.board, self.players[int(p) - 1], h)
                    deciding = False
            turn = turn + 1

        if self.board.check_complete():
            print("******************************************")
            print("******************************************")
            print("Yay! You Win!!!!")

        if self.board.chances == 0:
            print("******************************************")
            print("******************************************")
            print(" :( ")

        input("\n\nPress any key to exit")

    def game_view(self):
        """Prints out visible cards to current player"""
        for num, player in enumerate(self.players):
            print(f"\n*** Player {num + 1} ({player.name}) Hand: ***")
            if num == 0:
                player.show_concealed_hand()
            else:
                player.show_hand()

class View:
    """Class for a view of the game."""
    pass

game = Game("game")
game.start_game()