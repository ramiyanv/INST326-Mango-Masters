"""
A Blackjack game.
"""
import random
class Card:
    """ A base playing card with a rank, suit, and general-purpose value.
    Attributes:
    rank (str): The rank label, e.g., "2".."10", "J", "Q", "K", or "A".
    suit (str): The suit label, one of: "Clubs", "Diamonds", "Hearts",
    "Spades".
    value (int): A numeric value useful for comparisons (not the Blackjack
    total).
    Blackjack-specific totals are computed in "Hand" class because Aces may
    count as 1 or 11 depending on the rest of the hand.
    """
    def __init__(self, rank: str, suit: str, value: int):
        self.rank = rank
        self.suit = suit
        self.value = value

    def __str__(self):
        """ Return a human-readable card name like "Ace of Hearts".
        Returns:
        A descriptive string for the card (str).
        """
        names = {"J": "Jack", "Q": "Queen", "K": "King", "A": "Ace"}
        rank_name = names.get(self.rank, self.rank)
        return f"{rank_name} of {self.suit}"

class PipCard(Card):
    """ A numeric card (ranks "2" to "10").
    The card's value equals the integer form of its rank.
    Example:
    >>> PipCard("9", "Hearts").value
    9
    """
    def __init__(self, rank: str, suit: str):
        super().__init__(rank, suit, int(rank))

class FaceCard(Card):
    """A face card ("J", "Q", "K", or "A").
    For general comparisons, J/Q/K are valued at 10 and A is 11.
    For Blackjack totals, the flexible Ace logic (1 or 11) lives in "Hand" class.
    """
    def __init__(self, rank: str, suit: str):
        if rank in ["J", "Q", "K"]:
            value = 10
        elif rank == "A":
            value = 11
        super().__init__(rank, suit, value)

def make_card(rank: str, suit: str):
    """ Factory function that returns the appropriate Card subclass.
    Attributes:
    rank (str): Rank label ("2" to "10", "J", "Q", "K", "A").
    suit (str): Suit label ("Clubs", "Diamonds", "Hearts", "Spades").
    Returns:
    A PipCard object for numeric ranks or a FaceCard object otherwise.
    """
    if rank in ["J", "Q", "K", "A"]:
        return FaceCard(rank, suit)
    return PipCard(rank, suit)

class Deck:
    """ A standard 52-card deck.
    Attributes:
    shuffled (bool, optional): If True (default), the deck is shuffled on
    creation.
    cards (list of cards): The internal stack of cards. The right end is
    considered the "top".
    Drawing removes a card from the top (right end) via draw method.
    """
    def __init__(self, shuffled: bool = True):
        self.cards = []
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        for suit in suits:
            for rank in ranks:
                self.cards.append(make_card(rank, suit))
        if shuffled:
            random.shuffle(self.cards)

    def draw(self):
        """ Remove and return the top Card object from the deck.
        Returns:
        Card: The card drawn from the deck.
        Raises:
        RuntimeError: If the deck is empty.
        """
        if not self.cards:
            raise RuntimeError("Cannot draw from an empty deck.")
        return self.cards.pop()

    def __len__(self):
        """Return the number of remaining cards in the deck.
        Returns
        int: Count of cards left.
        """
        return len(self.cards)

class Hand:
    """A collection of cards with Blackjack scoring helpers."""
    def __init__(self):
        """Initialize an empty hand."""
        self.cards = []

    def add(self, card: Card):
        """ Append a Card object to the hand.
        Attributes:
        card (Card): The card to add.
        """
        self.cards.append(card)

    def values_for_blackjack(self):
        """ Compute the best Blackjack total for the hand (<= 21 when possible)."""
        total = 0
        aces = 0
        for card in self.cards:
            if card.rank == "A":
                total += 11
                aces += 1
            elif card.rank in ["J", "Q", "K"]:
                total += 10
            else:
                total += int(card.rank)
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total

    def is_blackjack(self):
        """ Return True if the hand is a natural Blackjack (two-card 21)."""
        return len(self.cards) == 2 and self.values_for_blackjack() == 21

    def is_bust(self):
        """ Return True if the hand's best Blackjack total exceeds 21."""
        return self.values_for_blackjack() > 21

    def __str__(self):
        """ Return a formatted representation including cards and total."""
        return "[" + ", ".join(str(c) for c in self.cards) + f"] (total={self.values_for_blackjack()})"

class Player:
    """ A participant in the game who holds a Hand object and draws cards.
    Attributes:
    name (str): Display name for the player.
    """
    def __init__(self, name: str):
        self.name = name
        self.hand = Hand()

    def draw_from(self, deck: Deck, n: int = 1):
        """Draw "n" cards from a Deck object into the player's hand."""
        for _ in range(n):
            self.hand.add(deck.draw())

    def __str__(self):
        """Return a readable summary of the player's current hand."""
        return f"{self.name}: {self.hand}"

class Dealer:
    """The Blackjack dealer with a simple, fixed strategy (hit until 17)."""
    def __init__(self):
        """Initialize the dealer with an empty Hand object."""
        self.hand = Hand()

    def draw_from(self, deck: Deck, n: int = 1):
        """ Draw "n" cards from a Deck object into the dealer's hand."""
        for _ in range(n):
            self.hand.add(deck.draw())

    def should_hit(self):
        """ Return True if dealer must draw another card (total < 17)."""
        return self.hand.values_for_blackjack() < 17

    def __str__(self):
        """Return a readable summary of the dealer's current hand."""
        return "Dealer " + str(self.hand)

class BlackjackGame:
    """ High-level game controller for a single round of Blackjack."""
    def __init__(self, player_name: str = "Player"):
        self.deck = Deck(shuffled=True)
        self.player = Player(player_name)
        self.dealer = Dealer()

    def initial_deal(self):
        """Deal two cards to the player and two cards to the dealer."""
        for _ in range(2):
            self.player.draw_from(self.deck)
            self.dealer.draw_from(self.deck)

    def player_turn(self, strategy: str = "hold_at_17"):
        """ Automate the player's turn with a basic strategy."""
        while self.player.hand.values_for_blackjack() < 17:
            self.player.draw_from(self.deck)

    def dealer_turn(self):
        """Execute the dealer's forced strategy: hit until total >= 17."""
        while self.dealer.should_hit():
            self.dealer.draw_from(self.deck)

    def determine_winner(self):
        """Compute the round outcome string based on both hands."""
        p_total = self.player.hand.values_for_blackjack()
        d_total = self.dealer.hand.values_for_blackjack()
        if self.player.hand.is_bust() and self.dealer.hand.is_bust():
            return "Both bust: push (tie)."
        if self.player.hand.is_bust():
            return "Dealer wins (player busts)."
        if self.dealer.hand.is_bust():
            return "Player wins (dealer busts)."
        if self.player.hand.is_blackjack() and self.dealer.hand.is_blackjack():
            return "Both have Blackjack: push (tie)."
        if self.player.hand.is_blackjack():
            return "Player wins with Blackjack!"
        if self.dealer.hand.is_blackjack():
            return "Dealer wins with Blackjack."
        if p_total > d_total:
            return "Player wins."
        if d_total > p_total:
            return "Dealer wins."
        return "Push (tie)."

    def play_round(self, player_strategy: str = "hold_at_17"):
        """Play a single round of Blackjack and return the outcome string."""
        if len(self.deck) < 10:
            self.deck = Deck(shuffled=True)
        self.player.hand = Hand()
        self.dealer.hand = Hand()
        self.initial_deal()
        self.player_turn(player_strategy)
        self.dealer_turn()
        credit = "Created by GPT-5 with assistance for [Your Name], 2025-11-12"
        return self.determine_winner()
