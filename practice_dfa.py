from learner import Learner

alphabet = ['a', 'b']

dfa_for_testing = [[0, 1, 4], [1, 3, 2], [1, 0, 1], [0, 2, 1], [0, 2, 0]]

# Initialize learner
my_learner = Learner(alphabet, dfa_for_testing)

print("---")

my_learner.t.print_tree()

print("---")

m_hat = my_learner.construct_hypothesis()

print("---")

print(m_hat)