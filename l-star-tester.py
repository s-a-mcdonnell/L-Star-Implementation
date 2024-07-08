from learner import Learner
import sys
import os

##########################################################################################################

# Reads chars from the alphabet file and returns list storing alphabet
def __read_alphabet(loc):

    # Default alphabet is 0 and 1
    try:
        alpha_file = open(os.path.join(loc, "alphabet.txt"), "r")
    except:
        return ['0', '1']
    
    alpha = []

    for line in alpha_file:
        # Check type and length of character in alphabet
        assert type(line) is str
        assert (len(line) == 1) or (len(line) == 2)
        if len(line) == 2:
            assert line[1] == '\n'

        # Add character to alphabet
        alpha.append(line[0])
    
    return alpha

##########################################################################################################

# Reads lines from the DFA file and returns matrix (2d list) storing DFA
def __read_dfa(loc):
    # Return None if no file is provided
    try:
        dfa_file = open(os.path.join(loc, "dfa.txt"), "r")
    except:
        return None
    
    dfa = []

    for line in dfa_file:

        # Parsing the text file
        line_parts = line.split(" ")
        print(f"line_parts: {line_parts}")

        to_append = []

        # Save each int in the text file to the to_append list for that row
        for num in line_parts:
            to_append.append(int(num))


        # Check that each list row of the DFA is the length of the alphabet plus 1
        print(f"to_append: {to_append}")
        assert len(to_append) == len(alphabet) + 1
        
        # Append row to DFA
        dfa.append(to_append)
    
    # Return parsed DFA
    return dfa

##########################################################################################################

num_states = -1

if len(sys.argv) > 1:
    num_states = int(sys.argv[1])

seed = 1821

if len(sys.argv) > 2:
    seed = int(sys.argv[2])

# Import alphabet from text file (if provided, else use binary alphabet)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
alphabet = __read_alphabet(__location__)
print(f"alphabet: {alphabet}")

# Read DFA from text file (if provided)
dfa_for_testing = __read_dfa(__location__)



# Create learner

# If a DFA was provided, use it
if dfa_for_testing:
    my_learner = Learner(alphabet, premade_dfa = dfa_for_testing)

# Else if command-line arguments are provided, pass them to the learner
# TODO: Enable command-line arguments specifying if graphs should be shown
elif len(sys.argv):
    my_learner = Learner(alphabet, num_states = num_states, seed = seed)

# Else allow the DFA to be randomly generated
else:
    my_learner = Learner(alphabet=alphabet)


# Let learner run
my_learner.lstar_algorithm()