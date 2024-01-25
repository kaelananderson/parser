LR Grammar Parsing and Processing Repository

Overview
This repository contains a collection of Python modules and scripts that collectively contribute to parsing and processing LR grammars. The project includes the implementation of various aspects of computational linguistics and compiler design, such as lexical analysis, NFA and DFA simulations, regular expression processing, and error handling in grammar parsing.

Files Description
parse.py
Authors: Kaelan Anderson, Dillon Timmer
Last Modified: December 19, 2023
Description: This module is essential for parsing and processing LR grammars. It includes functionality to detect and handle non-LR grammars and identify syntax errors in source files. Key components include exception classes for specific parsing errors and the definition of an 'Item' class, representing individual rules within the LR automaton's states.

lexer.py
Authors: Kaelan Anderson, Dillon Timmer
Last Modified: November 30, 2023
Description: A Python program containing a class called Lex that serves as a rudimentary lexical analyzer generator. It reads specifications for token types defined by regular expressions and scans source files for these tokens.

nfa.py
Description: This script deals with the simulation of Non-deterministic Finite Automata (NFA). It includes functionalities for initializing NFAs from files, creating internal representations, and handling various NFA operations.

dfa.py
Authors: Kaelan Anderson, Dillon Timmer
Last Modified: September 21, 2023
Description: A program that reads in the contents of a file containing the information of a DFA (Deterministic Finite Automaton). It handles incorrectly formatted files and determines if an input string is in the language of the DFA.

regex.py
Authors: Kaelan Anderson, Dillon Timmer
Last Modified: November 7, 2023
Description: This program defines classes and methods to work with regular expressions and convert them into NFAs. It includes a Node class for creating a syntax tree from a regular expression, an NFA class to represent NFAs, and a RegEx class to process regular expressions and validate strings against them.

test_pa5.py
Author: Dr. John Glick
Description: A test script for the project. It tests the functionalities provided by the lexer.py and parse.py modules, ensuring the correct parsing and handling of LR grammars.

The repository also includes source files, grammer files, token files, and correct files that are used to run tests on the python source code to simulate how the LR parses computes. 

Usage
To run the project, access the test_pa5.py file that will simulate tests for all src.txt files. 
