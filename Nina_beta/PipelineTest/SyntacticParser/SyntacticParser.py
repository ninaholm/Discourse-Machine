import polyglot
from polyglot.text import Text, Word
import pickle
from Grammar import *
import sys
import time
from datetime import datetime, timedelta


class SyntacticParser(object):

	def __init__(self):
		self.grammar = self._import_grammar()
		self.log = Logger()
		self.cky_logger = Logger()
		self.grammar_logger = Logger()
		self.tree_logger = Logger()
		self.test = False
		self.print_all = False

	# run() method
	def parse_sentence(self, sentence):
		m = self.cky_parse(sentence)
		if m is not None:
			return self.build_sentence_tree(m)
		else:
			return None

	# Takes a sentence string and returns a POS-tagged version of said sentence (as a list of word:tag tuples)
	# Can be replaced with another POS-tagger
	def postag_sentence(self, sentence):
		split = sentence.split(" ")
		output = []
		for s in split:
			n = s.split("/")
			if len(n) == 2:
				output.append(n)
		return output


	# Takes a sentence string, runs CKY and returns the sentence matrix of said sentence.
	def cky_parse(self, sentence):
		
		if self.print_all: print ">>PARSE: Starting the syntactic parsing..."
		if self.test: print ">>PARSE: Running with test ON."

		# Set variables
		pos_sentence = self.postag_sentence(sentence)
		n = len(pos_sentence)+1
		sentence_matrix = [[[] for x in range(n)] for y in range(n)] # Create CKY matrix
		sentence_length = len(pos_sentence)
		if self.print_all: print ">>LOG: Time spent POS-tagging:", self.log.time_since_last_check()

		# Fill out the NTs resolving to terminals
		if self.print_all: print ">>PARSE: Now parsing the sentence \'%s\'" % (sentence)
		for i in range(1, sentence_length+1):
			if pos_sentence[i-1][1] not in self.grammar.rules: # IGNORE NON-EXISTiNG TAGS
				return None
			r = self.grammar.rules[pos_sentence[i-1][1]][0].left_side # map the CST tag to DDT tag
			po = ParseOption(r, 1, None, None)
			po.own_coord = [1, i]
			sentence_matrix[0][i].append(pos_sentence[i-1][0])
			sentence_matrix[1][i].append(po)
		if self.print_all: print ">>LOG: Time spent mapping CST to DDT:", self.log.time_since_last_check()

		if self.test: self._print_matrix(sentence_matrix)

		self.cky_logger.start_timer()
		# GO GO CKY ALGORITHM DO YO' THANG
		for substring_length in range(2, sentence_length+1):
			for substring_start in range(1, (sentence_length - substring_length)+2):
				for split_point in range(1, substring_length):
					b = sentence_matrix[split_point][substring_start]
					c = sentence_matrix[substring_length - split_point][substring_start + split_point]
					for b_option in b:
						for c_option in c:
							grammar_rule = (str(b_option.constituent) + str(c_option.constituent))
							if grammar_rule in self.grammar.rules:
								self.grammar_logger.start_timer()
								if self.test: print "grammar rule exists: " + grammar_rule
								for nonterminal in self.grammar.rules[grammar_rule]:
									prob = b_option.probability * c_option.probability * nonterminal.prob
									b_option_coord = [split_point, substring_start, b.index(b_option)]
									c_option_coord = [substring_length - split_point, substring_start + split_point, c.index(c_option)]
									po = ParseOption(nonterminal.left_side, prob, b_option_coord, c_option_coord)
									sentence_matrix[substring_length][substring_start].append(po)
									if self.test: self._print_matrix(sentence_matrix)
								self.grammar_logger.stop_timer()

		if self.print_all: print ">>LOG: Time spent running CKY:", self.log.time_since_last_check()
		self.cky_logger.stop_timer()

		if self.print_all: print ">>GRAMMARLOG: Amount of time spent on grammar lookups:", self.grammar_logger.time_counter
		if self.test:
			print ">>PARSE: The finished CKY parse table:"
			self._print_matrix(sentence_matrix)
			print

		return sentence_matrix



	def _print_matrix(self, sentence_matrix):
		for entry in sentence_matrix:
			for cell in entry:
				print cell, "\t",
			print


	# Returns a dictionary containing the grammar used by the CKY parser
	def _import_grammar(self):
#		sys.modules['Grammar'] = Grammar
		with open("SyntacticParser/grammar.in", "r") as gfile:
			g = pickle.load(gfile)
		return g




	def build_sentence_tree(self, sentence_matrix):
		self.tree_logger.start_timer()
		sentence_length = len(sentence_matrix)-1

		if len(sentence_matrix[sentence_length][1])==0:
			print ">>PARSE: No legal parse tree for this sentence."
			return None

		if self.print_all: print ">>PARSE: Building the syntactic tree."
		# Extracting the most probably sentence structure as a binary tree
		tree = Tree(sentence_matrix)
		maximum = 0
		index = None
		for option in sentence_matrix[sentence_length][1]: # Find the maximum probable S
			if option.probability > maximum:
				maximum = option.probability
				index = sentence_matrix[sentence_length][1].index(option)
		tree.build_tree(sentence_matrix[sentence_length][1][index])

		self.tree_logger.stop_timer()
		if self.print_all: print ">>LOG: Time spent building the tree:", self.log.time_since_last_check()
		return tree





# Object for storing all relevant information about a potential constituent within the sentence_matrix
class ParseOption(object):
	def __init__(self, const, prob, left, right):
		self.constituent = const # non-terminal to which left+right might resolve
		self.probability = prob # probability of left+right resolving to this constituent
		self.left_coord = left # coordinates of the first right-side nonterminal
		self.right_coord = right # coordinates of the second right-side nonterminal

	def __repr__(self):
		return self.constituent + " " + str(self.probability)




# Binary tree for extracting the most probably parse of a sentence in the sentence_matrix
class Tree(object):
	def __init__(self, sentence_matrix):
		self.matrix = sentence_matrix
		self.size = 0

	# Builds a syntactic tree based on the ParseOption object for a legal S in the sentence_matrix.
	def build_tree(self, parse_root):
		self.root = self._create_node(parse_root)

	# recursive utility function for building the tree
	def _create_node(self, parse_option):
		if parse_option is None:
			return None
		else:
			value = parse_option.constituent
			if parse_option.left_coord is not None:
				left_child = self.matrix[parse_option.left_coord[0]][parse_option.left_coord[1]][parse_option.left_coord[2]]
				right_child = self.matrix[parse_option.right_coord[0]][parse_option.right_coord[1]][parse_option.right_coord[2]]
				self.size = self.size +1
				return Node(value, self._create_node(left_child), self._create_node(right_child))
			else:
				node = Node(value, None, None)
				node.leaf = True
				node.leaf_word = self.matrix[parse_option.own_coord[0]-1][parse_option.own_coord[1]][0]
				self.size = self.size +1
				return node

	def print_tree(self):
		print self.root.print_self(0)


class Node(object):
	def __init__(self, value, left_child, right_child):
		self.value = value
		self.left_child = left_child
		self.right_child = right_child
		self.leaf = False


	def print_self(self, depth,):
		ret = ""

		# Print right branch
		if self.right_child != None:
			ret += self.right_child.print_self(depth + 1)

		# Print own value
		ret += "\n" + ("    "*depth) + str(self.value)
		if self.right_child is None:
			ret += " --- " + str(self.leaf_word)

		# Print left branch
		if self.left_child != None:
			ret += self.left_child.print_self(depth + 1)

		return ret



class Logger(object):
	def __init__(self):
		self.time_keeper = datetime.now()
		self.starttime = datetime.now()
		self.time_counter = None

	def time_since_last_check(self):
		t = (datetime.now() - self.time_keeper)
		self.time_keeper = datetime.now()
		return t

	def start_timer(self):
		self.timer = datetime.now()

	def stop_timer(self):
		if self.time_counter is None:
			self.time_counter = datetime.now() - self.timer
		else:
			self.time_counter += datetime.now() - self.timer
