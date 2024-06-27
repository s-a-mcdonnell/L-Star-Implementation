from teacher import Teacher
import random

random.seed(1)

alphabet = [0, 1]
num_nodes = 4

dfa = []

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
for i in range(len(dfa)):
    node = dfa[i]

    # The first entry in each node is a boolean indicating whether the node is an accept or reject state
    node[0] = random.randint(0, 1)
    if node[0]:
        accept_states += 1
        print("accept state created")
    else:
        reject_states += 1
        print("reject state created")


    # The subsequent entries indicate which node a given alphabet value directs to
    for i in range(1, len(node)):
        arrow = random.randint(0, num_nodes - 1)
        print("arrow with value " + str(arrow) + " created")
        node[i] = arrow
        arrows_created += 1

    print("completed node: " + str(node))
    print("completed dfa row: " + str(dfa[dfa.index(node)]))
    print("dfa so far: " + str(dfa))



print("arrows created: " + str(arrows_created))
print("accept states created: " + str(accept_states))
print("reject states created: " + str(reject_states))

'''for node in dfa:
    print(node)'''
print(dfa[0])
print(dfa[1])
print(dfa[2])
print(dfa[3])