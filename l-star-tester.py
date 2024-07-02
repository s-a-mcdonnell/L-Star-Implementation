from learner import Learner

alphabet = ['a', 'b', 'c', 'd']

dfa_for_testing = [[0, 1, 4], [1, 3, 2], [1, 5, 1], [0, 2, 5], [0, 2, 0], [0, 3, 1]]

# Create learner
my_learner = Learner(alphabet, num_states = 6)

# Let learner run
my_learner.lstar_algorithm()