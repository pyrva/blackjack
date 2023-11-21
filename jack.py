from dataclasses import dataclass
from deck import Deck, Card

Hand = list[Card]


def evaluate_hand(hand: Hand) -> int:
    # TODO Should this function be on it's own or in the Player class?
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
    """A player in a game of Blackjack.

    :param id: Player ID
    :param hand: Initial hand of two cards
    """

    id: int
    hand: list[Card]

    @property
    def is_bust(self) -> bool:
        """Determine if the player is busted (score > 21)."""
        return evaluate_hand(self.hand) > 21

    @property
    def name(self) -> str:
        """Player name."""
        return f"Player {self.id}"

    @property
    def score(self) -> int:
        """Score of the player's hand."""
        return evaluate_hand(self.hand)

    @property
    def cards(self) -> str:
        """String representation of the player's hand."""
        display_value = {
            1: "A",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "10",
            11: "J",
            12: "Q",
            13: "K",
        }
        return " ".join(
            [
                f"[{display_value[card.value.value]:>2} {card.suit.value} ]"
                for card in self.hand
            ]
        )

    @property
    def state(self) -> str:
        """String representation of the player's state (score and hand)."""
        return f"{self.score:>2}  {self.cards}"

    def __str__(self):
        return f"{self.name:<10} {self.state}"


@dataclass
class Dealer:
    # TODO This class is almost identical to Player, we can probably refactor
    hand: list[Card]
    current: bool = False

    @property
    def is_bust(self) -> bool:
        """Determine if the dealer is busted (score > 21)."""
        return evaluate_hand(self.hand) > 21

    @property
    def name(self) -> str:
        """Dealer name."""
        return "Dealer"

    @property
    def score(self) -> int:
        """Score of the dealer's hand."""
        revealed_cards = self.hand
        if not self.current:
            revealed_cards = self.hand[:1]

        return evaluate_hand(revealed_cards)

    @property
    def cards(self) -> str:
        """String representation of the dealer's hand."""
        revealed_cards = self.hand
        if not self.current:
            revealed_cards = self.hand[:1]
        # TODO revealed cards logic is duplicated in score property

        display_value = {
            1: "A",
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "10",
            11: "J",
            12: "Q",
            13: "K",
        }
        return " ".join(
            [
                f"[{display_value[card.value.value]:>2} {card.suit.value} ]"
                for card in revealed_cards
            ]
        )

    @property
    def state(self) -> str:
        """String representation of the Dealer's state (score and hand)."""
        return f"{self.score:>2}  {self.cards}"

    def __str__(self):
        return f"{self.name:<10} {self.state}"


class Game(object):
    def __init__(self, players: int = 1, initial_deck: list[Card] = None) -> None:
        """Setup a game of Blackjack.

        The game will add a dealer as the last player.

        :param players: Number of players in game excluding dealer, defaults to 1
        :param initial_deck: Ordered deck (only used for testing), defaults to None
        """
        self.cards = Deck(include_jokers=False)
        self.cards.shuffle()

        # Overwrite deck if we're testing
        if initial_deck:
            self.cards.clear()
            self.cards.extend(initial_deck)

        self.players = [Player(id + 1, self.get_hand()) for id in range(players)]
        self.players.append(Dealer(self.get_hand()))

    def get_hand(self) -> Hand:
        """Deal a hand of two cards to a player.

        The two cards are removed from the game deck when dealt to a player.
        """
        hand = [self.cards.deal(), self.cards.deal()]
        return hand

    def deal(self, hand: Hand) -> None:
        """Deal a single card to a player."""
        hand.append(self.cards.deal())

    def play(self, defined_actions: list[str] | str = None):
        """Play a game of Blackjack.

        This loop will run until all players are bust or have stood.

        :param defined_actions: predefined actions (only used for testing),
            should only contain values of 's' (stand) or 'h' (hit), defaults to None
        """
        # TODO This function is too long, we can break it up into multiple functions
        defined_actions = list(defined_actions or [])

        for player in self.players:
            print(player)

        for i, player in enumerate(self.players):
            print("\n", player.name.center(30, "-"))
            player.current = True

            while not player.is_bust:
                if defined_actions:
                    action = defined_actions.pop(0)
                else:
                    if i == len(self.players) - 1:
                        # TODO This logic might be useful for automated players as well as the dealer
                        action = "h" if player.score < 17 else "s"
                        if action == "h":
                            print(f"🤖 {player.state} -> Dealer Hits")
                        if action == "s":
                            print(f"🤖 {player.state} -> Dealer Stands")
                    else:
                        action = input(f"hit (h) or stand (s)?   {player.state}: ")

                if action == "h":
                    self.deal(player.hand)
                elif action == "s":
                    if not i == len(self.players) - 1:
                        print("🧍Player Stands")
                    break
                else:
                    print(f"Invalid action: {action}")

                if player.is_bust:
                    print(f"💥 {player.name} busted! 💥")

            print(player.state)
            player.current = False

        print("\n", "Results".center(30, "="))
        for player in self.players[:-1]:
            if player.is_bust:
                print(f"🧍Player {player.id} busted! 💥")
            elif player.score > self.players[-1].score or self.players[-1].is_bust:
                print(f"🧍Player {player.id} wins! 🏆")
            elif player.score < self.players[-1].score:
                print(f"🤖 Dealer wins! 🏆")
            else:
                print(f"🤝 It's a draw! 🤝")


if __name__ == "__main__":
    n_players = int(input("How many players? [1]") or 1)
    print(
        f"We have {n_players} {'player' if n_players == 1 else 'players'}, plus the dealer which we're pretty sure is a robot 🤖."
    )

    game = Game(players=n_players)
    game.play()
