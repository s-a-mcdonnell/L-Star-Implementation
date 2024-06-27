from teacher import Teacher

# Initialize T and ^M
# Go through the loop

class Learner:

    def __init__(self):
        # initialize T with just the empty string (lambda)
        # create M_hat with just one state in T
        # equivalence query on initial M_hat
        # put counterexample gamma into our tree T

        # TODO: alphabet created in learner and passed to teacher for teacher's constructor

        # call lstar_algorithm
        pass


    def lstar_algorithm(self, teacher):
        # loop:
            # create new M_hat from current T => call construct_hypothesis
            # equivalence query => does our current M_hat equal the real M from teacher?
            # if yes we are done
            # if no, update T by determining the new access string and distinguishing string (shift down)
                # call update_tree
                # series of membership queries on prefix of counterexample gamma
        pass


    # input: gamma, a counterexample generated from an equivalence query, and our tree T
    # output: an updated tree T
    def update_tree(self, gamma, T):
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
    def construct_hypothesis(self, T):
        # for each access string (leaf) of T, create a state in M_hat
        # start state of M_hat is gamma, the empty string
        # for each state in M_hat and each symbol b in the language, compute the b-transition out of s:
            # sift(sb, T)
            # direct the b-transition out of s to the resulting sifted state in M_hat
        pass


    # input: s is the string being sifted and T is our tree
    # output: access string in T for the state of M accessed by s
    def sift(self, s, T):
        # set current node to root of T

        # loop:
            # d is distinguishing string at current node
            # membership query on sd
                # if accepted, current node is right child of current node
                # else if rejected, current node is left child of current node
            # after updating current node's position, if current node is a leaf node, return access string
            # otherwise, repeat loop
        pass