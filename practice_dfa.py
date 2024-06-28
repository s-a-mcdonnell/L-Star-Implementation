from teacher import Teacher
import random

# The teacher will use the provided alphabet
alphabet = ['0','1']

# Using this guide to PRN generation in Python: https://www.tutorialspoint.com/generate-pseudo-random-numbers-in-python
# Arbitarily chosen seed for the PRNG
random.seed(1820)

num_nodes = 3

# The DFA (M) is a matrix in which the rows are the nodes
# The first entry in each row is a boolean in int form (0 or 1) indicating whether the node is an accept (1) or reject (0) state
# The remaining entries in each row are the numbers of the nodes which the corresponding alphabet value at that index points to
dfa = []

# Initialize all values in M to -1 (invalid)
for i in range(num_nodes):
    new_node = []
    dfa.append(new_node)
    for j in range(len(alphabet) + 1):
        dfa[i].append(-1)

print("num_nodes = " + str(num_nodes))
print("alphabet size = " + str(len(alphabet)))
print("M has " + str(len(dfa)) + " rows and " + str(len(dfa[0])) + " columns")

arrows_created = 0
accept_states = 0
reject_states = 0
# Set each arrow in each node to point at a random node
for node in dfa:
    # The first entry in each node is a boolean indicating whether the node is an accept or reject state
    node[0] = random.randint(0, 1)
    if node[0]:
        accept_states += 1
    else:
        reject_states += 1

    # The subsequent entries indicate which node a given alphabet value directs to
    for i in range(1, len(node)):
        arrow = random.randint(0, num_nodes - 1)
        node[i] = arrow
        arrows_created += 1

print("arrows created: " + str(arrows_created))
print("accept states created: " + str(accept_states))
print("reject states created: " + str(reject_states))

print("Complete DFA:")
for node in dfa:
    print(node)


print("00110 is accepted: " + str(Teacher.member("00110", dfa, alphabet)))



