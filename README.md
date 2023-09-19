# Blackjack coding nights

This repository houses the code we create during coding nights at PyRVA.

We leverage the [deck](https://github.com/zooba/deck) Python package to handle dealing with the cards.

The goal of this library is to develop a game of Blackjack that can be played by any number of players. The intention is to write the game logic independent of any interface.

## Blackjack

Each player is playing to beat the dealer, they do not play against other players. The goal is to get as close to 21 without going over.

### Card Values

**2 - 10**: Number cards are worth their numeric value
**J/Q/K**: Royal cards are worth 10 points
**Aces**: Aces are worth 1 point or 11 points, whichever is more advantageous to the player

### Dealing

Each player receives two cards face up with the exception of the dealer which has one card face up and the other face down.

If a player's two cards have a value of 21 and the dealer does not, they automatically win.

### Playing

Each player will choose to **hit** or **stand**. When a player **hits**, they are dealt the top card of the deck. If they choose to **stand**, they do not receive any additional cards and their turn is over. If they player goes over 21, they **bust** and automatically lose.

Once a player **stands** or **busts**, the next player has their turn.

The dealer goes last. The dealer must **hit** until they have a value greater than 17.

If the dealer **busts**, any player who has not already busted wins. If the dealer does not **bust**, any player with a higher score **wins** provided they did not **bust**. Any player with a lower score **loses** and any player with the same value of the dealer **ties**.

### Betting

Players determine how much money they want to bet. All bets must be made prior to the deal phase.

If a player **wins** they gain the amount of their original bet.
if a player **loses** they lose their original bet.
If a player **ties** they take their bet back, but do not gain additional money.

### Extra Elements

The game of Blackjack contains a few more options for the players.

- Splitting pairs: if the players first two cards are the same denomination, they may split their hand into two hands on their turn.
- Doubling down: if the player's hand totals 9, 10, or 11 after the initial deal, they may dobule their initial bet and only get one extra card.
- Insurance: If the dealer is showing an Ace, all players may make a second bet as to if the dealer's second card has a value of 10.

For more information, see the [rules](https://bicyclecards.com/how-to-play/blackjack/)
