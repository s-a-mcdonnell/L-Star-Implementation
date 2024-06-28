from teacher import Teacher
import random

# The teacher will use the provided alphabet
alphabet = ['0','1']

my_teacher = Teacher(alphabet, num_nodes = 4)

print("Complete DFA:")
for node in my_teacher.m:
    print(node)


print("01 is accepted: " + str(Teacher.member("01", my_teacher.m, alphabet)))
print("10 is accepted: " + str(Teacher.member("10", my_teacher.m, alphabet)))




