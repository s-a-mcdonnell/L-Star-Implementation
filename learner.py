from teacher import Teacher

class Learner:

    # Constructor
    def __init__(self):
        print("learner created")

        self.alphabet = [0, 1]

        # Create teacher
        self.my_teacher = Teacher(self.alphabet)

        # Initialize T and ^M
        pass

    def run(self):
        print("running")

        unsolved = True

        # Go through the loop
        while unsolved:
            pass