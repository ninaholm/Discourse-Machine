import sys
import polyglot
from polyglot.text import Text, Word
from polyglot.mapping import Embedding
import pickle
import random
import time
import re





def build_sentence_matrix(n):
	return [[[] for x in range(n)] for y in range(n)]
#	return [["[" +str(x) + "," + str(y) + "]" for x in range(n)] for y in range(n)]


def print_matrix(sentence_matrix):
	for entry in sentence_matrix:
		for cell in entry:
			print cell, "\t",
		print


def build_grammar():
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




def cky_parse():

	print ">>PARSE: Starting the syntactic parsing..."
	grammar = build_grammar()

	# Set variables
	sentence = "Jeg er en glad studerende" # Set simple test sentence
	pos_sentence = Text(sentence).pos_tags # POS-tag sentence
	sentence_matrix = build_sentence_matrix(len(pos_sentence)+1) # Create CKY matrix
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
						if grammar_rule in grammar:
							for nonterminal in grammar[grammar_rule]:
								prob = b_option.probability * c_option.probability * nonterminal[1]
								b_option_coord = [split_point, substring_start, b.index(b_option)]
								c_option_coord = [substring_length - split_point, substring_start + split_point, c.index(c_option)]
								po = ParseOption(nonterminal[0], prob, b_option_coord, c_option_coord)
								sentence_matrix[substring_length][substring_start].append(po)


	print ">>PARSE: The finished CKY parse table:"
	print_matrix(sentence_matrix)
	print

	return sentence_matrix






# Object for storing all relevant information about a potential constituent within the sentence_matrix
class ParseOption(object):
	def __init__(self, const, prob, left, right):
		self.constituent = const
		self.probability = prob
		self.left_coord = left
		self.right_coord = right

	def __repr__(self):
		return self.constituent + " " + str(self.probability)


# Binary tree for extracting the most probably parse of a sentence in the sentence_matrix
class Tree(object):
	def __init__(self, sentence_matrix):
		self.matrix = sentence_matrix

	def build_tree(self, parse_root):
		self.root = self.create_node(parse_root)


	def create_node(self, parse_option):
		if parse_option is None:
			return None
		else:
			value = parse_option.constituent
			if parse_option.left_coord is not None:
				left_child = self.matrix[parse_option.left_coord[0]][parse_option.left_coord[1]][parse_option.left_coord[2]]
				right_child = self.matrix[parse_option.right_coord[0]][parse_option.right_coord[1]][parse_option.right_coord[2]]
				return Node(value, self.create_node(left_child), self.create_node(right_child))
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

		







sentence_matrix = cky_parse()
sentence_length = len(sentence_matrix)-1

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







# The very first, simple CKY implementation
def non_probabilistic_CKY(sentence):

	grammar_tree = build_grammar()

	pos_sentence = Text(sentence).pos_tags # POS-tag sentence
	sentence_matrix = build_sentence_matrix(len(pos_sentence)+1)
	sentence_length = len(pos_sentence)

	# Fill out the NTs resolving to terminals
	for i in range(1, sentence_length+1):
		sentence_matrix[1][i].append([pos_sentence[i-1][1], 1])

	# GO GO CKY ALGORITHM
	for substring_length in range(2, sentence_length+1):
		for substring_start in range(1, (sentence_length - substring_length)+2):
			for split_point in range(1, substring_length):
				b = sentence_matrix[split_point][substring_start]
				c = sentence_matrix[substring_length - split_point][substring_start + split_point]
				if grammar_rule in grammar_tree:
					sentence_matrix[substring_length][substring_start] = grammar_tree[grammar_rule]
		print_matrix(sentence_matrix)




