from dataclasses import dataclass

from deck import Deck, Card, Suit


def evaluate_hand(hand):
    # values = [card.value for card in hand if card.value < 10 else 10]
    values = []
    # ace count variable

    for card in hand:
        if card.value <= 10:
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

    # def __str__(self):
    #     print(self.hand)
    #     return ''.join([f"{card.value}{card.suit.value} " for card in self.hand])


class Game(object):
    def __init__(self, players=1, initial_deck=None):
        """
        Initial_deck: list of cards with a specific order to deal.
        """
        self.cards = initial_deck
        if not self.cards:
            self.cards = Deck(include_jokers=False)
            self.cards.shuffle()
        self.players = [Player(self.get_hand()) for _ in range(players + 1)]

    def get_hand(self):
        hand = [self.cards.deal(), self.cards.deal()]
        return hand

    def deal(self, hand):
        hand.append(self.cards.deal())

    def play(self, defined_actions=None):
        for i, player in enumerate(self.players):
            while not player.is_bust():
                print("-" * 20)
                print("player_id: ", i, "#cards: ", len(player.hand), "cards: ", player)
                if defined_actions:
                    print(defined_actions)
                    action = defined_actions.pop(0)
                    print(defined_actions)
                else:
                    action = input("hit (h) or stand (s)")

                if action == "h":
                    self.deal(player.hand)
                    print(player)
                else:
                    print(player)
                    break


if __name__ == "__main__":
    game = Game()
    game.play(["h", "s", "s"])
    print(game)
