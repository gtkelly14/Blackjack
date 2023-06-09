'''
Blackjack game
'''
# Imports
import random

# Statics and Global


# Class Definitions
class Deck:
    '''
    Holds a deck of cards
    '''

    suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10',
             'Jack', 'Queen', 'King']

    cards = []

    def __init__(self):
        self.cards = []
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(Card(suit, rank))
        self.shuffle()

    def shuffle(self):
        '''
        Shuffle the deck
        '''
        random.shuffle(self.cards)

    def deal(self):
        '''
        Deal a card from the deck
        '''
        return self.cards.pop()


class Card:
    '''
    Holds a card
    '''

    suit = ''
    rank = ''
    visible = False

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):

        return f'{self.rank} of {self.suit}'

    def turn_over(self):
        '''
        Turns a card over making it visible
        '''
        self.visible = True

    def get_value(self):
        '''
        Determines the value of a card, Jack, Queen, King are 10, Ace is 11
        '''
        if self.rank == 'Ace':
            return 11

        if self.rank in ['Jack', 'Queen', 'King']:
            return 10

        return int(self.rank)


class Player:
    '''
    Holds a player and the cards in their hand
    '''
    cards = []
    name = ''
    money = 0
    busted = False

    def __init__(self, name, money):
        self.name = name
        self.money = money

    def __str__(self):
        return f'{self.name} has ${self.money}'

    def bet(self):
        '''
        Make a bet with available player money. Cannot exceed the amount of mony the player has
        '''
        amount = 0
        bet_placed = False

        while not bet_placed:

            try:

                inp_val = input(
                    f'How much would you like to bet? (Max: ${self.money})')
                if inp_val.upper() == 'Q':
                    bet_placed = True
                    return 0

                amount = int(inp_val)

                if amount > self.money:
                    print(f'You do not have enough money to bet ${amount}')

                else:
                    self.money -= amount
                    bet_placed = True
                    return amount

            except ValueError:
                print('Please enter a number')

                continue

    def get_card(self, card):
        '''
        Player receives a card and adds it to their hand
        '''
        self.cards.append(card)

    def show_cards(self):
        '''
        Show the cards in the players hand
        '''
        print(f'{self.name} has:')
        for card in self.cards:
            print(card)

    def get_hand_value(self):
        ''' 
        Get the value of the players hand
        '''
        ace_count = 0
        hand_value = 0

        for card in self.cards:
            if card.rank == 'Ace':
                ace_count += 1
            elif card.rank in ['Jack', 'Queen', 'King']:
                hand_value += 10
            else:
                hand_value += int(card.rank)

        if ace_count > 0:
            if 21 - hand_value >= 11:
                hand_value += 11 + ace_count - 1
            else:
                hand_value += ace_count

        return hand_value

    def play(self, deck):
        ''' 
        Player plays their hand
        '''

        continue_playing = True

        while continue_playing and not self.busted:
            print(
                f'{self.name} you have  {self.get_hand_value()}')
            if self.get_hand_value() > 21:
                print('You have Busted')
                self.busted = True
                continue_playing = False
                break

            inp_val = input('Would you like to hit or stand? (H/S)')
            if inp_val.upper() == 'H':
                self.get_card(deck.deal())
                self.show_cards()
                continue_playing = True
                continue

            if inp_val.upper() == 'S':
                continue_playing = False
                break

            print('Please enter H or S')
            continue


class Dealer:
    '''
    Holds the dealer within the blackjack game
    '''
    cards = []
    busted = False

    def __init__(self):
        pass

    def get_card(self, card):
        '''
        Dealer recieves a card and adds it to their hand. If it is the first card they recieve
        it is turned over so the player cannot see what card it is
        '''
        if len(self.cards) > 0:
            card.turn_over()
        self.cards.append(card)

    def show_cards(self):
        '''
        Show the cards in the dealers hand. If a card is not visible, it is shown as face down
        '''
        print('Dealer has:')
        for card in self.cards:
            if card.visible:
                print(card)
            else:
                print('Card face down')

    def show_all_cards(self):
        '''
        Turns all cards in the dealers hand over so they are visible
        '''
        for card in self.cards:
            card.turn_over()
        self.show_cards()

    def get_hand_value(self):
        '''
        Get the value of the dealers hand
        '''

        ace_count = 0
        hand_value = 0

        for card in self.cards:
            if card.rank == 'Ace':
                ace_count += 1
            else:

                if card.rank in ['Jack', 'Queen', 'King']:
                    hand_value += 10
                else:
                    hand_value += int(card.rank)

        if ace_count > 0:
            if 21 - hand_value >= 11:
                hand_value += 11 + ace_count - 1
            else:
                hand_value += ace_count

        return hand_value

    def play(self, deck):
        '''
        Dealer plays their hand
        '''

        continue_playing = True

        while continue_playing and not self.busted:
            self.show_all_cards()
            print(f'Dealer has {self.get_hand_value()}')
            if self.get_hand_value() > 21:
                print('Dealer has Busted')
                self.busted = True
                continue_playing = False
                break

            if self.get_hand_value() < 17:
                self.get_card(deck.deal())
                continue_playing = True
                continue

            continue_playing = False


class Hand:
    '''
    Defines a hand of blackjack
    '''

    pot = 0
    curr_dealer = None
    curr_player = None
    deck = None

    def __init__(self, dealer, player):

        self.curr_dealer = dealer
        self.curr_player = player
        self.deck = Deck()
        self.pot = 0

    def __str__(self):
        return f'Pot: ${self.pot}'

    def deal_the_cards(self):
        ''' 
        Deal cards to player and dealer
        '''
        count = 1
        while count <= 4:
            if count % 2 == 0:
                self.curr_dealer.get_card(self.deck.deal())
            else:
                self.curr_player.get_card(self.deck.deal())
            count += 1

        self.curr_player.show_cards()

        self.curr_dealer.show_cards()

    def play(self):
        '''
        Play the hand. Player first, then dealer
        '''

        bet = self.curr_player.bet()

        if bet > 0:
            self.pot += (2*bet)

        else:
            print('Goodbye!')
            return

        self.deal_the_cards()
        self.curr_player.play(self.deck)

        if not self.curr_player.busted:
            self.curr_dealer.play(self.deck)

        if self.curr_player.busted:
            print(f'{self.curr_player.name} has lost ${self.pot}')
            return

        if self.curr_dealer.busted:

            print(f'{self.curr_player.name} has won ${self.pot}')
            self.curr_player.money += self.pot
            print(f'{self.curr_player.name} has ${self.curr_player.money}')
            return

        if self.curr_dealer.get_hand_value() > self.curr_player.get_hand_value():
            print(f'{self.curr_player.name} has lost ${self.pot/2}')
            print(f'{self.curr_player.name} has ${self.curr_player.money}')
            return

        if self.curr_dealer.get_hand_value() < self.curr_player.get_hand_value():
            print(f'{self.curr_player.name} has won ${self.pot}')
            self.curr_player.money += self.pot
            print(f'{self.curr_player.name} has ${self.curr_player.money}')
            return

        print('Push')

        self.curr_player.money += self.pot
        self.pot = 0
        print(f'{self.curr_player.name} has ${self.curr_player.money}')


# Function Definitions


# Main Body

def main():
    '''
    Main function to run the game
    '''
    inp_val = input(
        'Welcome to Blackjack! Press any key to continue or Q to quit')

    if inp_val.upper() == 'Q':
        print('Goodbye!')
        return

    player_name = input('Please enter your name: ')
    try:

        player_money = int(
            input('Please enter the amount of money you would like to start with: '))
    except ValueError:
        player_money = 0

    player = Player(player_name, player_money)
    dealer = Dealer()
    hand = Hand(dealer, player)
    hand.play()


if __name__ == '__main__':
    main()
