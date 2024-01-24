"""
File: dfa.py
Authors:
Kaelan Anderson - kaelananderson@sandiego.edu
Dillon Timmer - dtimmer@sandiego.edu

Last modified: 09/21/2023
Description: A program that reads in the contents of a file that contains the 
information of a DFA, handles files that are incorrectly formatted, and determines 
if an input string is in the language of the DFA.
"""

import sys

class FileFormatError(Exception):
    """
    Exception that is raised if the 
    input file to the DFA constructor
    is incorrectly formatted.
    """

    pass


class DFA:
    def __init__(self, *, filename=None):
        """
        Initializes DFA object from the dfa specification
        in named parameter filename.
        """

        # initialze the general dfa
        self.num_states = 0
        self.alphabet = []
        self.transitions = {}
        self.start_state = None
        self.accept_states = set()

        if filename:

            f = open(filename, 'r')

            # set num_states to first line, throw if not an int
            try:
                self.num_states = int(f.readline())
            except:
                raise FileFormatError

            # set alphabet to array of second line, throw if no given alphabet
            self.alphabet = list(f.readline().strip())
            if len(self.alphabet) == 0:
                raise FileFormatError

            for line in f:
                # if ' in line then it is a transition function and add it to funcs list
                if "'" in line:

                    func = line.strip().split(" ")

                    # check if transition states are in range
                    if not (1 <= int(func[0]) <= self.num_states and 1 <= int(func[2]) <= self.num_states):
                        raise FileFormatError

                    # check if scanned symbol in alphabet
                    if not ((func[1])[1:-1] in self.alphabet):
                        raise FileFormatError

                    # add to dict with key = (qa, c) and val = qb
                    self.transitions[(int(func[0]), (func[1])[1:-1])] = int(func[2])

                # else, next line must be start state
                else:
                    self.start_state = line.strip()
                    # check state in range
                    if not (1 <= int(self.start_state) <= self.num_states):
                        raise FileFormatError
                    break

            # set accept states, check if each in range
            self.accept_states = set(f.readline().strip().split())
            for state in self.accept_states:
                try:
                    if not (1 <= int(state) <= self.num_states):
                        raise FileFormatError
                except:
                    raise FileFormatError

            # check if extra line
            if len(f.readline()) != 0:
                raise FileFormatError

        return

    def simulate(self, str):
        """
        Returns True if str is in the language of the DFA,
        and False if not.

        Assumes that all characters in str are in the alphabet 
        of the DFA.
        """

        current_state = self.start_state

        # update state for each transition
        for char in str:
            try:
                current_state = self.transitions[(current_state, char)]
            except:
                return False

        # return bool of final state being accept state
        return current_state in self.accept_states

    def transition(self, state, symbol):
        """
        Returns the state to transition to from "state" on in input symbol "symbol".
        state must be in the range 1, ..., num_states
        symbol must be in the alphabet
        the returned state must be in the range 1, ..., num_states
        """
        return (self.transitions[((state), (symbol))])

if __name__ == "__main__":
    # You can run your dfa.py code directly from a
    # terminal command line:

    # Check for correct number of command line arguments
    if len(sys.argv) != 3:
        print("Usage: python3 pa1.py dfa_filename str")
        sys.exit(0)

    dfa = DFA(filename=sys.argv[1])
    str = sys.argv[2]
    ans = dfa.simulate(str)
    if ans:
        print(f"The string {str} is in the language of the DFA")
    else:
        print(f"The string {str} is NOT in the language of the DFA")
