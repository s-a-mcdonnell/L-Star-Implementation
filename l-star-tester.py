from learner import Learner

alphabet = ['a', 'b']

dfa_for_testing = [[0, 1, 4], [1, 3, 2], [1, 0, 1], [0, 2, 1], [0, 2, 0]]

# Create learner
my_learner = Learner(alphabet, dfa_for_testing)

# Let learner run
my_learner.lstar_algorithm()