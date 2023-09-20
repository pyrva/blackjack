from dataclasses import dataclass

from deck import Deck, Card


def evaluate_hand(hand):
    # values = [card.value for card in hand if card.value < 10 else 10]
    values = []
    #ace count variable

    for card in hand:
        if card.value <=10:
            values.append(card.value)
        else:
            values.append(10)
    value = sum(values)
    if 1 in values:
        if value <= 11:
            value += 10
        pass
    return value

@dataclass
class Player:
    hand: list[Card]

    # @property
    def is_bust(self):
        return evaluate_hand(self.hand) > 21

class Game(object):

    def __init__(self, players=1):
        self.cards = Deck(include_jokers=False)
        self.cards.shuffle()
        self.players = [Player(self.get_hand()) for _ in range(players + 1)]


    def get_hand(self):
        hand = [self.cards.deal(), self.cards.deal()]
        return hand


    def deal(self, hand):
        hand.append(self.cards.deal())
