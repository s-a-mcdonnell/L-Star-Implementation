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
        # and the entries in each row are the numbers of the nodes which the alphabet value at that index points to
        self.m = [[-1]*len(alphabet)]*num_nodes
        
        print("num_nodes = " + str(num_nodes))
        print("alphabet size = " + str(len(alphabet)))
        print("M has " + str(len(self.m)) + " rows and " + str(len(self.m[0])) + " columns")

        pass


    # equivalency query
    def equivalent(self, m_hat):
        pass

    # membership query
    def member(self, s):
        pass