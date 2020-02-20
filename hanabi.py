"""Module for Hanabi Card Game"""

import random

class Card:
    """Class for a hanabi playing card"""
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val

    def show(self):
        """Prints card value and suit"""
        print("{} of {}".format(self.value, self.suit))

class Deck:
    """Class for the playing card deck"""
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        "Generates a complete deck of Hanabi cards"
        for suit in ["Blue", "Green", "Red", "White", "Yellow"]:
            for val in range(1, 6):
                self.cards.append(Card(suit, val))
                if val != 5:
                    self.cards.append(Card(suit, val))
                if val == 1:
                    self.cards.append(Card(suit, val))

    def show(self):
        "Prints cards in the deck object"
        for card in self.cards:
            card.show()

    def shuffle(self):
        "Randomizes the order of cards in the deck"
        for i in range(len(self.cards) - 1, 0, -1):
            selected = random.randint(0, i)
            self.cards[i], self.cards[selected] = self.cards[selected], self.cards[i]

    def draw_card(self):
        "Pops top card from the deck"
        return self.cards.pop()

class Board:
    "Class for the game board"
    def __init__(self):
        self.blue = []
        self.green = []
        self.red = []
        self.white = []
        self.yellow = []
        self.chances = 3

    def add(self, card):
        "Add card to the board"
        if card.suit == "Blue":
            return self.blue
        if card.suit == "Green":
            return self.green
        if card.suit == "Red":
            return self.red
        if card.suit == "White":
            return self.white
        if card.suit == "Yellow":
            return self.yellow
        return None

    def check_play(self, card):
        "Return true if card can be played on the board"
        pass

    def check_next(self, card):
        pass
### Play card to Board
# if val >= 2 & val <= 5:
#   if self.blue[-1] == val - 1:
#       self.blue.append(val)
#   else:
#       self.chances = self.chances - 1
# if val == 1:
#   if not self.blue:
#       self.blue.append(val)
#   else:
#       self.chances = self.chances - 1

class Player:
    "Class for a player"
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw(self, deck):
        "Draw a card from the deck into a player's hand"
        self.hand.append(deck.draw_card())
        return self

    def show_hand(self):
        "Print cards in a player's hand"
        for card in self.hand:
            card.show()

DECK = Deck()
DECK.shuffle()
#deck.show()

print("Initializing Player: ")
P1 = Player("Chris")

print("Drawing Hand: ")
P1.draw(DECK)
P1.draw(DECK)
P1.draw(DECK)
P1.draw(DECK)
P1.draw(DECK)

P1.show_hand()
