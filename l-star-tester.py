from learner import Learner

alphabet = ['a', 'b']

dfa_for_testing = [[0, 1, 4], [1, 3, 2], [1, 5, 1], [0, 2, 5], [0, 2, 0], [0, 3, 1]]
my_learner = Learner(premade_dfa=dfa_for_testing)

# Create learner
# TODO: Change seed to 1821 to see 5-state M_hat be (wrongly) learned from 4-state M
# my_learner = Learner(alphabet, num_states = 4, seed = 1823)

# Let learner run
my_learner.lstar_algorithm()