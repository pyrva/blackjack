import pytest
from deck import Card, Suit, Value, Deck

from jack import Game, Player, evaluate_hand


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
    Game()

    hand = [Card(suit="spades", value=2), Card(suit="spades", value=3)]
    assert evaluate_hand(hand) == 5


def test_deal_one_card():
    game = Game()
    game.deal(game.players[0].hand)
    game.deal(game.players[1].hand)
    assert len(game.players[0].hand) == 3
    assert len(game.players[1].hand) == 3

    # Check count of cards go down over time


def test_hand_bust():
    player = Player(
        [
            Card(suit="spades", value=10),
            Card(suit="spades", value=10),
            Card(suit="spades", value=2),
        ]
    )

    assert player.is_bust() is True


@pytest.mark.parametrize(
    "first_card, second_card, expected_score",
    [
        (
            Card(suit=Suit.Spades, value=Value.Two),
            Card(suit=Suit.Hearts, value=Value.Three),
            5,
        ),
        (
            Card(suit=Suit.Diamonds, value=Value.Six),
            Card(suit=Suit.Clubs, value=Value.Eight),
            14,
        ),
    ],
)
def test_score_is_calculated_correctly_for_number_cards(
    first_card, second_card, expected_score
):
    """The score should be the sum of the values of the cards."""
    assert evaluate_hand([first_card, second_card]) == expected_score


@pytest.mark.parametrize(
    "first_card, second_card, expected_score",
    [
        (
            Card(suit=Suit.Spades, value=Value.Eight),
            Card(suit=Suit.Hearts, value=Value.Jack),
            18,
        ),
        (
            Card(suit=Suit.Spades, value=Value.Eight),
            Card(suit=Suit.Hearts, value=Value.Queen),
            18,
        ),
        (
            Card(suit=Suit.Spades, value=Value.Eight),
            Card(suit=Suit.Hearts, value=Value.King),
            18,
        ),
    ],
)
def test_score_is_calculated_correctly_for_face_cards(
    first_card, second_card, expected_score
):
    """The score should be the sum of the values of the cards with face cards having a value of 10."""
    assert evaluate_hand([first_card, second_card]) == expected_score


# @pytest.mark.xfail
@pytest.mark.parametrize(
    "hand, expected_score",
    [
        (
            [
                Card(suit=Suit.Spades, value=Value.Ace),
                Card(suit=Suit.Hearts, value=Value.Ace),
            ],
            12,
        ),
        (
            [
                Card(suit=Suit.Spades, value=Value.Ace),
                Card(suit=Suit.Hearts, value=Value.Six),
                Card(suit=Suit.Hearts, value=Value.Three),
            ],
            20,
        ),
        (
            [
                Card(suit=Suit.Spades, value=Value.Ace),
                Card(suit=Suit.Hearts, value=Value.Six),
                Card(suit=Suit.Hearts, value=Value.King),
            ],
            17,
        ),
        (
            [
                Card(suit=Suit.Hearts, value=Value.King),
                Card(suit=Suit.Hearts, value=Value.Ace),
            ],
            21,
        ),
        (
            [
                Card(suit=Suit.Hearts, value=Value.Ace),
                Card(suit=Suit.Clubs, value=Value.Ace),
                Card(suit=Suit.Hearts, value=Value.Six),
            ],
            18,
        ),
    ],
)
def test_score_is_calculated_correctly_for_aces(hand, expected_score):
    """The score should be the sum of the values of the cards with aces having a value of 1 or 11."""
    assert evaluate_hand(hand) == expected_score


# @pytest.mark.skip
def test_correct_number_of_cards_on_hit():
    """The player should have one more card after hitting."""
    starting_deck = Deck(
        [
            Card(suit=Suit.Spades, value=Value.Ten),
            Card(suit=Suit.Spades, value=Value.Eight),
            Card(suit=Suit.Diamonds, value=Value.Ten),
            Card(suit=Suit.Diamonds, value=Value.Eight),
            Card(suit=Suit.Clubs, value=Value.Ten),
            Card(suit=Suit.Clubs, value=Value.Eight),
        ]
    )
    game = Game()

    assert len(game.players[0].hand) == 2
    game.play(["h"])
    assert len(game.players[0].hand) == 3


@pytest.mark.xfail
def test_correct_number_of_cards_on_stand():
    """The player should have the same number of cards after standing."""
    player_hand = [
        Card(suit=Suit.Spades, value=Value.Ten),
        Card(suit=Suit.Spades, value=Value.Eight),
    ]
    assert len(player_hand) == 2
    # Stand
    assert len(player_hand) == 2


@pytest.mark.parametrize(
    "first_card, second_card, hit",
    [
        (
            Card(suit=Suit.Spades, value=Value.Ten),
            Card(suit=Suit.Hearts, value=Value.Six),
            True,
        ),
        (
            Card(suit=Suit.Spades, value=Value.Ten),
            Card(suit=Suit.Hearts, value=Value.Seven),
            False,
        ),
    ],
)
def test_dealer_must_hit(first_card, second_card, hit):
    """The dealer must hit if their score is less than 17."""
    hand = [first_card, second_card]
    evaluate_dealer_hand(hand)
    assert False


@pytest.mark.xfail
def test_player_wins_with_higher_score():
    """The player wins when their score is higher than the dealer's score."""
    [Card(suit=Suit.Spades, value=Value.Ten), Card(suit=Suit.Spades, value=Value.King)]
    [Card(suit=Suit.Spades, value=Value.Ten), Card(suit=Suit.Spades, value=Value.Eight)]
    assert False


@pytest.mark.xfail
def test_player_loses_with_lower_score():
    """The player loses when their score is lower than the dealer's score."""
    [Card(suit=Suit.Spades, value=Value.Ten), Card(suit=Suit.Spades, value=Value.Eight)]
    [Card(suit=Suit.Spades, value=Value.Ten), Card(suit=Suit.Spades, value=Value.King)]
    assert False


@pytest.mark.xfail
def test_player_ties_with_same_score():
    """The player ties when their score is the same as the dealer's score."""
    [Card(suit=Suit.Spades, value=Value.Ten), Card(suit=Suit.Spades, value=Value.Eight)]
    [Card(suit=Suit.Spades, value=Value.Ten), Card(suit=Suit.Spades, value=Value.Eight)]
    assert False


@pytest.mark.xfail
def test_funds_increase_on_win():
    """The player's funds should increase when they win.

    The player's funds should increase by the amount they bet. In this case, the player has 100 credits
    and bets 10. The player wins and should now have 110 credits.
    """
    [Card(suit=Suit.Spades, value=Value.Ten), Card(suit=Suit.Spades, value=Value.King)]
    [Card(suit=Suit.Spades, value=Value.Ten), Card(suit=Suit.Spades, value=Value.Eight)]
    player_funds = 100
    # Play
    assert player_funds == 110


@pytest.mark.xfail
def test_funds_decrease_on_loss():
    """The player's funds should decrease when they lose.

    The player's funds should decrease by the amount they bet. In this case, the player has 100 credits
    and bets 10. The player loses and should now have 90 credits.
    """
    [Card(suit=Suit.Spades, value=Value.Ten), Card(suit=Suit.Spades, value=Value.Eight)]
    [Card(suit=Suit.Spades, value=Value.Ten), Card(suit=Suit.Spades, value=Value.King)]
    player_funds = 100
    # Play
    assert player_funds == 90


@pytest.mark.xfail
def test_funds_stay_the_same_on_tie():
    """The player's funds should stay the same when they tie.

    The player's funds should stay the same. In this case, the player has 100 credits
    and bets 10. The player ties and should still have 100 credits.
    """
    [Card(suit=Suit.Spades, value=Value.Ten), Card(suit=Suit.Spades, value=Value.Eight)]
    [Card(suit=Suit.Spades, value=Value.Ten), Card(suit=Suit.Spades, value=Value.Eight)]
    player_funds = 100
    # Play
    assert player_funds == 100
