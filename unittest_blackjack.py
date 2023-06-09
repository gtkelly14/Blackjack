import unittest
import blackjack

class testPlayer(unittest.TestCase):

    def __init__(self):
        self.player = blackjack.Player('Player 1')  
        

   def test_bet(self):
      player = blackjack.Player('Player 1')
      player.bank = 100
      player.bet(10)
      self.assertEqual(player.bank, 90)


    

    
