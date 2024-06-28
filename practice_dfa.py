############################################################################

# Checks teacher and passed DFA for equivalency and prints the result
def compare_dfas(teacher, dfa_to_compare):
    counterexample = teacher.equivalent(dfa_to_compare)
    if counterexample:
        print("Counterexample: " + counterexample)
    else:
        print("DFAs are equivalent")

############################################################################

from teacher import Teacher
import random

# The teacher will use the provided alphabet
alphabet = ['0','1']

my_teacher = Teacher(alphabet, num_nodes = 5, seed = 1821)

# My DFA always accepts
my_dfa = [[1, 0, 0]]

compare_dfas(my_teacher, my_dfa)

print("-----")

# My other DFA always rejects

my_dfa_2 = [[0,0,0]]

compare_dfas(my_teacher, my_dfa_2)

print("-----")


my_teacher_2 = Teacher(alphabet, num_nodes = 4, seed = 1821)
compare_dfas(my_teacher_2, my_dfa)




