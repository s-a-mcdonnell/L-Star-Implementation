from teacher import Teacher
import random

# The teacher will use the provided alphabet
alphabet = ['0','1']

my_teacher = Teacher(alphabet, num_nodes = 5)

print("Complete DFA:")
for node in my_teacher.m:
    print(node)


print("01 is accepted: " + str(Teacher.member("01", my_teacher.m, alphabet)))
print("10 is accepted: " + str(Teacher.member("10", my_teacher.m, alphabet)))

my_dfa = [1, 0, 0]

counterexample_found = my_teacher.equivalent(my_dfa)
print("equivalent DFAs: " + str(not counterexample_found))

my_teacher_2 = Teacher(alphabet, num_nodes = 4)
counterexample_found_2 = my_teacher_2.equivalent(my_dfa)
print("equivalent DFAs (#2): " + str(not counterexample_found_2))




