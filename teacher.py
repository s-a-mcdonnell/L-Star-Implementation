import random

class Teacher:

    # Constructor
    def __init__(self, alphabet):
        print("teacher created")

        # The teacher will use the provided alphabet
        self.alphabet = alphabet

        # Using this guide to PRN generation in Python: https://www.tutorialspoint.com/generate-pseudo-random-numbers-in-python
        # Arbitarily chosen seed for the PRNG
        random.seed(1821)

        # Determine the number of states in the DFA (between 1 and 100, inclusive)
        # NOTE: The upper limit here is arbitrarily chosed
        num_nodes = random.randint(1, 100)

        # The DFA (M) is a matrix in which the rows are the nodes
        # The first entry in each row is a boolean in int form (0 or 1) indicating whether the node is an accept (1) or reject (0) state
        # The remaining entries in each row are the numbers of the nodes which the corresponding alphabet value at that index points to
        self.m = [[-1]*(len(alphabet)+1)]*num_nodes
        
        print("num_nodes = " + str(num_nodes))
        print("alphabet size = " + str(len(alphabet)))
        print("M has " + str(len(self.m)) + " rows and " + str(len(self.m[0])) + " columns")
        
        arrows_created = 0
        accept_states = 0
        reject_states = 0
        # Set each arrow in each node to point at a random node
        for node in self.m:
            # The first entry in each node is a boolean indicating whether the node is an accept or reject state
            node[0] = random.randint(0, 1)
            if node[0]:
                accept_states += 1
            else:
                reject_states += 1

            # The subsequent entries indicate which node a given alphabet value directs to
            for i in range(1, len(node)):
                arrow = random.randint(0, num_nodes - 1)
                arrows_created += 1

        print("arrows created: " + str(arrows_created))
        print("accept states created: " + str(accept_states))
        print("reject states created: " + str(reject_states))

    # equivalency query
    def equivalent(self, m_hat):
        pass

    # membership query
    def member(self, s):
        pass