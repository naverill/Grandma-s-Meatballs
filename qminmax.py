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
        assert(player.isQ() != opponent.isQ())
        self.QPlayer = player
        self.UPlayer = opponent
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def updateQ(self, player, state, action):
        new_state = self.nextState(state, action)

        rsa = self.reward(player, new_state) #reward for current (state, action)
        qsa = player.getQ(state, action)  #current Q-value

        if self.gameOver(new_state):
            expected = rsa

        else:
            if player.isQ():
                #if Q-learning agent, choose move with minimum Q value of opponent
                expected = rsa + (self.gamma * min(self.UPlayer.getQ(new_state)))
            else:
                #if opponent agent, choose move with maximum Q value of Q-Learner, and discount
                expected = rsa + (self.gamma * max(self.QPlayer.getQ(new_state)))

        q = qsa + self.alpha * (expected - qsa)
        player.setQ(state, action, q)


    def switchPlayer(self):
        self.UPlayer.switchTurn()
        self.QPlayer.switchTurn()

        return self.UPlayer if self.UPlayer.isTurn() else self.QPlayer

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
                self.loadTrainStats()
                self.randomPlay(n_trials, player.RPlayer())
                self.saveTrainStats()
                self.saveStats()
            elif argv[1]=="-t":
                n_trials = int(argv[2])
                if n_trials < 20:
                    print("Error: Must be greater than 20 Trials")
                    return False
                self.train(n_trials)
                self.saveTrainStats()
                self.saveStats()
            #Load saved Q-Table and set-up free play-environment
            else:
                self.loadTrainStats()
            return True

        except IndexError:
            print("Invalid command line arguments:\n\t-t n_trials to train\n\t-r n_trials for random trials\n\t-p to play\n")
            return False

    def saveTrainStats(self):
        self.QPlayer.saveQTable()
        self.UPlayer.saveQTable()

    def loadTrainStats(self):
        self.QPlayer.loadQTable()
        self.epsilon = 0
