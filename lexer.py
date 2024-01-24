"""
file: lexer.py

Authors: 
Kaelan Anderson - kaelananderson@sandiego.edu
Dillon Timmer - dtimmer@sandiego.edu

Last modified: 11/30/2023

Description: 
A Python program, that contains a class called Lex that 
serves as a rudimentary lexical analyzer generator. The class 
constructor accepts two parameters: the name of a file containing 
specifications for a set of token types defined by regular expressions and 
the name of a source text file. The primary method, next_token, scans the 
source file and returns the subsequent token based on the provided specifications.
"""

from regex import RegEx

class InvalidToken(Exception):
	""" 
	Raised if while scanning for a token,
	the lexical analyzer cannot identify 
	a valid token, but there are still
	characters remaining in the input file
	"""
	pass

class Lex:
	def __init__(self, regex_file, source_file):
		"""
		Initializes a lexical analyzer.  regex_file
		contains specifications of the types of tokens
		(see problem assignment for format), and source_file
		is the text file that tokens are returned from.
		"""

		regex_f = open(regex_file, 'r')

		# save alphabet as list
		alphabet_line = regex_f.readline()
		self.alphabet = list(alphabet_line[alphabet_line.find('"') + 1: alphabet_line.rfind('"')])

		# iterate through lines with tokens to build dict
		self.tokens_dict = {}
		for line in regex_f:

			token = line.strip().split(" ")

			# initialize regex object for line
			regex = RegEx()
			regex.alphabet = self.alphabet
			regex.regex = list(token[1][token[1].find('"') + 1: token[1].rfind('"')])

			# add "token_name: token_regex" to dict
			self.tokens_dict[token[0]] = regex

		# save split source file and current index for next_token
		source_f = open(source_file, 'r').read()
		self.source = [word for line in source_f.splitlines() for word in line.split()]
		self.current_index = 0
		
	def next_token(self):

		# no more tokens in the source file, raise EOFError
		if len(self.source) == 0:
			raise EOFError

		token_type = None
		token_value = None
		max_length = 0

		#if self.current_index < len(self.source):
		current_token = self.source[0]

		for name, regex in self.tokens_dict.items():
			
			for i in range(self.current_index, len(current_token) + 1):

				# simulate regex on substring
				if regex.simulate(current_token[self.current_index: i]) and (i - self.current_index > max_length):
					# if longest match
					token_type = name
					token_value = current_token[self.current_index: i]
					max_length = i - self.current_index

		# moving to the next token
		if max_length == len(current_token) - self.current_index:
			self.source.pop(0)
			self.current_index = 0

		else:
			self.current_index += max_length

		# if not token, raise invalid
		if token_type is None:
			raise InvalidToken

		return (token_type, token_value)
		
# You will likely add other classes, drawn from code from your previous 
# assignments.

if __name__ == "__main__":
	num = 18   # can replace this with any number 1, ... 20.
			  # can also create your own test files.
	reg_ex_filename = f"regex{num}.txt" 
	source_filename = f"src{num}.txt"
	lex = Lex(reg_ex_filename, source_filename)

	print(lex.next_token())
