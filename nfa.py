import dfa  # imports your DFA class from pa1
from collections import deque

class NFA:
    """ Simulates an NFA """

    def __init__(self, nfa_filename=None):
        """
        Initializes NFA from the file whose name is
        nfa_filename.  (So you should create an internal representation
        of the nfa.)
        """

        self.num_states = 0
        self.alphabet = []
        self.transitions = {}
        self.start_st = None
        self.accept_sts = None

        if nfa_filename:

            f = open(nfa_filename, 'r')

            self.num_states = int(f.readline())
            self.alphabet = list(f.readline().strip())

            for line in f:
                # add each transition to dict
                if "'" in line:

                    func = line.strip().split(" ")

                    # Check if transition state is in dict yet, append if so
                    if int(func[0]) in self.transitions.keys():
                        # {state: (char, state)}
                        self.transitions[int(func[0])].append(((func[1])[1:-1], int(func[2])))
                    else:
                        self.transitions[int(func[0])] = [((func[1])[1:-1], int(func[2]))]
                else:
                    break

            self.start_st = int(f.readline().strip())
            self.accept_sts = (f.readline().strip().split())
            
            return

    def to_DFA(self):
        """
        Converts the "self" NFA into an equivalent DFA object
        and returns that DFA.  The DFA object should be an
        instance of the DFA class that you defined in pa1.
        The attributes (instance variables) of the DFA must conform to
        the requirements laid out in the pa2 problem statement (and that are the same
        as the DFA file requirements specified in the pa1 problem statement).

        This function should not read in the NFA file again.  It should
        create the DFA from the internal representation of the NFA that you
        created in __init__.
        """

        def find_epsilons(from_state):
            queue = deque([from_state])
            results = set()

            while queue:
                # Get the next state to process
                current_state = queue.pop()
                if current_state != from_state:
                    results.add(current_state)

                # If the current state has an 'e' transition, add its 'e' transition states to the queue
                if current_state in self.transitions:
                    for char, next_state in self.transitions[current_state]:
                        if char == 'e' and next_state not in results:
                            queue.append(next_state)
            
            return list(results)

        def find_accepts(from_states):
            for state in from_states:
                if (state) in self.accept_sts:
                    converted_dfa.accept_states.add(converted_dfa.num_states)

        # initialize dfa values
        converted_dfa = dfa.DFA()
        converted_dfa.alphabet = self.alphabet

        # set reject state (1) to loop on all chars
        for char in self.alphabet:
            converted_dfa.transitions[(1, char) ] = 1

        # map start state to 2
        converted_dfa.start_state = 2
        state_map = {2: [self.start_st]}
        converted_dfa.num_states = 2

        # find all epsilons from start state
        state_map[2] += find_epsilons(self.start_st)

        # find if start state is an accept state
        find_accepts(state_map[2])

        # create queue with start state
        queue = deque([2])

        while queue:

            current_state = queue.pop()

            # get nfa states from mapping
            substates = state_map[current_state]

            # check where every char transitions to from nfa states
            for char in self.alphabet:

                # add all possible transitions to array
                next_states = []
                for state in substates:
                    # if no transitions for state, add nothing to array
                    try:
                        next_states += [tup[1] for tup in self.transitions[state] if tup[0] == char]
                        # for state in next state
                            # if state has epsilon trans
                                # add epsilon to next_state also
                    except:
                        next_states += []

                for state in next_states:
                    next_states += find_epsilons(state)

                if next_states:

                    # remove duplicates and sort subset
                    next_states = list(set(next_states))
                    state_mapped = False

					# if subset already defined by new state
                    for key, val in state_map.items():
                        if next_states == val:
                            converted_dfa.transitions[((current_state), char) ] = (key)
                            state_mapped = True
                    
                    if not state_mapped:

                        # if subset not defined set to next state
                        converted_dfa.num_states += 1
                        converted_dfa.transitions[((current_state), char) ] = (converted_dfa.num_states)

                        # set accept states if they are in subset
                        find_accepts(next_states)

                        # map subset to int state and add to queue
                        state_map[converted_dfa.num_states] = next_states
                        queue.append(converted_dfa.num_states)

                # if no transitions, send to reject state (1)
                else:
                    converted_dfa.transitions[((current_state), char) ] = 1

        return converted_dfa
