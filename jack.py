from dataclasses import dataclass
from deck import Deck, Card

Hand = list[Card]

DISPLAY_VALUE = {
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


def display_card(card: Card) -> str:
    """Display a card."""
    return f"[{DISPLAY_VALUE[card.value.value]:>2} {card.suit.value} ]"


@dataclass
class Player:
    """A player in a game of Blackjack.

    :param id: Player ID
    :param hand: Initial hand of two cards
    """

    id: int
    hand: list[Card]
    dealer: bool = False
    current: bool = False

    @property
    def score(self) -> int:
        """Score of the player's hand."""
        values = []

        for card in self.revealed_cards:
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

    @property
    def is_bust(self) -> bool:
        """Determine if the player is busted (score > 21)."""
        return self.score > 21

    @property
    def name(self) -> str:
        """Player name."""
        return "Dealer" if self.dealer else f"Player {self.id}"

    @property
    def revealed_cards(self) -> Hand:
        """Cards that are revealed to other players."""
        if self.dealer and not self.current:
            return self.hand[:1]
        return self.hand

    @property
    def cards(self) -> str:
        """String representation of the player's hand."""
        return " ".join([display_card(card) for card in self.revealed_cards])

    @property
    def state(self) -> str:
        """String representation of the player's state (score and hand)."""
        return f"{self.score:>2}  {self.cards}"

    def __str__(self):
        return f"{self.name:<10} {self.state}"

    def next_action(self, threshold: int = 17) -> str:
        """Determine the next action for the player."""
        action = "s"
        if not self.dealer:
            action = input(f"hit (h) or stand (s)?   {self.state}: ")
        elif self.score < threshold:
            action = "h"

        return action

    def __eq__(self, other: object) -> bool:
        return self.score == other.score

    def __gt__(self, other: object) -> bool:
        return self.score < other.score


class Game(object):
    def __init__(self, players: int = 1, initial_deck: list[Card] = None) -> None:
        """Setup a game of Blackjack.

        The game will add a dealer as the last player.

        :param players: Number of players in game excluding dealer, defaults to 1
        :param initial_deck: Ordered deck (only used for testing), defaults to None
        """
        self.deck = Deck(include_jokers=False)
        self.deck.shuffle()

        # Overwrite deck if we're testing
        if initial_deck:
            self.deck.clear()
            self.deck.extend(initial_deck)

        self.players = [Player(id + 1, self.get_card(n=2)) for id in range(players + 1)]
        self.players[-1].dealer = True

    def get_card(self, n: int = 1) -> list[Card]:
        """Deal cards to a player.

        :param n: Number of cards to deal, defaults to 1
        """
        return [self.deck.deal() for _ in range(n)]

    def print_player_summary(self, end_of_game: bool = False) -> None:
        """Print a summary of all players.

        :param end_of_game: Whether this is the end of the game, defaults to False
            This is used to determine if the dealer's hand should be revealed
        """
        print("\n", "Player Summary".center(30, "-"))
        for player in self.players:
            player.current = end_of_game
            if end_of_game:
                if player.is_bust:
                    icon = "💥"
                elif player.dealer:
                    icon = "🤖"
                elif player == self.players[-1]:
                    icon = "👔"

                # TODO This logic doesn't seem to be working correctly
                elif player > self.players[-1]:
                    icon = "👑"
                else:
                    icon = "👎"
                print(icon, end=" ")
            print(player)
            player.current = False

    def play(self, defined_actions: list[str] | str = None):
        """Play a game of Blackjack.

        This loop will run until all players are bust or have stood.

        :param defined_actions: predefined actions (only used for testing),
            should only contain values of 's' (stand) or 'h' (hit), defaults to None
        """
        defined_actions = list(defined_actions or [])

        self.print_player_summary()

        for player in self.players:
            print("\n", player.name.center(30, "-"))
            player.current = True

            while not player.is_bust:
                if defined_actions:
                    action = defined_actions.pop(0)
                else:
                    action = player.next_action()

                if action == "h":
                    card = self.get_card()
                    player.hand.extend(card)
                    print(f"{player.name} Hits! {display_card(card[0])}")

                elif action == "s":
                    print(f"{player.name} Stands!")
                    break
                else:
                    print(f"Invalid action: {action}")

                if player.is_bust:
                    print(f"💥 {player.name} busted! 💥")

            print(player.state)
            player.current = False

        self.print_player_summary(end_of_game=True)


if __name__ == "__main__":
    n_players = int(input("How many players? [1] ") or 1)
    print(
        f"We have {n_players} {'player' if n_players == 1 else 'players'}, "
        "plus the dealer which we're pretty sure is a robot 🤖."
    )

    game = Game(players=n_players)
    game.play()
