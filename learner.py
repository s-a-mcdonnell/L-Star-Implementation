from teacher import Teacher

# Initialize T and ^M
# Go through the loop

class Learner:

    def __init__(self):

        self.solved = False
        # intialize alphabet and teacher
        # Note that the alphabet must contains characters (one-character strings), not ints
        self.alphabet = ['0','1']
        self.my_teacher = Teacher(self.alphabet)

        # initialize T with just the empty string (lambda)
        t = Tree("")
        # lambda is not a variable name in Python due to it being used for function stuff so I'm going to call it 

        # create M_hat with just one state in T
        # The DFA (M) is a matrix in which the rows are the nodes
        # The first entry in each row is a boolean in int form (0 or 1) indicating whether the node is an accept (1) or reject (0) state
        # The remaining entries in each row are the numbers of the nodes which the corresponding alphabet value at that index points to
        self.m_hat = [[-1]*(len(self.alphabet)+1)]

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
                t.root.rightChild = Node(gamma)
                t.root.leftChild = Node("")
            else:
                # counterexample is rejected
                t.root.rightChild = Node("")
                t.root.leftChild = Node(gamma)


    def lstar_algorithm(self):
        print("running l-star")

        while not self.solved:
            # create new M_hat from current T => call construct_hypothesis
            # equivalence query => does our current M_hat equal the real M from teacher?
            # if yes we are done
            # if no, update T by determining the new access string and distinguishing string (shift down)
                # call update_tree
                # series of membership queries on prefix of counterexample gamma
            pass


    # input: gamma (a counterexample generated from an equivalence query) and our tree T
    # output: an updated tree T
    def update_tree(self, gamma, t):
        # for each prefix set of characters of gamma
            # sift gamma[i] in T
            # repeat until gamma[i] gives you differing results in M and M_hat (s[i] does not equal s_hat[i])
        # let j be the least i s.t. s[i] does not equal s_hat[i]
        # replace access string s[j-1] in T with an internal node with two leaf nodes
            # leaf nodes are the previous access string and the new access string gamma[j-1]
            # the internal node is distinguishing CHARACTER gamma_j appended with d where d is the parent distinguishing string
        # return new tree
        pass


    # input: T is our classification tree
    # output: hypothesis M_hat constructed from T
    def construct_hypothesis(self, t):
        # for each access string (leaf) of T, create a state in M_hat
        # start state of M_hat is gamma, the empty string
        # for each state in M_hat and each symbol b in the language, compute the b-transition out of s:
            # sift(sb, T)
            # direct the b-transition out of s to the resulting sifted state in M_hat
        pass


    # input: s is the string being sifted and T is our tree
    # output: access string in T for the state of M accessed by s
    def sift(self, s, t):
        # set current node to root of T

        # loop:
            # d is distinguishing string at current node
            # membership query on sd
                # if accepted, current node is right child of current node
                # else if rejected, current node is left child of current node
            # after updating current node's position, if current node is a leaf node, return access string
            # otherwise, repeat loop
        pass

class Node:

    def __init__(self, value, parent = None):
        self.value = value

        self.parent = parent

        # always have 0 or 2 children, never only 1 child, due to distinguishing string logistics
        self.leftChild = None
        self.rightChild = None


# TODO: implement regular silly tree :)
class Tree:

    def __init__(self, root: Node):
        self.root = root

    # other methods go here ie sorting stuff
        