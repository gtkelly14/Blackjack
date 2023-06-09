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

# Dealer

# Hand


if __name__ == '__main__':
    unittest.main()
