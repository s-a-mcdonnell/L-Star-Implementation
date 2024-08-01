from teacher import Teacher

import itertools as it
import matplotlib.pyplot as plt
import networkx as nx

import functools

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

class Learner:

    ##########################################################################################################

    def draw_graph(self):
        '''
        Draws current, a graph representing the current DFA M_Hat using Networkx.   
        Graphs are set off to default but can be enabled with a command line prompt when running any of the testing files
        '''

        # turn the m_hat array into the graph (add appropriate nodes and edges based on table)
        m_graph = nx.MultiDiGraph(directed = True)

        accepting = []

        for row in self.m_hat:
            # create node with label from the index, and add it to the list of accepted nodes if row[0] is 1

            access_string = next(key for key in self.access_string_reference.keys() if self.access_string_reference[key] == self.m_hat.index(row))

            m_graph.add_node(self.m_hat.index(row), data=access_string)
            if row[0] == 1:
                accepting.append(self.m_hat.index(row))

            # edge from node "row index" to node "row[i]" where it is labelled by the character in language[i]
            for i in range(1, len(row)):
                m_graph.add_edge(self.m_hat.index(row), row[i], key = self.alphabet[i - 1], data = self.alphabet[i-1])

        # draw the graph

        colors_node = []
        for node in m_graph:
            if node in accepting:
                colors_node.append('green')
            else:
                colors_node.append('red')

        labels_node = {n : data["data"] for n, data in m_graph.nodes(data = True)}

        labels = {(u, v, key): data["data"] for u, v, key, data in m_graph.edges(keys = True, data = True)}

        pos = nx.shell_layout(m_graph)
        connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
        # ^^^ from this multigraph tutorial https://networkx.org/documentation/stable/auto_examples/drawing/plot_multigraphs.html
        
        nx.draw_networkx_nodes(m_graph, pos, node_color=colors_node)
        nx.draw_networkx_labels(m_graph, pos, labels_node, font_size=10)

        nx.draw_networkx_edges(m_graph, pos, edge_color="grey", connectionstyle=connectionstyle)
        nx.draw_networkx_edge_labels(m_graph, pos, labels, label_pos=0.25, font_size = 10, font_color="black", connectionstyle=connectionstyle, bbox={"alpha": 0})

        plt.show()
    
    ##########################################################################################################

    def __init__(self, alphabet = ['0','1'], num_states = -1, seed = -1, premade_dfa = None, display_graphs = False):
        '''
        Initializes the learner
        :param alphabet: the alphabet the DFA is using (defaults to binary) (assumed to be in List form otherwise)
        :param num_states: number of states to be created in a randomly generated DFA for the teacher
        :param seed: seed to be used for a randomly generated teacher DFA if applicable
        :param premade_dfa: the premade Teacher DFA if applicable
        :param display_graphs: boolean value for if graphs should be drawn of M_Hat as the program progresses
        '''

        self.solved = False
        # Intialize alphabet
        self.alphabet = alphabet

        # Whether or not to draw the graphs
        self.graphs = display_graphs

        # Note that the alphabet must contains characters (strings of length one), not longer strings or ints
        for character in alphabet:
            assert type(character) is str
            assert len(character) == 1
        

        # Initialize teacher

        # If a premade DFA was provided (for testing), use it
        if premade_dfa:
            assert len(premade_dfa[0]) == len(alphabet) + 1

            self.my_teacher = Teacher(self.alphabet, premade_dfa = premade_dfa)

        
        # Else the DFA to be learned will be constructed by the teacher
        else:
            self.my_teacher = Teacher(self.alphabet, num_states = num_states, seed = seed)

        # Initialize binary classifcation tree T and tentative hypothesis M_hat
        self.init_t_m_hat()

        # Confirm that all -1s with which M_hat was initialized have been overwritten
        for row in self.m_hat:
            for entry in row:
                assert entry >= 0
        
    ##########################################################################################################

    def init_t_m_hat(self):
        '''
        Initialize the Tree T and the initial M_Hat with the empty initial string and one other state.
        Helper method for constructor __init__.
        '''

        # initialize T with just the empty string (lambda)
        self.t = Tree(Node("", None, 0))

        # create M_hat with just one state in T
        # The DFA (M) is a matrix in which the rows are the nodes
        # The first entry in each row is a boolean in int form (0 or 1) indicating whether the node is an accept (1) or reject (0) state
        # The remaining entries in each row are the numbers of the nodes which the corresponding alphabet value at that index points to
        self.m_hat = []

        # dictionary for storing access strings as keys corresponding to their rows in the m_hat matrix
        # add to the dictionary when updating the tree, not when reconstructing m_hat, because we need dict to construct m_hat
        self.access_string_reference = {}
        self.update_dictionary("", 0)

        # Create the first state (with the empty access string)
        # check whether empty string is accepted or rejected
        to_append = []
        if self.my_teacher.member(""):
            # empty string accepted
            to_append.append(1)
        else:
            to_append.append(0)
        
        # This initial state points only to itself
        for i in range(len(self.alphabet)):
            to_append.append(0)

        # Append the first state to M_hat        
        self.m_hat.append(to_append)


        # draw m_hat graph here, as m_hat is not updated in initialization past this point
        if self.graphs:
            self.draw_graph()
    
        # equivalence query on initial M_hat
        gamma = self.my_teacher.equivalent(self.m_hat)

        # If there is no counterexample, we have solved the DFA
        if not gamma:
            self.solved = True
        
        # Else put counterexample gamma into our tree T
        else:

            assert type(gamma) is str

            assert(self.my_teacher.member(gamma) != self.my_teacher.member(gamma, self.m_hat, self.alphabet))


            if self.my_teacher.member(gamma):
                self.t.root.right_child = Node(gamma, self.t.root, 1)
                self.t.root.left_child = Node("", self.t.root, 1)
            else:
                # counterexample is rejected
                self.t.root.right_child = Node("", self.t.root, 1)
                self.t.root.left_child = Node(gamma, self.t.root, 1)
            
            # Add counterexample to the dictionary
            self.update_dictionary(gamma, 1)

    ##########################################################################################################

    def update_dictionary(self, key : str, index : int):
        '''
        updates the variable access_string_reference (dictionary) with the given values
        :param key: the key in the key,value pair being added to the dictionary
        :param index: the value in the key value pair, which represnts the index in the matrix of the acess string being added
        '''
        
        # assert (not key in self.access_string_reference.keys()) 

        # Print debugging information if trying to clobber a pre-existing key:
        if key in self.access_string_reference.keys():
            print("Error: Trying to clobber key " + key)
            self.__sift(key, self.t)
            exit(1)

        self.access_string_reference.update({key : index})

    ##########################################################################################################

    def lstar_algorithm(self):
        '''runs Anlguin's L-Star algorithm and prints the learned DFA and its tree upon completion'''

        print("Running L*")

        while not self.solved:
            # create new M_hat from current T => call construct_hypothesis
            self.m_hat = self.construct_hypothesis()            

            if self.graphs:
                self.draw_graph()
            
            # equivalence query => does our current M_hat equal the real M from teacher?
            gamma = self.my_teacher.equivalent(self.m_hat)

            if gamma:
                # if a counterexample is provided, update T by determining the new access string and distinguishing string (sift down)
                assert(self.my_teacher.member(gamma) != self.my_teacher.member(gamma, self.m_hat, self.alphabet))

                assert type(gamma) is str

                # call update_tree (includes updating dictionary)
                self.update_tree(gamma)

            else:
                # If no counterexample is provided, the DFA has been solved
                self.solved = True

        # If we have exited the loop, we have solved the DFA
        # if yes we are done
        print("DFA solved!")
        print(f"Learned DFA with {len(self.m_hat)} states:")
        print(self.m_hat)
        print("with tree:")
        self.t.print_tree()
        
        print("End L-Star algorithm")

        return self.m_hat

    ##########################################################################################################

    def __get_lca(self, s1 , s2):
        '''
        returns the distinguishing string corresponding to the last (most recent) common ancestor of the access strings s1 and s2 in tree T
        :param s1: access string 1
        :param s2: access string 2
        '''

        assert s1 != s2
        assert s1 in self.access_string_reference.keys()
        assert s2 in self.access_string_reference.keys()

        # Get the tree nodes corresponding to the two passed access strings
        # NOTE: We could also have passed n1 instead of s1 to this method, but we would need to sift for s2 (which comes from M_hat) regardless
        # NOTE: since these are guaranteed access strings, we can just outright use the memoize version of the function

        n1 = memoize(self.__sift_return_node(s1, self.t))
        n2 = memoize(self.__sift_return_node(s2, self.t))

        assert n1 != n2

        # Travel up the tree until you've found the point in n1 and n2's family trees when they are on the same level
        while n1.level > n2.level:
            n1 = n1.parent
        

        while n2.level > n1.level:
            n2 = n2.parent
        
        assert n1 and n2
        assert n1.level == n2.level

        # Travel up the family trees until you are looking at the same node via both paths
        while n1 != n2:
            n1 = n1.parent
            n2 = n2.parent

            assert n1 and n2
        
        # Confirm that we have found a common ancestor
        assert n1 == n2

        # Return the distinguishing string assosciated with the LCA
        return n1.value
    
    ##########################################################################################################

    def update_tree(self, gamma):
        '''
        takes in a counterexaple and edits the Classification Tree T to update it with the new string and sift all other affected strings
        NOTE: does not return the tree but updates it within the method
        :param gamma: new counterexample provided by equivalence query that needs to be sifted down the tree
        '''

        # Assert that gamma really is a counterexample
        assert bool(self.my_teacher.member(gamma)) != bool(self.my_teacher.member(gamma, self.m_hat, self.alphabet))


        j = 0
        # for each prefix set of characters of gamma
        for i in range(len(gamma)):
            j = i

            # Get the first i characters of gamma
            strng = gamma[0 : i + 1]
            # sift gamma[i] in T
            if strng in self.access_string_reference.keys():
                node_sift = memoize(self.__sift_return_node(strng, self.t))
            else:
                node_sift = self.__sift_return_node(strng, self.t)
            access_string_sift = node_sift.value

            loop_d = node_sift.parent.value if node_sift.parent else ""

            # Accessing dictionary key from value according to these instructions: https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/#
            row_in_m_hat = self.m_hat.index(Teacher.final_state(strng, self.m_hat, self.alphabet))
            my_dict = self.access_string_reference
            access_string_m_hat = list(my_dict.keys())[list(my_dict.values()).index(row_in_m_hat)]
            
            # Repeat loop until sifting and running the truncated string through M_hat lead to distinct states (different access strings/row indices in M_hat)
            if access_string_sift != access_string_m_hat:
                break
        
        # Assert that we haven't left the loop just because of iterating through all values of i
        assert access_string_sift != access_string_m_hat

        # Find the last common ancestor (lca) of access_string_sift and access_string_m_hat in T
        lca = self.__get_lca(access_string_sift, access_string_m_hat)


        # let j be the least i such that s[i] does not equal s_hat[i]
        gamma_j_minus_1 = gamma[0 : j]

        # Update dictionary with access string
        assert(gamma_j_minus_1 != "")
        self.update_dictionary(gamma_j_minus_1, len(self.access_string_reference))
        
        # Get node in tree T to edit
        if gamma_j_minus_1 in self.access_string_reference.keys():
            node_to_edit = memoize(self.__sift_return_node(gamma_j_minus_1, self.t))
        else:
            node_to_edit = self.__sift_return_node(gamma_j_minus_1, self.t)
        s_j_minus_1 = node_to_edit.value
    
        # The new distinguishing string is the character gamma[j] concatonated with
        # the last common ancestor distinguishing string between access_string_sift and access_string_m_hat in T
        new_d = gamma[j] + lca

        assert new_d
        assert self.my_teacher.member(s_j_minus_1 + new_d) != self.my_teacher.member(gamma_j_minus_1 + new_d)

        # create a parent for our new node
        temp = node_to_edit.parent
        assert temp.left_child
        assert temp.right_child

        # assert (temp.left_child == node_to_edit) or (temp.right_child == node_to_edit)

        node_to_edit.parent = Node(None, temp, node_to_edit.level)
        node_to_edit.level += 1
        # set parent value to distinguishing string
        node_to_edit.parent.value = new_d
        if(temp.left_child.value == node_to_edit.value):
            temp.left_child = node_to_edit.parent
        else:
            assert temp.right_child.value == node_to_edit.value
            temp.right_child = node_to_edit.parent

        # determine whether our current "node to edit", which contains the access string, is left or right child (acc/rej)
        assert (not node_to_edit.left_child) and (not node_to_edit.right_child)
        # this statement should still be true because we have not changed the child of our NEW PARENT to node_to_edit

        if self.my_teacher.member(s_j_minus_1 + new_d) and not self.my_teacher.member(gamma_j_minus_1 + new_d):
            node_to_edit.parent.right_child = node_to_edit
            node_to_edit.parent.left_child = Node(gamma_j_minus_1, node_to_edit.parent, node_to_edit.level)
        elif self.my_teacher.member(gamma_j_minus_1 + new_d) and not self.my_teacher.member(s_j_minus_1 + new_d):
            node_to_edit.parent.left_child = node_to_edit
            node_to_edit.parent.right_child = Node(gamma_j_minus_1, node_to_edit.parent, node_to_edit.level)
        else:
            print(f"Error: Both {s_j_minus_1 + new_d} and {gamma_j_minus_1 + new_d} are {"accepted" if self.my_teacher.member(s_j_minus_1 + new_d) else "rejected"}")
            exit(f"Error: Unable to sort access string {gamma_j_minus_1} into T")


    ##########################################################################################################

    def construct_hypothesis(self):
        '''
        Constructs a hypothesized DFA M_Hat from the classification tree self.t.
        Returns array representing the DFA
        '''
       
        to_become = []

        # for each access string (leaf) of T, create a state in M_hat
        for key in self.access_string_reference.keys():
            to_append = []
            
            # Save a boolean indicating if the given key corresponds to an accept or reject state
            if self.my_teacher.member(key):
                to_append.append(1)
            else:
                to_append.append(0)

            # Create space for the arrows
            for i in range(len(self.alphabet)):
                to_append.append(-1)
            
            to_become.append(to_append)

        # start state of M_hat is lambda, the empty string
        # for each state in M_hat and each symbol b in the language, compute the b-transition out of the access string s:
        for key in self.access_string_reference.keys():
            # for each symbol b in the language, sift
            for b in self.alphabet:
                resulting_state = self.__sift(key + b, self.t)
                # direct the b-transition out of s to the resulting sifted state in M_hat
                to_direct = self.access_string_reference[resulting_state]
                # set TO BECOME [ index of key string ] [ index of character b in alphabet ] to be equal to to_direct
            
                to_become[self.access_string_reference[key]][self.alphabet.index(b) + 1] = to_direct

        # Ensure that all -1s have been overwritten
        for row in to_become:
            for entry in row:
                assert entry >= 0

        return to_become

    ##########################################################################################################

    def __sift_return_node(self, s, tr):
        '''
        sifts string s through the Tree T and returns the leaf NODE (not the access string, which is the Node's value) in T for the state in M accessed by string s
        :param s: the string being sifted
        NOTE: this function will be called as a memoized version of itself if the param s is an access string
        '''
        
        # set current node to root of T
        current = tr.root

        loops_to_find_leaf = 0

        # Loop as long as current has a left child (that is, as long as current is not a leaf)
        while (current.left_child):
                        
            # d is distinguishing string at current node
            d = current.value

            # membership query on sd (concatenated) 
            # if membership query is accepted, current node is right child of current node
            if self.my_teacher.member(s + d):
                current = current.right_child
            # else (if rejected), current node is left child of current node
            else:
                current = current.left_child
            
            loops_to_find_leaf += 1
                    
        # We have reached this point because current does not have a left child.
        # Because each tree node should have either 0 or 2 children (not 1), this means that current should also not have a right child
        assert not current.right_child

        # Check that access string is properly stored
        assert (current.value in self.access_string_reference.keys())
        
        # Return the access string at the leaf found
        return current

    ##########################################################################################################

    # input: s is the string being sifted and T is our tree
    # output: access string in T for the state of M accessed by s
    def __sift(self, s, tr):
        '''
        Returns the access string from tree T associated with the state of M accessed by string s.
        Calls sift_return_node and then returns the value from the node.
        :param s: the string s being sifted
        '''

        if s in self.access_string_reference.keys():
            return memoize(self.__sift_return_node(s, tr)).value
        
        return self.__sift_return_node(s, tr).value
    
    ##########################################################################################################

##############################################################################################################

class Node:

    ##########################################################################################################

    def __init__(self, value : str, parent, level):
        '''
        Node constructor
        :param value: the string stored in the node
        :param parent: the Node that is self's parent
        :param level: an int representing the level of the Node in T (root = 0)
        '''
        self.value = value

        self.parent = parent

        # always have 0 or 2 children, never only 1 child, due to distinguishing string logistics
        self.left_child = None
        self.right_child = None
        
        # The level of the tree at which the node is located (root = 0)
        self.level = level
    
    ##########################################################################################################

##############################################################################################################

class Tree:

    ##########################################################################################################

    def __init__(self, root: Node):
        '''
        Tree constructor
        :param root: the Node that is the root of the tree
        '''
        self.root = root

    ##########################################################################################################

    def print_tree(self):
        '''
        Prints the tree to terminal
        '''
        stack = []
        stack.append(self.root)
        while stack:
            to_print = stack.pop()
            # append right child first so the left child gets printed first
            if to_print.right_child is not None:
                stack.append(to_print.right_child)
            if to_print.left_child is not None:
                stack.append(to_print.left_child)
            
            n = to_print
            while n.parent is not None:
                print("\t", end="")
                n = n.parent
            
            # Specify if the string is a distinguishing string or access string
            # If the string is empty, print "empty." If it is NoneType, indicate lack of initialization. If it has a non-empty value, print it
            # Also print the level at which the node is located
            print(f"{"d" if to_print.left_child else "s"}: {("empty" if to_print.value == "" else to_print.value) if (to_print.value != None) else "not initialized"}, level {to_print.level}")

    ##########################################################################################################

##############################################################################################################