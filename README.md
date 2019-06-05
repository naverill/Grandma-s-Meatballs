# Grandma's Meatballs

Reinforcement leaning algorithm for the zero-sum, adversarial game Grandma's Meatballs


## Rules
Grandma has made you twenty-one meatballs.

Grandma will get offended if:
1. You don't take any meatballs
2. You take too many meatballs
3. You eat the last meatball

Each side can only take 1, 2 or 3 meatballs per round. The goal is to make  Grandma eat the last meatball. You make the first move.


## Basic Usage*

#### Training
To train the Q-Learning player through reinforcement learning, enter ```python main.py -t n_trials```

Where n_trials is an integer denoting the number of trials to run


#### Random Play
To play a random selection algorithm against the trained algorithm, enter ```python main.py -r n_trials```

Where n_trials is an integer denoting the number of trials to run

#### Free Play

To play Grandma's Meatballs against a trained computer player, enter
```python main.py -p```

**NOTE**
It is recommended that at least one training session is run before random or free play

## Evidence of Solution
My approach involved using the reinforcement algorithm Q-Learning to train the 'Grandma' agent.

To encourage exploration at the beginning of the training phase, I set the epsilon parameter (probability that a random action is chosen) to be `0.95`. As the training progresses, the epsilon value is incrementally reduced by `0.05`  every `n_trials/20` trials to encourage exploitation.

In determining the optimal parameters for the q-learning algorithm, I ran multiple training sessions. In these sessions, I varied parameters such as the number of trials and the learning rate of the algorithm.

#### Varying Number of Trials in Q1 v. Q2 Training Session
This test was done by varying the number of trials for Q-Learning algorithm to run against itself.
[Trials](data/training_data/training.png)
*Image 1: Win Ratio over all Training Sample Sizes*

[TrialsK](data/training_data/trainingK.png)
*Image 2: Win Ratio over Training Sample Sizes [50K, 100K, 500K]*

[TrialsM](data/training_data/trainingM.png)
*Image 3: Win Ratio over Training Sample Sizes [1M, 2M, 10M]*

This indicates that the algorithm requires upwards of 1M training sessions to reach optimal win ratios against an optimal competitor.

#### Varying Learning Rate in Q1 v. Q2 Training Session
This test was done by varying the learning rate of the algorithm of two Q-Learning agents, trained over a session of 1M trials.

[LearningT](data/random_data/training_rate.png)
*Image 4: Win Ratio over various Learning Rates*

This indicates that higher learning rates for the algorithm lead to initially higher win rates. However, this win ratio ultimately declines in the exploitation phase. Moves that initially generate positive returns are unfairly weighted, leading the algorithm to later preference these sub-optimal moves.

#### Varying Learning Rate in Q1 v. Random Selection Training Session
This test was done by varying the learning rate of the algorithm of a q-learning agent against an agent that randomly selected actions, trained over a session of 1M trials.

[LearningR](data/random_data/learning.png)
*Image 5: Win Ratio over various Learning Rates*

This indicates that lower learning rate lead to optimal decision against random-selection agents.

#### Optimal Solution
Therefore, I chose the optimal parameters for the algorithm to be a training session of 10M trials, with parameters `(epsilon, alpha, gamma) = (0.95, 0.4, 0.5)`

## Parameters
*Epsilon*: Probability that Q-Learning agent chooses a move at random

*Alpha*: Learning Rate; Determines the rate at which new Q values

*Gamma*: Discount Factor; Determines the importance of future feedback

#### *Load Previous Training Sessions
To load the Q-tables generated from previous training sessions, copy the files `QPlayer` and `UPlayer` into the `data` directory and then run either random or free play.

Running a training session will overwrite these files.

`training_data` stores Q-Tables generated from training sessions with various numbers of trials

`random_data` stores Q-Tables generated from training sessions with various learning rates

`optimal` stores Q-Tables generated from a training session with optimal parameters

## Credits
Q-Learning implementation written by Nina Averill, based off pseudocode written by Meeden [CS63 Lab 6](https://www.cs.swarthmore.edu/~meeden/cs63/f11/lab6.php)
