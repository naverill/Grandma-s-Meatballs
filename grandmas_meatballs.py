"""
Grandma's Meatballs Class:
Wrapper Class Grandma's Meatballs gameplay.
Contains Training, Random Play and Free Play environments.

by Nina Averill <averill.nina@gmail.com>
"""
from qminmax import QMinMaxGame
from os import path, getcwd
import player

init = "---------------------"

class GrandmasMeatballs(QMinMaxGame):
    def __init__(self, grandma, user, epsilon=0.95, alpha=0.5, gamma=0.5):
        self.n_states = 21
        self.n_actions = 3
        self.stats = [["Trial", "Games Won", "Ratio"]]
        self.meatballs = init
        super(GrandmasMeatballs, self).__init__(grandma, user, epsilon, alpha, gamma)

    #Reinforcement Learning for two Q-Learning agents
    def train(self, n_trials):
        state = self._init_players()
        trial = 1
        n_updates = n_trials//20 #rate at which game statistics are updated

        while trial <= n_trials:
            print("Trial #" + str(trial))
            if trial % n_updates == 0:
                self.update_stats(trial)
                #decrease randomness of actions
                if self.epsilon >= 0.05:
                    self.epsilon -= 0.05
                else:
                    self.epsilon = 0.0

            player = self.UPlayer #user starts round

            while not self.game_over(state):
                action = player.choose_action(state, self)

                self.render(player, state, action)

                self.update_q(player, state, action)

                player = self.switch_player()

                state = self.next_state(state, action)

            player.won()
            state = self.reset()
            trial += 1

        self.save_train_stats()

    #Play for Q-Learning Agent vs. Randon-Selection Algorithm
    def random_play(self, n_trials, rplayer):
        trial = 1
        n_updates = n_trials//20
        self.UPlayer = rplayer
        state = self._init_players()

        while trial <= n_trials:

            if trial % n_updates == 0:
                self.update_stats(trial)

            player = self.UPlayer

            while not self.game_over(state):
                action = player.choose_action(state, self)

                self.render(player, state, action)

                player = self.switch_player()

                state = self.next_state(state, action)

            player.won()
            state = self.reset()
            trial += 1

    #Q-Learning Algorithm vs. Human Player
    def start_game(self, grandma, user):
        self.UPlayer = user;
        state = self._init_players()
        player = user; #user starts round

        while not self.game_over(state):
            action = player.choose_action(state, self)

            self.render(player, state, action)

            player = self.switch_player()

            state = self.next_state(state, action)
        player.won()
        state = self.reset()

    def next_state(self, state, action):
        return state + action

    def reward(self, player, state):
        if state > 21:
            r = -2
        if state == 20:
            r = 1.0
        elif state == 21:
            r = -1
        else:
            r = 0.0

        if player.is_q():
            return r
        else:
            return -r

    def game_over(self, state):
        return state >= self.n_states

    def valid_move(self, state, action):
        try:
            action = int(action)

            if action < 0:
                print("? No.")
                return False

            elif action == 0:
                print("Don't offend your Grandma. Take a meatball.")
                return False

            elif not action <= self.n_actions:
                print("Greedy. Too many meatballs.")
                return False

            elif state + action > self.n_states:
                print("Greedy. Not enough meatballs left.")
                return False

            return True
        except ValueError:
            print("Invalid move: not an integer.")
            return False

    def _init_players(self):
        self.reset_players()
        self.UPlayer.set_actions(self.n_actions)
        self.QPlayer.set_actions(self.n_actions)

        #Load Q-Table for Random-Selection Algorithm and Human-Player
        if isinstance(self.UPlayer, player.RPlayer) or isinstance(self.UPlayer, player.HPlayer):
            self.UPlayer.load_qtable()
        return 0

    def reset(self):
        print("\n")
        self.meatballs = init
        self.reset_players()
        return 0

    #render game play in terminal
    def render(self, player, state, action):
        mark = "G" if player.is_q() else "U"
        self.meatballs = self.meatballs[:state] + mark * action + self.meatballs[state + action:]
        print(self.meatballs)

    def reset_players(self):
        self.UPlayer.set_turn(True)
        self.QPlayer.set_turn(False)

    def update_stats(self, trials):
        self.stats.append([str(trials), str(self.QPlayer.getWon()), str(float(self.QPlayer.getWon())/float(trials))])

    def save_stats(self):
        fpath = path.join(getcwd(),"data")
        if not path.isdir(fpath):
            mkdir(fpath)

        #save statistics in different files depending on if algorithm
        #is in training mode or random play mode
        fname = "train_stats.csv" if isinstance(self.UPlayer, player.QLearner) else "random_stats.csv"

        #save game statistics
        with open(path.join(fpath, fname), "w+") as handle:
            for row in self.stats:
                line = ",".join(row)
                handle.write(line)
                handle.write("\n")
        handle.close()

        #save Q-Learning parameters
        with open(path.join(fpath, "parameters.csv"), "w+") as handle:
            handle.write(",".join(["epsilon","alpha","gamma"]) + "\n")
            handle.write(",".join([str(self.epsilon), str(self.alpha), str(self.gamma)]))
        handle.close()
