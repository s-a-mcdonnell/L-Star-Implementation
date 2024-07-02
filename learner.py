from teacher import Teacher

# Initialize T and ^M
# Go through the loop

class Learner:

    # NOTE: I don't think we have to pass the tree t into any of the methods in the Learner class because it belongs
    # TODO: NOTHING IS TESTED except for init :)

    # Updates the access string reference dictionary with the given values
    # Isolated to its own method for debugging purposes (prevent clobbering)
    def update_dictionary(self, key : str, index : int):
        print("adding key " + key + " to dictionary")
        # assert (not key in self.access_string_reference.keys()) 

        # Print debugging information if trying to clobber a pre-existing key:
        if key in self.access_string_reference.keys():
            print("trying to clobber key " + key)
            self.sift(key)
            #exit(1)
            assert not key in self.access_string_reference.keys()

        self.access_string_reference.update({key : index})

    def __init__(self, alphabet = ['0','1'], num_states = -1, premade_dfa = None):

        test_tree = Tree(Node("root", None))
        test_tree.root.left_child = Node("left child", test_tree.root)
        test_tree.root.right_child = Node("right child", test_tree.root)
        #test_tree.print_tree()


        self.solved = False
        # intialize alphabet and teacher
        # Note that the alphabet must contains characters (one-character strings), not ints
        self.alphabet = alphabet
        
        # If a premade DFA was provided (for testing), use it
        if premade_dfa:
            self.my_teacher = Teacher(self.alphabet, premade_dfa = premade_dfa)
        else:
            self.my_teacher = Teacher(self.alphabet, num_states = num_states)

        # initialize T with just the empty string (lambda)
        self.t = Tree(Node("", None))
        # lambda is not a variable name in Python due to it being used for function stuff so I'm going to call it 

        # create M_hat with just one state in T
        # The DFA (M) is a matrix in which the rows are the nodes
        # The first entry in each row is a boolean in int form (0 or 1) indicating whether the node is an accept (1) or reject (0) state
        # The remaining entries in each row are the numbers of the nodes which the corresponding alphabet value at that index points to
        self.m_hat = []

        # dictionary for storing access strings as keys corresponding to their rows in the m_hat matrix
        # add to the dictionary when updating the tree, not when reconstructing m_hat, because we need dict to construct m_hat
        self.access_string_reference = {}
        self.update_dictionary("", 0)
        # self.access_string_reference.update({"": 0})

        # append the first state
        # check whether empty string is accepted or rejected
        to_append = []
        if self.my_teacher.member(""):
            # empty string accepted
            to_append.append(1)
        else:
            to_append.append(0)
        for i in range(len(self.alphabet)):
            to_append.append(0)
        
        print("appending to m_hat")
        self.m_hat.append(to_append)
    
        # equivalence query on initial M_hat
        gamma = self.my_teacher.equivalent(self.m_hat)
        assert(self.my_teacher.member(gamma) != self.my_teacher.member(gamma, self.m_hat, self.alphabet))

        if not gamma:
            print("We are done. DFA is the trivial DFA.")
            self.solved = True
        # put counterexample gamma into our tree T
        else:
            assert gamma == str(gamma)

            print("Counterexample found, adding to tree.")
            if self.my_teacher.member(gamma):
                self.t.root.right_child = Node(gamma, self.t.root)
                self.t.root.left_child = Node("", self.t.root)
            else:
                # counterexample is rejected
                self.t.root.right_child = Node("", self.t.root)
                self.t.root.left_child = Node(gamma, self.t.root)
            
            # Add counterexample to the dictionary
            self.update_dictionary(gamma, 1)
            # self.access_string_reference.update({gamma: 1})

        # Confirm that all -1s have been overwritten
        for row in self.m_hat:
            for entry in row:
                assert entry >= 0
        
        print("m_hat at end of initialization: " + str(self.m_hat))

        #self.t.print_tree()

        print("Initialization done")
        # t.print_tree()
        # print("tree printed")
        # print(self.access_string_reference)


    def lstar_algorithm(self):
        print("running l-star")

        while not self.solved:
            # create new M_hat from current T => call construct_hypothesis
            self.m_hat = self.construct_hypothesis()
            print(f"m_hat updated {self.m_hat}")
            # print("m_hat updated " + str(self.m_hat))
            # equivalence query => does our current M_hat equal the real M from teacher?
            gamma = self.my_teacher.equivalent(self.m_hat)

            print("Counterexample is ===> " + str(gamma))
            if not gamma:
                # if yes we are done
                print("DFA solved!")
                print("Learned DFA:")
                print(self.m_hat)
                self.solved = True
            # if no, update T by determining the new access string and distinguishing string (sift down)
            else:
                assert(self.my_teacher.member(gamma) != self.my_teacher.member(gamma, self.m_hat, self.alphabet))

                assert type(gamma) is str

                # call update_tree (includes updating dictionary)
                self.update_tree(gamma)

                print("number of entries in dictionary: " + str(len(self.access_string_reference)))
                print("number of rows in M_hat: " + str(len(self.m_hat)))

                #self.t.print_tree()
            print("LOOP COMPLETE IN L STAR")
        print("End L-Star algorithm")

    # input: gamma (a counterexample generated from an equivalence query) and our tree T (from self)
    # output: Edits T to update it (returns nothing)
    # NOTE: remember to SET THE PARENT of a new node when you declare it
    def update_tree(self, gamma):
        print("Update tree called")
        print(f"Updating the tree with {gamma}")

        # Assert that gamma really is a counterexample
        assert bool(self.my_teacher.member(gamma)) != bool(self.my_teacher.member(gamma, self.m_hat, self.alphabet))


        j = 0
        # for each prefix set of characters of gamma
        for i in range(len(gamma)):
            j = i

            # Get the first i characters of gamma
            strng = gamma[0 : i + 1]
            # sift gamma[i] in T
            node_sift = self.sift_return_node(strng, breaker = True)
            access_string_sift = node_sift.value
            loop_d = node_sift.parent.value if node_sift.parent else ""

            # Accessing dictionary key from value according to these instructions: https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/#
            # TODO: This is a janky way to be using a dictionary. Is this the best-suited ADT for our purposes?
            row_in_m_hat = self.m_hat.index(Teacher.final_state(strng, self.m_hat, self.alphabet))
            my_dict = self.access_string_reference
            access_string_m_hat = list(my_dict.keys())[list(my_dict.values()).index(row_in_m_hat)]

            # check if the returned access string accepts or rejects in M and M_hat
            # repeat loop until gamma[i] gives you differing results in M and M_hat (s[i] does not equal s_hat[i])
            '''if self.my_teacher.member(access_string) != self.my_teacher.member(access_string, self.m_hat):
                print("breaking loop")
                break'''
            
            # Repeat loop until sifting and running the truncated string through M_hat lead to distinct states (different access strings/row indices in M_hat)
            #if self.access_string_reference[access_string] != self.m_hat.index(Teacher.final_state(strng, self.m_hat, self.alphabet)):
            if access_string_sift != access_string_m_hat:
                print(f"strng {strng}")
                print(f"Access string from sifting: {access_string_sift if access_string_sift else "empty string"}")
                print(f"Access string from M_hat: {access_string_m_hat if access_string_m_hat else "empty string"}")
                print("breaking loop")
                break

        # let j be the least i such that s[i] does not equal s_hat[i]
        gamma_j_minus_1 = gamma[0 : j]
        print(f"gamma[j-1]: {gamma_j_minus_1}, j = {j}")
    
        # Update dictionary with access string
        assert(gamma_j_minus_1 != "")
        self.update_dictionary(gamma_j_minus_1, len(self.access_string_reference))
        
        # Get node in tree T to edit
        node_to_edit = self.sift_return_node(gamma_j_minus_1)
        s_j_minus_1 = node_to_edit.value
    
        # replace access string s[j-1] in T with an internal node with two leaf nodes
        # the new distinguishing string is the CHARACTER gamma_j concatenated with d where d is the parent distinguishing string
        # TODO: Replacing old d with d from loop
        # new_d = gamma[j] + node_to_edit.parent.value
        new_d = gamma[j] + loop_d
        print(f"node to edit value: {node_to_edit.value}")
        print(f"node to edit parent value: {(node_to_edit.parent.value if node_to_edit.parent.value else "empty") if node_to_edit.parent else "no parent"}")
        print(f"new distinguishing string: {new_d}")
        print(f"s[j-1] = {s_j_minus_1}")
        print(f"gamma[j-1] = {gamma_j_minus_1}")

        self.t.print_tree()
        print(self.m_hat)


    
        # Create child leaves for node_to_edit, making it an internal node
        assert (not node_to_edit.left_child) and (not node_to_edit.right_child)
        node_to_edit.left_child = Node(None, node_to_edit)
        node_to_edit.right_child = Node(None, node_to_edit)
    
        # Set values of node_to_edit's children
        # leaf nodes are the previous access string and the new access string gamma[j-1]
        # Determine which leaf node goes on each side by checking membership when concatenated with the new distinguishing string        
        if self.my_teacher.member(s_j_minus_1 + new_d):
            node_to_edit.right_child.value =  s_j_minus_1
            node_to_edit.left_child.value = gamma_j_minus_1
        elif self.my_teacher.member(gamma_j_minus_1 + new_d):
            node_to_edit.right_child.value = gamma_j_minus_1
            node_to_edit.left_child.value =  s_j_minus_1
        else:
            print(f"Both {s_j_minus_1 + new_d} and {gamma_j_minus_1 + new_d} are {"accepted" if self.my_teacher.member(s_j_minus_1 + new_d) else "rejected"}")
            exit(f"Error: Unable to sort access string {gamma_j_minus_1} into T")

        # Set node_to_edit's value to be the new distinguishing string
        assert node_to_edit.parent
        node_to_edit.value = new_d

        # print("update tree done.")


    # input: T is our classification tree
    # output: hypothesis M_hat constructed from T
    def construct_hypothesis(self):
        # print("construct hypothesis called")
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
            
            print(f"appending row to to_become for key {key}")
            to_become.append(to_append)
        
        #print("M_hat mid-construction: " + str(to_become))

        #print("access_string_reference.keys(): " + str(self.access_string_reference.keys()))

        # start state of M_hat is lambda, the empty string
        # for each state in M_hat and each symbol b in the language, compute the b-transition out of the access string s:
        for key in self.access_string_reference.keys():
            # for each symbol b in the language, sift
            for b in self.alphabet:
                resulting_state = self.sift(key + b)
                # direct the b-transition out of s to the resulting sifted state in M_hat
                to_direct = self.access_string_reference[resulting_state]
                # set TO BECOME [ index of key string ] [ index of character b in alphabet ] to be equal to to_direct
                #print("dictionary: " + str(self.access_string_reference))
                #print("key: " + key)
                #print("row index: " + str(self.access_string_reference[key]))
                #print("rows in to_become: " + str(len(to_become)))
                to_become[self.access_string_reference[key]][self.alphabet.index(b) + 1] = to_direct

        # Ensure that all -1s have been overwritten
        for row in to_become:
            for entry in row:
                entry >= 0
        print("new m_hat:")
        print(to_become)
        return to_become

    # input: s is the string being sifted and T is our tree
    # output: leaf NODE (not access string) in T for the state of M accessed by s
    def sift_return_node(self, s, breaker : bool = False):
        print("sift_return_node called on " + (s if s else "the empty string"))
        
        # set current node to root of T
        current = self.t.root

        loops_to_find_leaf = 0

        '''if breaker:
            breakpoint()'''

        # Loop as long as current has a left child (that is, as long as current is not a leaf)
        while (current.left_child):
                        
            # d is distinguishing string at current node
            d = current.value

            #print("current.value: " + d)
            #print(s + " + " + d + " is " + ("accepted" if self.my_teacher.member(s+d) else "rejected") + " by M")

            # membership query on sd (concatenated) 
            # if membership query is accepted, current node is right child of current node
            '''if self.my_teacher.member(str(s) + str(d)):'''
            if self.my_teacher.member(s + d):
                current = current.right_child
            # else (if rejected), current node is left child of current node
            else:
                current = current.left_child
            
            loops_to_find_leaf += 1
                    
        # NOTE: We have reached this point because current does not have a left child.
        # Because each tree node should have either 0 or 2 children (not 1), this means that current should also not have a right child
        assert not current.right_child

        #print("loops to find leaf: " + str(loops_to_find_leaf))

        # Check that access string is properly stored
        '''if not (current.value in self.access_string_reference.keys()):
            print("current value: " + current.value)
            print("dictionary: " + str(self.access_string_reference))
            exit(1)'''
        assert (current.value in self.access_string_reference.keys())
        
        # Return the access string at the leaf found
        print(f"ending sift after {loops_to_find_leaf} loops. returning NODE {self.access_string_reference[current.value]} with access string {current.value if current.value else "empty"}")
        return current


    # input: s is the string being sifted and T is our tree
    # output: access string in T for the state of M accessed by s
    def sift(self, s, breaker : bool = False):
        #print("---")
        #print("sift called on " + (s if s else "the empty string"))
        return self.sift_return_node(s, breaker).value


class Node:

    def __init__(self, value : str, parent):
        self.value = value

        self.parent = parent

        # always have 0 or 2 children, never only 1 child, due to distinguishing string logistics
        self.left_child = None
        self.right_child = None


class Tree:

    def __init__(self, root: Node):
        self.root = root

    # other methods go here ie sorting stuff
    def print_tree(self):
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
            print(f"{"d" if to_print.left_child else "s"}: {("empty" if to_print.value == "" else to_print.value) if (to_print.value != None) else "not initialized"}")
            '''if(to_print.value == ""):
                print(("d: " if to_print.left_child else "s: ") + "empty")
            else:
                print(("d: " if to_print.left_child else "s: ") + to_print.value)'''