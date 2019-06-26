"""
Player Class:
Abstract Class for Q-Learning agents, Human Agents agents and Random-Selection
Aggents

by Nina Averill <averill.nina@gmail.com>
"""
from random import random, randint
import qminmax
import pickle
from os import path, mkdir, getcwd

class Player(object):
    def __init__(self, q_player, Q={}):
        self._is_q = q_player
        self.games_won = 0
        self.Q = Q

        if not path.isdir(path.join(getcwd(),"data")):
            mkdir(path.join(getcwd(),"data"))

        qfile = "QPlayer" if q_player else "UPlayer"

        self.file_path = path.join(getcwd(),"data", qfile)

    def is_q(self):
        return self._is_q

    def is_turn(self):
        return self._is_turn

    def set_turn(self, is_turn):
        self._is_turn = is_turn

    def won(self):
        self.games_won += 1

        if self.is_q():
            print("Grandma won")
        else:
            print("User won")

    def get_won(self):
        return self.games_won

    def switch_turn(self):
        self._is_turn = not self._is_turn

    def set_actions(self, n_actions):
        self.n_actions = n_actions

    def save_qtable(self):
        with open(self.file_path, 'wb') as handle:
            pickle.dump(self.Q, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_qtable(self):
        if not path.isfile(self.file_path):
            self.Q = {}
        else:
            with open(self.file_path, 'rb') as handle:
                tmp = pickle.load(handle)

                if  not all(isinstance(i, list) for i in tmp.values()):
                    Q = {}
                else :
                    self.Q = tmp

#Class for Q-Learning agent
class QLearner(Player):
    def __init__(self, q_player, Q={}):
        super(QLearner, self).__init__(q_player, Q)

    def get_q(self, state, action=None):
        if not self.Q.get(state):
            self.Q[state] = [0] * self.n_actions
        if action:
            return self.Q[state][action - 1]
        else:
            return self.Q[state]

    def set_q(self, state, action, q):
        if not self.Q.get(state):
            self.Q[state] = [0] * self.n_actions
        self.Q[state][action - 1] = q

    #probability that random action is chosen encourages exploration of
    #the state/action space
    def choose_action(self, state, game):
        if random() < game.epsilon:
            return randint(1, game.n_actions)
        else:
            return self._minmax_q(state, game.n_actions)

    def _minmax_q(self, state, n_actions):
        if not self.Q.get(state):
            self.Q[state] = [0] * self.n_actions

        if self.is_q():
            q = max(self.Q[state])
        else:
            q = min(self.Q[state])
        #if multiple max/min Q-values, choose an action at random
        action = [i for i in range(n_actions) if self.Q[state][i] == q]

        return action[randint(0, len(action)-1)] + 1

#Class for Human Player
class HPlayer(Player):
    def __init__(self):
        super(HPlayer, self).__init__(False, Q={})

    #prompt Human user for action
    def choose_action(self, state, game):
        action = input("Eat Meatballs: ")

        while not game.valid_move(state, action):
            action = input("Enter a valid number of meatballs: ")
        return int(action)

#Class for Random-Selection algorithm
class RPlayer(Player):
    def __init__(self):
        super(RPlayer, self).__init__(False, Q={})

    def choose_action(self, state, game):
        return randint(1, game.n_actions)
