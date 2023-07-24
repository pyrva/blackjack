from deck import Deck



class Game(object):

    def __init__(self):
        self.cards = Deck(include_jokers=False)
        self.cards.shuffle()
        self.dealer_hand = self.get_hand()
        self.player_hand = self.get_hand()

    def get_hand(self):
        hand = [self.cards.deal(), self.cards.deal()]
        return hand

