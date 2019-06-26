"""
QMinMax Algorithm Class:
Reinforcement Learning environment for a Zero-Sum Adversarial game

  - epsilon:  probability that QPlayer chooses a move at random ("epsilon-greedy" exploration)
  - alpha: learning rate of agent
  - gamma: discount factor

by Nina Averill <averill.nina@gmail.com>
"""

import random
import player
class QMinMaxGame(object):
    def __init__(self, player, opponent, epsilon=0.95, alpha=0.5, gamma=0.5):
        assert(player.is_q() != opponent.is_q())
        self.QPlayer = player
        self.UPlayer = opponent
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def update_q(self, player, state, action):
        new_state = self.next_state(state, action)

        rsa = self.reward(player, new_state) #reward for current (state, action)
        qsa = player.get_q(state, action)  #current Q-value

        if self.game_over(new_state):
            expected = rsa

        else:
            if player.is_q():
                #if Q-learning agent, choose move with minimum Q value of opponent
                expected = rsa + (self.gamma * min(self.UPlayer.get_q(new_state)))
            else:
                #if opponent agent, choose move with maximum Q value of Q-Learner, and discount
                expected = rsa + (self.gamma * max(self.QPlayer.get_q(new_state)))

        q = qsa + self.alpha * (expected - qsa)
        player.set_q(state, action, q)


    def switch_player(self):
        self.UPlayer.switch_turn()
        self.QPlayer.switch_turn()

        return self.UPlayer if self.UPlayer.is_turn() else self.QPlayer

    #set-up gameplay based on command line arguments
    def setup(self, argv):
        try:
            #set-up random play environment
            if argv[1]=="-r":
                n_trials = int(argv[2])
                #protect against zero-division error for updates
                if n_trials < 20:
                    print("Error: Must be greater than 20 Trials")
                    return False
                self.load_train_stats()
                self.random_play(n_trials, player.RPlayer())
                self.save_train_stats()
                self.save_stats()
            elif argv[1]=="-t":
                n_trials = int(argv[2])
                if n_trials < 20:
                    print("Error: Must be greater than 20 Trials")
                    return False
                self.train(n_trials)
                self.save_train_stats()
                self.save_stats()
            #Load saved Q-Table and set-up free play-environment
            else:
                self.load_train_stats()
            return True

        except IndexError:
            print("Invalid command line arguments:\n\t-t n_trials to train\n\t-r n_trials for random trials\n\t-p to play\n")
            return False

    def save_train_stats(self):
        self.QPlayer.save_qtable()
        self.UPlayer.saveQTable()

    def load_train_stats(self):
        self.QPlayer.load_qtable()
        self.epsilon = 0
