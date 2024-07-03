from learner import Learner
import sys

num_states = -1

if len(sys.argv) > 1:
    num_states = int(sys.argv[1])

seed = 1821

if len(sys.argv) > 2:
    seed = int(sys.argv[2])


alphabet = ['a', 'b']

#dfa_for_testing = [[0, 1, 4], [1, 3, 2], [1, 5, 1], [0, 2, 5], [0, 2, 0], [0, 3, 1]]

# Create learner
# TODO: Change seed to 1821 to see 5-state M_hat be (wrongly) learned from 4-state M
my_learner = Learner(alphabet, num_states = num_states, seed = seed)

# Let learner run
my_learner.lstar_algorithm()