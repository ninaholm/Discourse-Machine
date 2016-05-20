# -*- coding: utf-8 -*-

import pickle
from Grammar import *
import sys
from datetime import datetime, timedelta
from treelib import Node, Tree
import math
import numpy as np
cimport numpy as np


class SyntacticParser(object):

	def __init__(self):
		self.grammar, self.reverse_grammar = self._import_grammar()
		self.log = Logger()
		self.cky_logger = Logger()
		self.tree_logger = Logger()
		self.cky_logger1 = Logger()
		self.cky_logger2 = Logger()

		self.test = False
		self.print_all = False

	# run() method
	def parse_sentence(self, sentence):
		m = self.cky_parse(sentence)
		if m is None: return None
		return self.build_sentence_tree(m)


	# Takes a sentence string, runs CKY and returns the sentence matrix of said sentence.
	def cky_parse(self, sentence):
		if self.test: print ">>PARSE: Running with test ON."
		cdef int i, j, sentence_length, k
		self.cky_logger.start_timer()

		n = len(sentence)+1
		grammar_rules = self.grammar.rules
		sentence_matrix = [[{} for x in range(n)] for y in range(n)] # Create CKY matrix
		sentence_length = len(sentence)

		# Fill out the NTs resolving to terminals
		for i in range(1, sentence_length+1):
			if sentence[i-1][1] not in grammar_rules: # IGNORE NON-EXISTiNG TAGS
				print ">>PARSE: Encountered illegal tag: %s. Disregarding sentence." % sentence[i-1][1]
				print sentence
				return None
			sentence_matrix[0][i][0] = (sentence[i-1][0]) # Enter word into sentence matrix

			for j in range(len(grammar_rules[sentence[i-1][1]])):
				r = grammar_rules[sentence[i-1][1]][j]
				# 0: leftside | 1: probability | 2: left coordinates | 3: right coordinates
				sentence_matrix[1][i][r.left_side] = ([r.left_side, 1, None, None])


		# GO GO CKY ALGORITHM DO YO' THANG
		cdef int substring_length, substring_start, split_point
		
		for substring_length in xrange(2, sentence_length+1):
			for substring_start in xrange(1, (sentence_length - substring_length)+2):
				for split_point in xrange(1, substring_length):
					b_dict = sentence_matrix[split_point][substring_start]
					c_dict = sentence_matrix[substring_length - split_point][substring_start + split_point]

					crossproduct = [(b, c) for b in b_dict.keys() for c in c_dict.keys()]
					uniquecrossproduct = list(set(crossproduct))
					
					for i in range(len(uniquecrossproduct)):
						grammar_rule = "".join(uniquecrossproduct[i])
						
						if grammar_rule in grammar_rules:
							k = len(grammar_rules[grammar_rule])
							b, c = uniquecrossproduct[i]

							b_option_coord = ":".join(map(str, [split_point, substring_start, b]))
							c_option_coord = ":".join(map(str, [substring_length - split_point, substring_start + split_point, c]))

							cb_prob = float(b_dict[b][1]) * float(c_dict[c][1])

							rules = [x.left_side for x in grammar_rules[grammar_rule]]
							probs = [(x.prob * cb_prob) for x in grammar_rules[grammar_rule]]

							for j in range(k):
								new_row = [rules[j], probs[j], b_option_coord, c_option_coord]
								if rules[j] in sentence_matrix[substring_length][substring_start]:
									if sentence_matrix[substring_length][substring_start][rules[j]][1] < probs[j]:
										sentence_matrix[substring_length][substring_start][rules[j]] = new_row
								else: sentence_matrix[substring_length][substring_start][rules[j]] = new_row

		self.cky_logger.stop_timer()
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
		
		reverse_grammar = {}
		for lookup in g.rules:
			for gr in g.rules[lookup]:
				if gr.left_side not in reverse_grammar:
					reverse_grammar[gr.left_side] = [gr]
				else:
					reverse_grammar[gr.left_side].append(gr)

		for nt in reverse_grammar:
			reverse_grammar[nt].sort(key=lambda x: x.prob, reverse=True)

		return (g, reverse_grammar)

	# Builds sentence tree from sentence_matrix. Returns none if no probable parse
	def build_sentence_tree(self, sentence_matrix):
		self.tree_logger.start_timer()
		if len(sentence_matrix[len(sentence_matrix)-1][1]) == 0:
			return None
		st = SentenceTree()
		st.build_tree(sentence_matrix)
		self.tree_logger.stop_timer()
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

		# Find the most probable sentence option
		maximum = 0
		index = None

		options = sentence_matrix[sentence_length][1]
		max_option = [options[x] for x in options if options[x][1]==max([y[1] for y in options.values()])][0]

		# Build the tree
		self._nid = sentence_length+2
		root = max_option
		self.tree.create_node(root[0], self._nid)
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
			if parse_option[2] is not None:
				left_coord = parse_option[2].split(":")
				left_coord[:2] = map(int, [left_coord[0], left_coord[1]])
				right_coord = parse_option[3].split(":")
				right_coord[:2] = map(int, [right_coord[0], right_coord[1]])

				left_child = self.matrix[left_coord[0]][left_coord[1]][left_coord[2]]
				right_child = self.matrix[right_coord[0]][right_coord[1]][right_coord[2]]

				# Create left child as node (plus extra word node if leaf)
				cid = self._nnid()
				self.tree.create_node(left_child[0], cid, parent=pid)
				if left_child[2] is None: #If left_child is a leaf node, append a word node
					nid = left_coord[1]-1
					word = self.matrix[left_coord[0]-1][left_coord[1]][0]
					word = word.decode('utf-8')
					self.tree.create_node(word, nid, parent=cid)
				else:
					self._create_children(left_child, cid) # Create children of left_child

				# Create right child as node (plus extra word node if leaf)
				cid = self._nnid()
				self.tree.create_node(right_child[0], cid, parent=pid)
				if right_child[2] is None: #If left_child is a leaf node, append a word node
					nid = right_coord[1]-1
					word = self.matrix[right_coord[0]-1][right_coord[1]][0]
					word = word.decode('utf-8')
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
				if d==0: score = float(sentimentDict[key])
				else: score = float(sentimentDict[key]) / float(d)

				# If SentWord is negated, flip the score derived from it
				if self._is_negated(key, negationList):
					score = score * -1

				print "Term: %s | SentWord: %s | Distance: %s | Score: %s" % (term, key, d,score)
				total_score += score

		print "Total score:", total_score
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
