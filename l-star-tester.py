from learner import Learner
import sys

num_states = -1

if len(sys.argv) > 1:
    num_states = int(sys.argv[1])

seed = 1821

if len(sys.argv) > 2:
    seed = int(sys.argv[2])


alphabet = ['0', '1', '2']

# dfa_for_testing = [[0, 0, 1], [0, 1, 2], [0, 2, 3], [1, 3, 0]]

# Create learner
# my_learner = Learner(alphabet, premade_dfa = dfa_for_testing)
my_learner = Learner(alphabet, num_states = num_states, seed = seed)

# Let learner run
my_learner.lstar_algorithm()