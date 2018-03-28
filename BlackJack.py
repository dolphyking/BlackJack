import random
import time
import sys


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
deck = []
playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        self.str = self.rank + ' of ' + self.suit
        return self.str


class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        self.str = ''
        for card in self.deck:
            self.str += '\n ' + card.__str__()
        return 'The deck has: ' + self.str

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.hand = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.hand.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_aces(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -=1

    def __str__(self):
        self.str = ''
        for card in self.hand:
            self.str += '\n ' + card.__str__()
        return self.str


class Chips:

    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

    def __str__(self):
        return self.total


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('Enter your bet: '))
        except ValueError:
            print("That's not an acceptable value.")
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed ", chips.total)
            else:
                break


def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_aces()


def hit_or_stand(deck, hand):
    global playing
    while True:
        b = input('Hit or Stand?: ')
        if b.lower() == 'hit':
            hit(deck, hand)
            break
        elif b.lower() == 'stand':
            print('Player stands. Dealer is playing.')
            playing = False
            return playing
        else:
            print('Sorry, try again.')
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.hand[1])
    sys.stdout.flush()
    time.sleep(1)

    print("\nPlayer's Hand:", *player.hand, sep='\n ')
    sys.stdout.flush()
    time.sleep(1)

def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.hand, sep='\n')
    sys.stdout.flush()
    time.sleep(2)
    print("Dealer's Hand =", dealer.value)
    sys.stdout.flush()
    time.sleep(2)
    print("\nPlayer's Hand:", *player.hand, sep='\n')
    sys.stdout.flush()
    time.sleep(2)
    print("Player's Hand =", player.value)
    sys.stdout.flush()
    time.sleep(2)


def player_busts(player):
    if player.value > 21:
        chips.lose_bet()
        print('Bust, dealer wins.')
        print("Player's total chips decrease to " + str(chips.total))


def player_wins(player, dealer):
    if player.value > dealer.value and player.value < 22:
        chips.win_bet()
        print('Player Wins!')
        print("Player's total chips increase to ", str(chips.total))


def dealer_busts(dealer):
    if dealer.value > 21:
        chips.win_bet()
        print('Dealer Busts. Player Wins!')
        print("Player's total chips increase to ", str(chips.total))


def dealer_wins(player, dealer):
    if player.value < dealer.value and dealer.value < 22:
        chips.lose_bet()
        print('Dealer Wins')
        print("Player's total chips decrease to ", str(chips.total))


def push(player, dealer):
    if player.value == dealer.value:
        print('Push.')
        print("Player's total chips remain at ", str(chips.total))


chips = Chips()

while True:
    print('Welcome to King Casinos!! This is BlackJack. You have ' + str(chips.total) + ' chips.')

    # Create and Shuffle the Deck
    deck = Deck()
    deck.shuffle()

    # Setup Player and Dealers Hand
    player = Hand()
    dealer = Hand()

    # Deal Cards
    player.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    dealer.add_card(deck.deal())

    take_bet(chips)

    print('Dealing', end='')
    sys.stdout.flush()
    for i in range(3):
        time.sleep(.5)
        print('.', end='', flush=True)

    show_some(player, dealer)

    while playing:
        hit_or_stand(deck, player)
        print ("\n" * 100)
        if playing:
            print('Dealing', end='')
            sys.stdout.flush()
            for i in range(3):
                time.sleep(.5)
                print('.', end='', flush=True)
            show_some(player, dealer)

        if player.value > 21:
            player_busts(player)
            break

    while player.value < 22 and dealer.value < 17:

        hit(deck, dealer)

        print('Dealing', end='')
        sys.stdout.flush()
        for i in range(3):
            time.sleep(.5)
            print('.', end='', flush=True)
        show_all(player, dealer)

    player_wins(player, dealer)
    dealer_wins(player, dealer)
    push(player, dealer)
    dealer_busts(dealer)

    while True:
        c = input('Play Again?:  ')
        if c.lower() == 'yes':
            playing = True
            break
        elif c.lower() == 'no':
            print('Leaving table. Thanks for playing!')
            quit()

        else:
            print('Type yes or no.')
            continue
        break



