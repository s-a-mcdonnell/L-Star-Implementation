import random

class Teacher:

    # Constructor
    def __init__(self, alphabet, num_nodes = -1, seed = 1821):
        print("teacher created")

        # The teacher will use the provided alphabet
        self.alphabet = alphabet

        # Check the alphabet for validity (each symbol is just one character)
        for symbol in alphabet:
            if len(symbol) != 1:
                print("Error: Invalid alphabet")
                exit(1)

        # Using this guide to PRN generation in Python: https://www.tutorialspoint.com/generate-pseudo-random-numbers-in-python
        random.seed(seed)

        # Determine the number of states in the DFA (between 1 and 100, inclusive)
        # NOTE: The upper limit here is arbitrarily chosen
        # NOTE: Not all of these will be accessible, depending on how the arrows point
        if num_nodes == -1:
            num_nodes = random.randint(1, 100)

        # The DFA (M) is a matrix in which the rows are the nodes
        # The first entry in each row is a boolean in int form (0 or 1) indicating whether the node is an accept (1) or reject (0) state
        # The remaining entries in each row are the numbers of the nodes which the corresponding alphabet value at that index points to
        self.m = []
        
        # Initialize all values in M to -1 (invalid)
        for i in range(num_nodes):
            new_node = []
            self.m.append(new_node)
            for j in range(len(alphabet) + 1):
                self.m[i].append(-1)

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
                node[i] = arrow
                arrows_created += 1
        
        # Print DFA
        for row in self.m:
            print(row)


    # equivalency query
    # takes the DFA hypothesis m_hat
    # returns either a counterexample or False (indicating that the DFAs match)
    def equivalent(self, m_hat):
        if len(self.m[0]) != len(m_hat[0]):
            print("Incompatable alphabet size")
            return True

        # print("equivalency query called")

        # Generate and test an arbitrarily large number of strings
        # for each of these strings, if self.member(s, self.m) is not self.member(s, m_hat), return s

        for i in range(1000000):
            s = self.generate_string()
            if self.member(s) != self.member(s, m_hat, self.alphabet):
                return s            

        # else return false (so that the truthiness of a counterexample and a matching DFA result will be different)
        return False

    # membership query
    # takes a string s and returns a boolean indicating whether s is accepted or rejected by the given DFA
    def member(self, s, dfa: list[list[int]] = None, alpha = None):
        # print("membership query called")

        if not dfa:
            dfa = self.m
        
        if not alpha:
            alpha = self.alphabet

        input = []

        # Convert passed string into an array of ints, where each int is the index in the alphabet array corresponding to that character
        for char in s:
            input.append(alpha.index(char))
        
        # Enter the DFA (M) at node 0
        next_node_index = 0

        # Navigate through the DFA to the final state
        for char_index in input:
            current_node : list[int] = dfa[next_node_index]
            next_node_index = current_node[char_index + 1]
        
        # Return the int boolean indicating if the final state is an accept or reject state
        return bool(dfa[next_node_index][0])

    def generate_string(self):

        strg = ""
            
        # NOTE: The choice of maximum length of a string is arbitrary
        # Create a string of (pseudo-)random length, with each character (pseudo-)randomly chosen from the alphabet
        for i in range(0, random.randint(0, 10)):
            strg += self.alphabet[random.randint(0, len(self.alphabet) - 1)]
        
        return strg