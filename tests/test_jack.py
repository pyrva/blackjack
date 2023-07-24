from jack import Game
from deck import Card

def test_hand_dealt():
    game = Game()
    hand = game.get_hand()
    assert len(hand) == 2


def test_cards_dont_match():
    game = Game()
    hand = game.get_hand()
    assert hand[0] != hand[1]


def test_game_start():
    game = Game()
    assert len(game.cards) == 48
    assert len(game.dealer_hand) == 2
    assert len(game.player_hand) == 2

def test_player_hand_score():
    game = Game()

    hand = [Card(),Card()]
    assert game.evaluate()

# Check count of cards go down over time
