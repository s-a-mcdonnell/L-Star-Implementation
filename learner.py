from teacher import Teacher

# Initialize T and ^M
# Go through the loop

class Learner:

    # NOTE: I don't think we have to pass the tree t into any of the methods in the Learner class because it belongs 

    def __init__(self, alphabet = ['0','1']):

        test_tree = Tree(Node("root"))
        test_tree.root.left_child = Node("left child", test_tree.root)
        test_tree.root.right_child = Node("right child", test_tree.root)
        test_tree.print_tree()


        self.solved = False
        # intialize alphabet and teacher
        # Note that the alphabet must contains characters (one-character strings), not ints
        self.alphabet = alphabet
        self.my_teacher = Teacher(self.alphabet)

        # initialize T with just the empty string (lambda)
        t = Tree(Node(""))
        # lambda is not a variable name in Python due to it being used for function stuff so I'm going to call it 

        # create M_hat with just one state in T
        # The DFA (M) is a matrix in which the rows are the nodes
        # The first entry in each row is a boolean in int form (0 or 1) indicating whether the node is an accept (1) or reject (0) state
        # The remaining entries in each row are the numbers of the nodes which the corresponding alphabet value at that index points to
        self.m_hat = [[-1]*(len(self.alphabet)+1)]

        # dictionary for storing access strings as keys corresponding to their rows in the m_hat matrix
        # add to the dictionary when updating the tree, not when reconstructing m_hat, because we need dict to construct m_hat
        self.access_string_reference = {}
        self.access_string_reference.update({"": 0})

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
        self.m_hat.append(to_append)
    
        # equivalence query on initial M_hat
        gamma = self.my_teacher.equivalent(self.m_hat)
        if not gamma:
            print("We are done. DFA is the trivial DFA.")
            self.solved = True
        # put counterexample gamma into our tree T
        else:
            print("Counterexample found, adding to tree.")
            if self.my_teacher.member(gamma):
                t.root.right_child = Node(gamma, t.root)
                t.root.left_child = Node("", t.root)
            else:
                # counterexample is rejected
                t.root.right_child = Node("", t.root)
                t.root.left_child = Node(gamma, t.root)
            self.access_string_reference.update({gamma: 1})
        print("Initialization done")
        # t.print_tree()
        # print("tree printed")
        # print(self.access_string_reference)


    def lstar_algorithm(self):
        print("running l-star")

        while not self.solved:
            # create new M_hat from current T => call construct_hypothesis
            self.m_hat = self.construct_hypothesis(self.t)
            # equivalence query => does our current M_hat equal the real M from teacher?
            gamma = self.my_teacher.equivalent(self.m_hat)
            if not gamma:
                # if yes we are done
                print("We are done. DFA is the trivial DFA.")
                self.solved = True
            # if no, update T by determining the new access string and distinguishing string (shift down)
            else:
                self.update_tree(gamma)
                # call update_tree
        print("End L-Star algorithm")


    # input: gamma (a counterexample generated from an equivalence query) and our tree T
    # output: an updated tree T
    def update_tree(self, gamma):
        # for each prefix set of characters of gamma
        j = ""
        for i in range(len(gamma)):
            strng = gamma[0: i + 1]
            # sift gamma[i] in T
            self.sift(strng)
            # repeat until gamma[i] gives you differing results in M and M_hat (s[i] does not equal s_hat[i])
            # TODO: a little confused on how to implement this part

        # let j be the least i s.t. s[i] does not equal s_hat[i]
    
        # replace access string s[j-1] in T with an internal node with two leaf nodes
            # leaf nodes are the previous access string and the new access string gamma[j-1]
            # the internal node is distinguishing CHARACTER gamma_j appended with d where d is the parent distinguishing string
        # return new tree and/or edit self.t


    # input: T is our classification tree
    # output: hypothesis M_hat constructed from T
    def construct_hypothesis(self):
        to_become = [[-1]*(len(self.alphabet)+1)]
        # for each access string (leaf) of T, create a state in M_hat
        for key in self.access_string_reference:
            to_append = []
            for i in range(len(self.alphabet) + 1):
                to_append.append(0)
            to_become.append(to_append)
        # start state of M_hat is gamma, the empty string
        # for each state in M_hat and each symbol b in the language, compute the b-transition out of s:
        for key in self.access_string_reference:
            # for each symbol b in the language, sift
            for b in self.alphabet:
                resulting_state = self.sift(key + b)
                # direct the b-transition out of s to the resulting sifted state in M_hat

        self.m_hat = to_become


    # input: s is the string being sifted and T is our tree
    # output: access string in T for the state of M accessed by s
    def sift(self, s):
        # set current node to root of T
        current = self.t.root

        # Loop as long as current has a left child (that is, as long as current is not a leaf)
        while (current.left_child):
                        
            # d is distinguishing string at current node
            d = current.value

            # membership query on sd
            counterexample = self.my_teacher.member(s + d)
            
            # if membership query rejected, current node is left child of current node
            if counterexample:
                current = current.left_child
            # else (if accepted), current node is right child of current node
            else:
                assert not counterexample
                current = current.right_child
                    
        # NOTE: We have reached this point because current does not have a left child.
        # Because each tree node should have either 0 or 2 children (not 1), this means that current should also not have a right child
        assert not current.right_child

        # Return the access string at the leaf found
        return current.value


class Node:

    def __init__(self, value, parent = None):
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
            if(to_print.value == ""):
                print("empty")
            else:
                print(to_print.value)