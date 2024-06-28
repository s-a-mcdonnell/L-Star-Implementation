############################################################################

# Checks teacher and passed DFA for equivalency and prints the result
def compare_dfas(teacher, dfa_to_compare):
    counterexample = teacher.equivalent(dfa_to_compare)
    if counterexample:
        print("Counterexample: " + counterexample)
    else:
        print("DFAs are equivalent")

############################################################################
# Checks and prints membership info for the passed string
def check_membership(s):
    s = str(s)
    print("Is " + (s if s else "the empty string") + " a member? " + str(my_learner.my_teacher.member(s)))

############################################################################


from learner import Learner
from learner import Node

# The teacher will use the provided alphabet
'''# NOTE: The alphabet can only contain single-character characters
alphabet = ['a', 'b', 'c', '1', '2', '3']

my_teacher = Teacher(alphabet, num_nodes = 5, seed = 1821)

# My DFA always accepts
my_dfa = []
my_dfa.append([])
my_dfa[0].append(1)
for character in alphabet:
    my_dfa[0].append(0)

my_dfa_2 = []
my_dfa_2.append([])
my_dfa_2[0].append(0)
for character in alphabet:
    my_dfa_2[0].append(0)

compare_dfas(my_teacher, my_dfa_2)

print("-----")


my_teacher_2 = Teacher(alphabet, num_nodes = 4, seed = 1821)
compare_dfas(my_teacher_2, my_dfa)'''

alphabet = ['0', '1']

my_learner = Learner(alphabet)

# my_learner.t.root = Node("", None)

# my_learner.t.root.left_child = Node("left", my_learner.t.root)

# my_learner.t.root.right_child = Node("right", my_learner.t.root)

print("left child exists: " + str(bool(my_learner.t.root.left_child)))

print("right child exists: " + str(bool(my_learner.t.root.right_child)))

my_learner.t.print_tree()

print(my_learner.m_hat)

hypothesis = my_learner.construct_hypothesis()

print(hypothesis)


check_membership("")
check_membership(0)
check_membership(1)
check_membership(11111001)
check_membership(111110010)
check_membership(111110011)
