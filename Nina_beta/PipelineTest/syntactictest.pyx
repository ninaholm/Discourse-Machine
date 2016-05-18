# -*- coding: utf-8 -*-

import pickle
from Grammar import *
import sys
from datetime import datetime, timedelta
from treelib import Node, Tree
import math


class SyntacticParser(object):

	def __init__(self):
		self.grammar = self._import_grammar()
		self.log = Logger()
		self.cky_logger1 = Logger()
		self.cky_logger2 = Logger()
		self.cky_logger3 = Logger()
		self.cky_logger4 = Logger()
		self.cky_logger5 = Logger()
		self.test = False
		self.print_all = False

	# run() method
	def parse_sentence(self, sentence):
		m = self.cky_parse(sentence)
		if m is not None:
			return self.build_sentence_tree(m)
		else:
			return None

	# Takes CST-tagged input string and returns a list of word:tag tuples
	def _postag_sentence(self, sentence):
		split = sentence.split(" ")
		output = []
		for s in split:
			n = s.split("/")
			if len(n) == 2:
				output.append(n)
		return output


	# Takes a sentence string, runs CKY and returns the sentence matrix of said sentence.
	def cky_parse(self, sentence):
		cdef int n, sentence_length, i

		n = len(sentence)+1
		sentence_matrix = [[[] for x in range(n)] for y in range(n)] # Create CKY matrix
		sentence_length = len(sentence)

		# Fill out the NTs resolving to terminals
		for i in range(1, sentence_length+1):
			if sentence[i-1][1] not in self.grammar.rules: # IGNORE NON-EXISTiNG TAGS
				print ">>PARSE: Encountered illegal tag: %s. Disregarding sentence." % sentence[i-1][1]
				print sentence
				return None
			sentence_matrix[0][i].append(sentence[i-1][0]) # Enter word into sentence matrix
			for r in self.grammar.rules[sentence[i-1][1]]:
				po = ParseOption(r.left_side, 1, None, None)
				po.own_coord = [1, i]		
				sentence_matrix[1][i].append(po)


		# GO GO CKY ALGORITHM DO YO' THANG
		cdef int substring_length, substring_start, split_point
		cdef float prob
		cdef str grammar_rule
		grammar_rules = self.grammar.rules
		for substring_length in range(2, sentence_length+1):
			for substring_start in range(1, (sentence_length - substring_length)+2):
				options = []
				for split_point in range(1, substring_length):
					b = sentence_matrix[split_point][substring_start]
					c = sentence_matrix[substring_length - split_point][substring_start + split_point]
					for i in range(len(b)):
						self.cky_logger1.start_timer()
						b_option_coord = [split_point, substring_start, i]
						self.cky_logger1.stop_timer()
						for j in range(len(c)):
							self.cky_logger1.start_timer()
							c_option_coord = [substring_length - split_point, substring_start + split_point, j]
							self.cky_logger1.stop_timer()
							self.cky_logger2.start_timer()
							grammar_rule = "".join([str(b[i].constituent), str(c[j].constituent)])
							self.cky_logger2.stop_timer()
							if grammar_rule in grammar_rules:
								for nonterminal in grammar_rules[grammar_rule]:
									self.cky_logger3.start_timer()
									prob = b[i].probability * c[j].probability * nonterminal.prob # Consider taking the log instead of multiplying (ONLY THIS YIELDS NEGATIVE VALUES)
									self.cky_logger3.stop_timer()
									self.cky_logger4.start_timer()
									po = ParseOption(nonterminal.left_side, prob, b_option_coord, c_option_coord)
									self.cky_logger4.stop_timer()
									options.append(po)

				self.cky_logger5.start_timer()
				options.sort(key=lambda x: x.probability, reverse=True)
				for o in options[:200]:
					sentence_matrix[substring_length][substring_start].append(o)
				self.cky_logger5.stop_timer()

		return sentence_matrix



	def _print_matrix(self, sentence_matrix):
		for entry in sentence_matrix:
			for cell in entry:
				print len(cell), "\t",
			print


	# Returns a dictionary containing the grammar used by the CKY parser
	def _import_grammar(self):
		with open("SyntacticParser/grammar.in", "r") as gfile:
			g = pickle.load(gfile)
		return g

	def build_sentence_tree(self, sentence_matrix):
		if len(sentence_matrix[len(sentence_matrix)-1][1]) == 0:
			return None
		st = SentenceTree()
		st.build_tree(sentence_matrix)
		return st



class SentenceTree(object):

	def __init__(self):
		self.tree = Tree()
		self.tree_logger = Logger()
		self.sentence = []
		

	# Builds a tree by backtracking the sentence matrix
	def build_tree(self, sentence_matrix):
		self.tree_logger.start_timer()
		self.matrix = sentence_matrix
		sentence_length = len(sentence_matrix)-1

		# Saves the ST's sentence as a list of strings
		for i in range(1,sentence_length+1):
			self.sentence.append(self.matrix[0][i][0])

		# Check if the sentence resolves to a tree
		if len(sentence_matrix[sentence_length][1])==0:
			return None

		# Find the most probable sentence option
		maximum = 0
		index = None
		for option in sentence_matrix[sentence_length][1]:
			if option.probability > maximum:
				maximum = option.probability
				index = sentence_matrix[sentence_length][1].index(option)

		if index is None:
			return None
		# Build the tree
		self._nid = sentence_length+2
		root = sentence_matrix[sentence_length][1][index]
		self.tree.create_node(root.constituent, self._nid)
		self._create_children(root, self._nid) # Call recursive function

		self.tree_logger.stop_timer()


	# Ensures unique node id in _create_children()
	def _nnid(self):
		self._nid +=1
		return self._nid


	# Recursive function which builds the children nodes of a given parse_option
	# and then builds their children
	def _create_children(self, parse_option, pid):
		if parse_option is None:
			return None
		else:
			# If parse_option has children, extract those
			if parse_option.left_coord is not None:
				left_child = self.matrix[parse_option.left_coord[0]][parse_option.left_coord[1]][parse_option.left_coord[2]]
				right_child = self.matrix[parse_option.right_coord[0]][parse_option.right_coord[1]][parse_option.right_coord[2]]

				# Create left child as node (plus extra word node if leaf)
				cid = self._nnid()
				self.tree.create_node(left_child.constituent, cid, parent=pid)
				if left_child.left_coord is None: #If left_child is a leaf node, append a word node
					nid = parse_option.left_coord[1]-1
					word = self.matrix[parse_option.left_coord[0]-1][parse_option.left_coord[1]][0]
					self.tree.create_node(word, nid, parent=cid)
				else:
					self._create_children(left_child, cid) # Create children of left_child

				# Create right child as node (plus extra word node if leaf)
				cid = self._nnid()
				self.tree.create_node(right_child.constituent, cid, parent=pid)
				if right_child.right_coord is None: #If left_child is a leaf node, append a word node
					nid = parse_option.right_coord[1]-1
					word = self.matrix[parse_option.right_coord[0]-1][parse_option.right_coord[1]][0]
					self.tree.create_node(word, nid, parent=cid)
				else:
					self._create_children(right_child, cid) # Create children of right_child



	# Returns the sentence's sentiment score
	def get_sentiment_score(self, sentimentDict, term):
		total_score = 0

		# placeholder dictionaries -TESTING PURPOSES
		negationList = ["ikke", "liden"]

		# Check the term against every sentiment word
		n1 = self.sentence.index(term)
		for key in sentimentDict:
			n2 = self._in_sentence(key)
			if n2 is not False:
				d = self._get_distance(n1, n2)
				score = float(sentimentDict[key]) / float(d)

				# If SentWord is negated, flip the score derived from it
				if self._is_negated(key, negationList):
					score = score * -1

				print ">>SENTIMENTSCORE: Term: %s | SentWord: %s | Distance: %s | Score: %s" % (term, key, d,score)
				total_score += score

		return total_score


	# Checks whether a word is within a specified threshold distance of a negation word
	def _is_negated(self, w, negationList):
		negationThreshold = 3
		n1 = self._in_sentence(w)
		if n1 is None: return False
		for nw in negationList:
			n2 = self._in_sentence(nw)
			if n2 is not None:
				if (self._get_distance(n1, n2)) < negationThreshold:
					print "negating word", w
					return True
		return False


	# Checks whether word w exists in the ST's sentence
	def _in_sentence(self, w):
		if w in self.sentence:
			return self.sentence.index(w)
		return False


	# Returns distance between two nodes n1 and n2
	def _get_distance(self, n1, n2):
		LCA = self._get_LCA(self.tree.root, n1, n2)
		distance = self.tree.depth(self.tree.get_node(n1)) + self.tree.depth(self.tree.get_node(n2))
		distance = distance - 2 * self.tree.depth(self.tree.get_node(LCA))
		return distance-2


	# Returns lowest common ancestor of two nodes n1 and n2
	# Supporting method of _get_distance()
	def _get_LCA(self, root, n1, n2):
		if root is None: return None
		if root == n1 or root == n2: return root
		if len(self.tree.get_node(root).fpointer) == 0: return None #if leaf, return None
		if len(self.tree.get_node(root).fpointer) == 1: #if terminal node, check its single leaf node
			return self._get_LCA(self.tree.get_node(root).fpointer[0], n1, n2)

		if len(self.tree.get_node(root).fpointer) == 2:
			left = self._get_LCA(self.tree.get_node(root).fpointer[0],n1,n2)
			right = self._get_LCA(self.tree.get_node(root).fpointer[1],n1,n2)

		if left is not None and right is not None: return root
		if left is not None: return left
		if right is not None:return right

		return None






# Object for storing all relevant information about a potential constituent within the sentence_matrix
class ParseOption(object):
	def __init__(self, str const, float prob, left, right):
		self.constituent = const # non-terminal to which left+right might resolve
		self.probability = prob # probability of left+right resolving to this constituent
		self.left_coord = left # coordinates of the first right-side nonterminal
		self.right_coord = right # coordinates of the second right-side nonterminal

	def __repr__(self):
		return self.constituent + " " + str(self.probability)




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
