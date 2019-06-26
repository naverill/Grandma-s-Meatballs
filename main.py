"""
Main program:
 reads command line options, trains model and runs Grandmas Meatball Game

 by Nina Averill <averill.nina@gmail.com>
 """

from player import QLearner, HPlayer
import sys
from grandmas_meatballs import GrandmasMeatballs

def playing():
     game = input("Continue? (y/n) ")

     if game.lower() == "y":
         return True
     else:
        return False

if __name__=="__main__":
    is_q = True
    grandma = QLearner(is_q)
    opponent = QLearner(not is_q)

    game = GrandmasMeatballs(grandma, opponent)

    player = HPlayer()

    if game.setup(sys.argv):
        while playing():
            game.start_game(grandma, player)
