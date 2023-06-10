'''
Unit Test Module for blackjack.py
'''

import unittest
import blackjack

# Card


class TestCards(unittest.TestCase):

    '''
    Test Cases for the Card class
    '''

    def test_face_card(self):
        '''
        Test Face Card
        '''
        card = blackjack.Card('Spades', 'Jack')
        self.assertEqual(card.get_value(), 10)
        self.assertEqual(str(card), 'Jack of Spades')

    def test_ace_card(self):
        '''
        Test Ace Card
        '''
        card = blackjack.Card('Spades', 'Ace')
        self.assertEqual(card.get_value(), 11)
        self.assertEqual(str(card), 'Ace of Spades')

    def test_number_card(self):
        '''
        Test Number Card
        '''
        card = blackjack.Card('Spades', '2')
        self.assertEqual(card.get_value(), 2)
        self.assertEqual(str(card), '2 of Spades')

# Deck


class TestDeck(unittest.TestCase):
    '''
    Test cases for Deck class
    '''

    def test_number_of_cards(self):
        '''
        Test number of cards in the deck
        '''

        deck = blackjack.Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_shuffle(self):
        '''
        Test shuffle of random order
        '''
        deck = blackjack.Deck()
        card_a = deck.cards[51]
        deck.shuffle()
        card_b = deck.cards[51]
        self.assertNotEqual(card_a, card_b)

    def test_deal(self):
        '''
        Test deal of a card
        '''
        deck = blackjack.Deck()
        card_a = deck.cards[51]
        card_b = deck.deal()
        self.assertEqual(len(deck.cards), 51)
        self.assertIsInstance(card_b, blackjack.Card)
        self.assertEqual(card_a, card_b)

# Player


class TestPlayer(unittest.TestCase):
    '''
    Test caese for Player aclass
    '''
    player_name = 'Test Player'

    def test_init(self):
        """
        Test cases for initializing the class
        """
        player = blackjack.Player(self.player_name, 100)
        self.assertEqual(player.name, "Test Player")
        self.assertEqual(player.money, 100)

    def test_bet(self):
        '''
        Test betting scenarios. Bet less than bankroll, then attempt bet > bankroll
        '''

        # Less than Max
        blackjack.input = lambda _: '75'

        player = blackjack.Player(self.player_name, 100)
        amount = player.bet()
        self.assertEqual(amount, 75)
        self.assertEqual(player.money, 25)

        # Test > Max
        player = blackjack.Player(self.player_name, 50)
        amount = player.bet()
        self.assertEqual(amount, 0)
        self.assertEqual(player.money, 50)

    def test_player_get_hand_value(self):
        '''
        Test paths to determine hand value
        '''
        player = blackjack.Player(self.player_name, 100)
        player.cards = [blackjack.Card(
            'Spades', 'Jack'), blackjack.Card('Spades', 'Ace')]
        self.assertEqual(player.get_hand_value(), 21)

        player.cards = [blackjack.Card(
            'Spades', '8'), blackjack.Card('Spades', 'Ace')]
        self.assertEqual(player.get_hand_value(), 19)

        player.cards.append(blackjack.Card('Spades', 'King'))
        self.assertEqual(player.get_hand_value(), 19)

        player.cards.append(blackjack.Card('Spades', '5'))
        self.assertEqual(player.get_hand_value(), 24)

    def test_play_stay(self):
        '''
        test stay scenarios for player
        '''

        blackjack.input = lambda _: 'S'
        deck = blackjack.Deck()
        player = blackjack.Player(self.player_name, 100)
        player.cards = [blackjack.Card(
            'Spades', '8'), blackjack.Card('Spades', 'Ace')]
        player.play(deck)
        self.assertEqual(len(player.cards), 2)
        self.assertEqual(player.get_hand_value(), 19)

    def test_play_hit(self):
        '''
        Test hit scenario for player
        '''
        blackjack.input = lambda _: 'H'
        deck = blackjack.Deck()
        deck.cards[51] = blackjack.Card('Clubs', '2')

        player = blackjack.Player(self.player_name, 100)

        player.cards = [blackjack.Card(
            'Spades', '8'), blackjack.Card('Spades', 'Ace')]
        player.play(deck)
        self.assertEqual(len(player.cards), 3)
        self.assertEqual(player.get_hand_value(), 21)

    def test_play_bust(self):
        ''' 
        Test bust scenario for player
        '''
        blackjack.input = lambda _: 'H'
        deck = blackjack.Deck()
        deck.cards[51] = blackjack.Card('Clubs', 'King')

        player = blackjack.Player(self.player_name, 100)

        player.cards = [blackjack.Card(
            'Spades', '10'), blackjack.Card('Spades', '8')]
        player.play(deck)
        self.assertEqual(len(player.cards), 3)
        self.assertTrue(player.busted)

    def teardown_method(self):
        '''
        Revert input function in module back to original
        '''

        blackjack.input = input

# Dealer


class TestDealer(unittest.TestCase):
    '''
    Test Cases for Dealer

    '''

    def test_dealer_get_hand_value(self):
        '''
        Test paths to determine hand value
        '''
        dealer = blackjack.Dealer()
        dealer.cards = [blackjack.Card(
            'Spades', 'Jack'), blackjack.Card('Spades', 'Ace')]
        self.assertEqual(dealer.get_hand_value(), 21)

        dealer.cards = [blackjack.Card(
            'Spades', '8'), blackjack.Card('Spades', 'Ace')]
        self.assertEqual(dealer.get_hand_value(), 19)

        dealer.cards.append(blackjack.Card('Spades', 'King'))
        self.assertEqual(dealer.get_hand_value(), 19)

        dealer.cards.append(blackjack.Card('Spades', '5'))
        self.assertEqual(dealer.get_hand_value(), 24)

    def test_play_stay(self):
        '''
        Hand Value of 18 - stay
        '''
        deck = blackjack.Deck()
        dealer = blackjack.Dealer()
        dealer.cards = [blackjack.Card(
            'Spades', '8'), blackjack.Card('Spades', 'King')]
        dealer.play(deck)
        self.assertEqual(len(dealer.cards), 2)
        self.assertEqual(dealer.get_hand_value(), 18)

    def test_play_hit(self):
        '''
        Hand value of 16 - hit to 20
        '''
        deck = blackjack.Deck()
        deck.cards[51] = blackjack.Card('Clubs', '4')
        dealer = blackjack.Dealer()
        dealer.cards = [blackjack.Card(
            'Spades', '6'), blackjack.Card('Spades', 'King')]
        dealer.play(deck)
        self.assertEqual(len(dealer.cards), 3)
        self.assertEqual(dealer.get_hand_value(), 20)

    def test_play_bust(self):
        '''
        Hand value of 16 - hit to 23 - busted
        '''
        deck = blackjack.Deck()
        deck.cards[51] = blackjack.Card('Clubs', '7')
        dealer = blackjack.Dealer()
        dealer.cards = [blackjack.Card(
            'Spades', '6'), blackjack.Card('Spades', 'King')]
        dealer.play(deck)
        self.assertEqual(len(dealer.cards), 3)
        self.assertEqual(dealer.get_hand_value(), 23)
        self.assertTrue(dealer.busted)

    def teardown_method(self):
        '''
        Revert input function in module back to original
        '''

        print("Function Teardown")
        blackjack.input = input


# Hand
if __name__ == '__main__':
    unittest.main()
