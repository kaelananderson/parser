"""
file: regex.py

Authors: 
Kaelan Anderson - kaelananderson@sandiego.edu
Dillon Timmer - dtimmer@sandiego.edu

Last modified: 11/7/2023

Description: 
A program defines classes and methods to work with regular expressions and 
convert them into NFAs. It includes a `Node` class for creating a syntax tree 
from a regular expression, an `NFA` class to represent NFAs, and a `RegEx` class 
to process regular expressions, convert them into NFAs, and validate strings 
against the regular expressions. The code aims to provide a framework for handling 
regular expressions and automata, with a focus on the NFA construction part.
"""

from dfa import DFA
from nfa import NFA
from collections import deque

class InvalidExpression(Exception):
	pass

state_count = 1

class Node:
	def __init__(self, data):
		self.data = data
		self.left = None
		self.right = None

	def Merge(self, dict1, dict2):
		res = {**dict1, **dict2}
		return res

	def to_nfa(self):

		global state_count

		# leaf node
		if self.left == None and self.right == None:

			# create base case NFA
			leaf_nfa = NFA()
			leaf_nfa.num_states = 2
			leaf_nfa.alphabet = [self.data]
			leaf_nfa.transitions[state_count] = [(self.data, state_count+1)] 
			leaf_nfa.start_st = state_count
			leaf_nfa.accept_sts = [state_count+1]

			# 2 states used to create base case
			state_count += 2

			return leaf_nfa

		# interior node
		else:
						
			# all operations have right node
			right_nfa = self.right.to_nfa()

			if self.data == '*':

				# create new accepting start state and epsilon to original start state
				star_nfa = NFA()
				star_nfa.num_states = right_nfa.num_states + 1
				star_nfa.alphabet = right_nfa.alphabet
				star_nfa.start_st = state_count
				star_nfa.accept_sts = right_nfa.accept_sts + [star_nfa.start_st]
				star_nfa.transitions = right_nfa.transitions
				star_nfa.transitions[star_nfa.start_st] = [('e', right_nfa.start_st)]

				# epsilon from all accept states to original start state
				for state in right_nfa.accept_sts:
					if state in star_nfa.transitions.keys():
						star_nfa.transitions[state].append(('e', right_nfa.start_st))
					else:
						star_nfa.transitions[state] = [('e', right_nfa.start_st)]

				# 1 state used for new start
				state_count += 1

				return star_nfa

			if self.data == '^':
				left_nfa = self.left.to_nfa()

				# combine both sub NFAs
				concat_nfa = NFA()
				concat_nfa.num_states = right_nfa.num_states + left_nfa.num_states
				concat_nfa.alphabet = list(set(right_nfa.alphabet + left_nfa.alphabet))
				concat_nfa.transitions = self.Merge(right_nfa.transitions, left_nfa.transitions)
				concat_nfa.start_st = left_nfa.start_st
				concat_nfa.accept_sts = right_nfa.accept_sts

				# set epsilon from accept state of left to start of right
				for state in left_nfa.accept_sts:
					if state in concat_nfa.transitions.keys():
						concat_nfa.transitions[state].append(('e', right_nfa.start_st))
					else:
						concat_nfa.transitions[state] = [('e', right_nfa.start_st)]

				return concat_nfa

			if self.data == '|':
				left_nfa = self.left.to_nfa()

				# combine NFAs and create new start state
				union_nfa = NFA()
				union_nfa.num_states = right_nfa.num_states + left_nfa.num_states + 1
				union_nfa.alphabet = list(set(right_nfa.alphabet + left_nfa.alphabet))
				union_nfa.transitions = self.Merge(right_nfa.transitions, left_nfa.transitions)
				union_nfa.start_st = state_count
				union_nfa.accept_sts = left_nfa.accept_sts + right_nfa.accept_sts

				# epsilon from new start to both accept states
				union_nfa.transitions[union_nfa.start_st] = [('e', left_nfa.start_st), ('e', right_nfa.start_st)]

				# 1 state used for new start
				state_count += 1

				return union_nfa

class RegEx:

	equivDfa = None

	def __init__(self, filename=None):
		"""
		Initializes regular expression from the file "filename"
		"""

		self.alphabet = None
		self.regex = None

		if filename:
		
			f = open(filename, 'r')

			# save alphabet as list
			alphabet_line = f.readline()
			self.alphabet = list(alphabet_line[alphabet_line.find('"') + 1: alphabet_line.rfind('"')])

			# split regex statement into list of chars
			regex_line = f.readline()
			self.regex = list(regex_line[regex_line.find('"') + 1: regex_line.rfind('"')])

		return

	def to_nfa(self):
		"""
		Returns an NFA object that is equivalent to 
		the "self" regular expression
		"""

		# create initial stacks
		operand_stack = deque()
		operator_stack = deque()

		# dict to evalute operator precedence
		precedence = {
			'*': 3,
			'^': 2,
			'|': 1,
			'(': 0
		}

		# iterate with while to handle escape chars
		i = 0
		while i < len(self.regex):

			char = self.regex[i]

			if char in self.alphabet + ['e', "\\"] and (char not in ['*', '|', '^', '(', ')']):

				if char == "\\":
					i += 1
					char = self.regex[i]

				# push tree node
				operand_stack.append(Node(char))

				# add implied concat
				if i+1 < len(self.regex):
					if self.regex[i+1] in self.alphabet + ['(', '\\'] and (self.regex[i+1] not in ['*', '|', '^', ')']):
						self.regex.insert(i+1, '^')

			# push left paren onto operator stack
			elif char == '(':
				operator_stack.append(char)
				pass

			elif char in ['*', '|', '^']:

				while len(operator_stack) != 0 and precedence[operator_stack[-1]] >= precedence[char]:

					# create new node from operator
					new_node = Node(operator_stack.pop())
					new_node.right = operand_stack.pop()

					# add 2nd operand if needed
					if new_node.data in ['|', '^']:
						new_node.left = operand_stack.pop()

					operand_stack.append(new_node)

				operator_stack.append(char)

				# check for implied concat after star
				if char == '*':
					if i+1 < len(self.regex):
						if self.regex[i+1] in self.alphabet + ['(', '\\'] and (self.regex[i+1] not in ['*', '|', '^', ')']):
							self.regex.insert(i+1, '^')

			elif char == ')':
				top = operator_stack.pop()

				while top != '(':

					# create new node from operator
					new_node = Node(top)
					new_node.right = operand_stack.pop()

					# add 2nd operand if needed
					if new_node.data in ['|', '^']:
						new_node.left = operand_stack.pop()

					operand_stack.append(new_node)

					top = operator_stack.pop()

				# if right paren followed by implied concat
				if i+1 < len(self.regex):
					if self.regex[i+1] in self.alphabet + ['(', '\\'] and (self.regex[i+1] not in ['*', '|', '^', ')']):
						self.regex.insert(i+1, '^')

			i += 1

		while len(operator_stack) != 0:

			# create new node from operator
			new_node = Node(operator_stack.pop())
			new_node.right = operand_stack.pop()

			# add 2nd operand if needed
			if new_node.data in ['|', '^']:
				new_node.left = operand_stack.pop()

			operand_stack.append(new_node)

		complete_nfa = operand_stack.pop().to_nfa()

		return complete_nfa

	def simulate(self, str):
		"""
		Returns True if str is in the languages defined
		by the "self" regular expression
		"""

		if self.equivDfa == None:
			nfa = self.to_nfa()
			self.equivDfa = nfa.to_DFA()

		return self.equivDfa.simulate(str)