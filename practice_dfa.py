from learner import Learner

alphabet = ['a', 'b']

dfa_for_testing = [[0, 1, 4], [1, 3, 2], [1, 0, 1], [0, 2, 1], [0, 2, 0]]

# Initialize learner
my_learner = Learner(alphabet, dfa_for_testing)

for i in range(2):

    print("---")

    my_learner.t.print_tree()

    print("---")

    my_learner.m_hat = my_learner.construct_hypothesis()

    print(my_learner.m_hat)

    print("---")

    my_learner.update_tree(my_learner.my_teacher.equivalent(my_learner.m_hat))