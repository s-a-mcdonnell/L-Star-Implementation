An implementation of Dana Angluin's L* Algorithm for exactly learning DFAs in polynomial time as explained in Chapter 8: "Learning Finite Automata by Experimentation" in "An Introduction to Computational Learning Theory" by Micheal J. Kearns and Umesh V. Vazirani.

The DFA to be learned can be provided in the form of a text file (dfa.txt) or generated using a pseudo-random number generator. DFAs provided as a text file take the following format:
Each row represents a node in the DFA.
The first entry in each row is a boolean value indicating whether the row represents an accept (1) or reject (0) state.
The subsequent entries in each row indicate which node each character in the alphabet transitions to, where the value stores represents the row at which information about that node is stored. Transition states are stored in the order corresponding to the order in which characters were entered into the alphabet (the order of characters in alphabet.txt, or, if the default alphabet is used, 0 followed by 1).

The alphabet provided in the file alphabet.txt can be of any size, with each row in alphabet.txt containing one character. If no alphabet is provided, the default alphabet is binary (0 and 1). For ease of reading the learned DFA, it is recommended to order the characters in the alphabet in an intuitive manner (eg. a hexademical alphabet would be ordered 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, a, b, c, d, e, f), but this decision is left to the user.

Python libraries required:
matplotlib, 
networkx
