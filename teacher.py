import random
import functools
import collections.abc

class memoized(object):
    '''Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    '''

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.abc.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value
        
    def __repr__(self):
        '''Return the function's docstring.'''
        return self.func.__doc__
    
    def __get__(self, obj, objtype):
        '''Support instance methods.'''
        return functools.partial(self.__call__, obj)
    
def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer

##############################################################################################################

class Teacher:

    ##########################################################################################################

    # Constructor
    def __init__(self, alphabet, num_states = -1, seed = 1821, premade_dfa = None):

        # The teacher will use the provided alphabet
        self.alphabet = alphabet

        # Check the alphabet for validity (each symbol is just one character)
        for symbol in alphabet:
            if len(symbol) != 1:
                print("Error: Invalid alphabet")
                exit(1)

        # Using this guide to PRN generation in Python: https://www.tutorialspoint.com/generate-pseudo-random-numbers-in-python
        random.seed(seed)
        
        # If a premade DFA was provided, use it
        if premade_dfa:
            self.m = premade_dfa

        # Else, create a DFA
        else:
            # Determine the number of states in the DFA (between 1 and 100, inclusive)
            # NOTE: The upper limit here is arbitrarily chosen
            # NOTE: Not all of these will be accessible, depending on how the arrows point
            if num_states == -1:
                num_states = random.randint(1, 100)

            # The DFA (M) is a matrix in which the rows are the states
            # The first entry in each row is a boolean in int form (0 or 1) indicating whether the state is an accept (1) or reject (0) state
            # The remaining entries in each row are the numbers of the states which the corresponding alphabet value at that index points to
            self.m = []
            
            # Initialize all values in M to -1 (invalid)
            for i in range(num_states):
                new_state = []
                self.m.append(new_state)
                for j in range(len(alphabet) + 1):
                    self.m[i].append(-1)

            arrows_created = 0
            accept_states = 0
            reject_states = 0
            # Set each arrow in each state to point at a random state
            for state in self.m:
                # The first entry in each state is a boolean indicating whether it is an accept or reject state
                state[0] = random.randint(0, 1)
                if state[0]:
                    accept_states += 1
                else:
                    reject_states += 1

                # The subsequent entries indicate which state a given alphabet value directs to
                for i in range(1, len(state)):
                    arrow = random.randint(0, num_states - 1)
                    state[i] = arrow
                    arrows_created += 1
            
            '''# Print DFA
            print("DFA to learn:")
            print(self.m)'''

    ##########################################################################################################

    # equivalency query
    # takes the DFA hypothesis m_hat
    # returns either a counterexample or False (indicating that the DFAs match)
    def equivalent(self, m_hat):
        assert m_hat
        if len(self.m[0]) != len(m_hat[0]):
            print("Error: Incompatable alphabet size")
            return True

        # Generate and test an arbitrarily large number of strings
        # for each of these strings, if self.member(s, self.m) is not self.member(s, m_hat), return s

        for i in range(1000000):
            s = self.generate_string()
            if self.member(s) != self.member(s, m_hat):
                assert(type(self.member(s)) is bool)
                assert(type(self.member(s, m_hat)) is bool)
    
                return s            

        # else return false (so that the truthiness of a counterexample and a matching DFA result will be different)
        return False

    ##########################################################################################################
    
    @staticmethod
    def final_state(s : str, dfa: list[list[int]], alpha):

        input = []

        assert (type(s) is str)

        # Convert passed string into an array of ints, where each int is the index in the alphabet array corresponding to that character
        for char in s:
            input.append(alpha.index(char))
        
        # Enter the DFA (M) at state 0
        next_state_index = 0

        # Navigate through the DFA to the final state
        for char_index in input:
            current_state = dfa[next_state_index]
            next_state_index = current_state[char_index + 1]
        
        # Return final state
        return dfa[next_state_index]
        
    ##########################################################################################################

    # membership query
    # takes a string s and returns a boolean indicating whether s is accepted or rejected by the given DFA
    @memoize
    def member(self, s : str, dfa: list[list[int]] = None, alpha = None):

        if not dfa:
            dfa = self.m
        
        if not alpha:
            alpha = self.alphabet

        # Return the int boolean indicating if the final state is an accept or reject state
        final_state : list[int] = Teacher.final_state(s, dfa, alpha)
        return bool(final_state[0])

    ##########################################################################################################

    def generate_string(self):

        strg = ""
            
        # NOTE: The choice of maximum length of a string is arbitrary
        # Create a string of (pseudo-)random length, with each character (pseudo-)randomly chosen from the alphabet
        for i in range(0, random.randint(0, 15)):
            strg += self.alphabet[random.randint(0, len(self.alphabet) - 1)]
        
        return strg

    ##########################################################################################################

##############################################################################################################