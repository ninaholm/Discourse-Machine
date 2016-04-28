import polyglot
from polyglot.text import Text, Word




class SyntacticParser(object):

	def __init__(self):
		self.grammar = self._import_grammar()

	# run() method
	def parse_sentence(self, sentence):
		return self.build_sentence_tree(self.cky_parse(sentence))

	# Takes a sentence string and returns a POS-tagged version of said sentence (as a list of word:tag tuples)
	# Can be replaced with another POS-tagger
	def postag_sentence(self, sentence):
		return Text(sentence).pos_tags


	# Takes a sentence string, runs CKY and returns the sentence matrix of said sentence.
	def cky_parse(self, sentence):
		print ">>PARSE: Starting the syntactic parsing..."
		
		# Set variables
		pos_sentence = self.postag_sentence(sentence)
		n = len(pos_sentence)+1
		sentence_matrix = [[[] for x in range(n)] for y in range(n)] # Create CKY matrix
		sentence_length = len(pos_sentence)

		# Fill out the NTs resolving to terminals
		print ">>PARSE: Now parsing the sentence \'%s\'" % (sentence)
		for i in range(1, sentence_length+1):
			po = ParseOption(pos_sentence[i-1][1], 1, None, None)
			sentence_matrix[1][i].append(po)

		# GO GO CKY ALGORITHM DO YO' THANG
		for substring_length in range(2, sentence_length+1):
			for substring_start in range(1, (sentence_length - substring_length)+2):
				for split_point in range(1, substring_length):
					b = sentence_matrix[split_point][substring_start]
					c = sentence_matrix[substring_length - split_point][substring_start + split_point]
					for b_option in b:
						for c_option in c:
							grammar_rule = (str(b_option.constituent) + " " + str(c_option.constituent))
							if grammar_rule in self.grammar:
								for nonterminal in self.grammar[grammar_rule]:
									prob = b_option.probability * c_option.probability * nonterminal[1]
									b_option_coord = [split_point, substring_start, b.index(b_option)]
									c_option_coord = [substring_length - split_point, substring_start + split_point, c.index(c_option)]
									po = ParseOption(nonterminal[0], prob, b_option_coord, c_option_coord)
									sentence_matrix[substring_length][substring_start].append(po)

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
		grammar_rules = []
		grammar_dict = {}

		grammar_dict["NP VP"] = [["S", 0.4],]
		grammar_dict["NEXUS VP"] = [["S", 0.2],]
		grammar_dict["VERB NP"] = [["VP", 0.4],]
		grammar_dict["PRON NOM"] = [["NP", 0.4], ["NOM", 0.6]]
		grammar_dict["ADJ NOUN"] = [["NOM", 0.4],]
		grammar_dict["ADP PROPN"] = [["PP", 0.4],]
		grammar_dict["NP PP"] = [["NP", 0.4],]
		grammar_dict["PRON VERB"] = [["NEXUS", 0.4],]
		grammar_dict["NP VERB"] = [["NEXUS", 0.4],]
		grammar_dict["NEXUS NP"] = [["S", 0.4],]
		grammar_dict["NEXUS VP"] = [["S", 0.4],]
		grammar_dict["PRON NOUN"] = [["NP", 0.4],]
		grammar_dict["VERB ADJ"] = [["VP", 0.4],]
		grammar_dict["PRON VP"] = [["S", 0.2],]


		return grammar_dict




	def build_sentence_tree(self, sentence_matrix):
		sentence_length = len(sentence_matrix)-1

		print sentence_matrix[sentence_length][1]

		if len(sentence_matrix[sentence_length][1])==0:
			print ">>PARSE: No legal parse tree for this sentence."
			return None

		print ">>PARSE: Building the syntactic tree."
		# Extracting the most probably sentence structure as a binary tree
		tree = Tree(sentence_matrix)
		maximum = 0
		index = None
		for option in sentence_matrix[sentence_length][1]: # Find the maximum probable S
			if option.probability > maximum:
				maximum = option.probability
				index = sentence_matrix[sentence_length][1].index(option)
		tree.build_tree(sentence_matrix[sentence_length][1][index])

		print ">>PARSE: Printing the syntactic tree..."
		tree.print_tree()

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
				return Node(value, self._create_node(left_child), self._create_node(right_child))
			else:
				return Node(value, None, None)

	def print_tree(self):
		thislevel = [self.root]
		while thislevel:
			nextlevel = list()
			for n in thislevel:
				print n.value,
				if n.left_child: nextlevel.append(n.left_child)
				if n.right_child: nextlevel.append(n.right_child)
			print
			thislevel = nextlevel

class Node(object):
	def __init__(self, value, left_child, right_child):
		self.value = value
		self.left_child = left_child
		self.right_child = right_child


