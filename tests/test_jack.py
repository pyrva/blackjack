from jack import Game, Player, evaluate_hand
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


def test_player_hand_score():
    game = Game()

    hand = [Card(suit='spades', value=2),Card(suit='spades', value=3)]
    assert evaluate_hand(hand) == 5

def test_deal_one_card():
    game = Game()
    game.deal(game.players[0].hand)
    game.deal(game.players[1].hand)
    assert len(game.players[0].hand) == 3
    assert len(game.players[1].hand) == 3


    # Check count of cards go down over time

def test_hand_bust():
    player = Player([Card(suit='spades', value=10), Card(suit='spades', value=10), Card(suit='spades', value=2)])

    assert player.is_bust() == True
