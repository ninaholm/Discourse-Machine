# -*- coding: utf-8 -*-

import pickle
from Grammar import *
from treelib import Node, Tree



class SyntacticParser(object):

	def __init__(self):
		self.grammar = self._import_grammar()

	# run() method
	def parse_sentence(self, sentence):
		m = self._cky_parse(sentence)
		if m is None: return None
		return self.build_sentence_tree(m)


	# Takes a sentence string, runs CKY and returns the sentence matrix of said sentence.
	def _cky_parse(self, sentence):
		cdef int i, j, sentence_length, k

		n = len(sentence)+1
		grammar_rules = self.grammar.rules.copy() # NOTE: DOUBLE CHECK THIS
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
				sentence_matrix[1][i][r.rule_head] = ([r.rule_head, 1, None, None])

		# Run the CKY algorithm
		cdef int substring_length, substring_start, split_point
		for substring_length in xrange(2, n):
			for substring_start in xrange(1, (n - substring_length)+1):
				for split_point in xrange(1, substring_length):
					b_dict = sentence_matrix[split_point][substring_start]
					c_dict = sentence_matrix[substring_length - split_point][substring_start + split_point]

					uniquecrossproduct = [(b, c) for b in b_dict.keys() for c in c_dict.keys()]

					for bc in uniquecrossproduct:
						if bc in grammar_rules:
							k = len(grammar_rules[bc])
							bc_prob = float(b_dict[b][1]) * float(c_dict[c][1])

							# DO NOT DO THE FUCKING COORDINATES
							b_option_coord = [split_point, substring_start, bc[0]]
							c_option_coord = [substring_length - split_point, substring_start + split_point, bc[1]]
							
							rules = [x.rule_head for x in grammar_rules[bc]]
							probs = [(x.prob * bc_prob) for x in grammar_rules[bc]]

							for j in range(k):
								new_rule = [rules[j], probs[j], b_option_coord, c_option_coord]
								if rules[j] in sentence_matrix[substring_length][substring_start]:
									if sentence_matrix[substring_length][substring_start][rules[j]][1] < probs[j]:
										sentence_matrix[substring_length][substring_start][rules[j]] = new_rule
								else: sentence_matrix[substring_length][substring_start][rules[j]] = new_rule

		if len(sentence_matrix[len(sentence_matrix)-1][1]) == 0: 
			return None
		return sentence_matrix


	# Returns a dictionary containing the grammar used by the CKY parser
	def _import_grammar(self):
		with open("SyntacticParser/grammar.in", "r") as gfile:
			g = pickle.load(gfile)
		
		# Transform grammar to tuple based grammar
		# new_grammar = Grammar()
		# for bc_key in g.rules:
		# 	for rule in g.rules[bc_key]:
		# 		if len(rule.constituents) == 2:
		# 			tpl = (rule.constituents[0], rule.constituents[1])
		# 			if tpl in new_grammar.rules: new_grammar.rules[tpl].append(rule)
		# 			else: new_grammar.rules[tpl] = [rule]
		# 		else:
		# 			c = rule.constituents[0]
		# 			if c in new_grammar.rules: new_grammar.rules[c].append(rule)
		# 			else: new_grammar.rules[c] = [rule]

		# return new_grammar
		return g

	# Builds sentence tree from sentence_matrix
	def build_sentence_tree(self, sentence_matrix):
		st = SentenceTree()
		st.build_tree(sentence_matrix)
		return st



class SentenceTree(object):

	def __init__(self):
		self.tree = Tree()
		self.sentence = []
		self.matrix = []
		

	# Builds a tree by backtracking the sentence matrix
	def build_tree(self, sentence_matrix):
		self.matrix = sentence_matrix
		sentence_length = len(sentence_matrix)-1

		# Saves the ST's sentence as a list of strings
		for i in range(1,sentence_length+1):
			self.sentence.append(self.matrix[0][i][0])

		# Finds the most probable sentence option
		options = sentence_matrix[sentence_length][1]
		maximum_prob = max([y[1] for y in options.values()])
		max_option = [options[x] for x in options if options[x][1]==maximum_prob][0]

		# Builds the tree
		self._nid = sentence_length+1
		root = max_option
		self.tree.create_node(root[0], self._nid)
		self._create_children(root, self._nid) # Call recursive function


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
				left_coord = parse_option[2]
				right_coord = parse_option[3]
				left_child = self.matrix[left_coord[0]][left_coord[1]][left_coord[2]]
				right_child = self.matrix[right_coord[0]][right_coord[1]][right_coord[2]]

				# Create left child as node (plus extra word node if leaf)
				cid = self._nnid()
				self.tree.create_node(left_child[0], cid, parent=pid)
				if left_child[2] is None: #If left_child is a leaf node, append a word node
					nid = left_coord[1]-1
					word = self.matrix[left_coord[0]-1][left_coord[1]][0]
					word = word.decode('utf-8', "ignore")
					self.tree.create_node(word, nid, parent=cid)
				else:
					self._create_children(left_child, cid) # Create children of left_child

				# Create right child as node (plus extra word node if leaf)
				cid = self._nnid()
				self.tree.create_node(right_child[0], cid, parent=pid)
				if right_child[2] is None: #If right_child is a leaf node, append a word node
					nid = right_coord[1]-1
					word = self.matrix[right_coord[0]-1][right_coord[1]][0]
					word = word.decode('utf-8', "ignore")
					self.tree.create_node(word, nid, parent=cid)
				else:
					self._create_children(right_child, cid) # Create children of right_child



	# Returns the sentence's sentiment score
	def get_sentiment_score(self, sentimentDict, term):
		total_score = 0

		# placeholder dictionaries -TESTING PURPOSES
		negationList = ["ikke", "ej"]

		# Check the term against every sentiment word
		n1 = self.sentence.index(term)
		for word in sentimentDict:
			if term==word: continue # If topic term is an opinion word, ignore.
			n2 = self._in_sentence(word)
			if n2 is not False:
				d = self._get_distance(n1, n2)
				score = float(sentimentDict[word]) / float(d)

				# If SentWord is negated, flip the score derived from it
				if self._is_negated(word, negationList):
					score = score * -1

				print "Term: %s | SentWord: %s | Distance: %s | Score: %s" % (term, word, d,score)
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
		return abs(distance)


	# Returns lowest common ancestor of two nodes n1 and n2
	# Supporting method of _get_distance()
	def _get_LCA(self, current_node, n1, n2):
		if current_node is None: return None
		if current_node == n1 or current_node == n2: return current_node
		if len(self.tree.get_node(current_node).fpointer) == 0: return None #if leaf, return None
		if len(self.tree.get_node(current_node).fpointer) == 1: #if terminal node, check its single leaf node
			return self._get_LCA(self.tree.get_node(current_node).fpointer[0], n1, n2)

		if len(self.tree.get_node(current_node).fpointer) == 2:
			left = self._get_LCA(self.tree.get_node(current_node).fpointer[0],n1,n2)
			right = self._get_LCA(self.tree.get_node(current_node).fpointer[1],n1,n2)

		if left is not None and right is not None: return current_node
		if left is not None: return left
		if right is not None:return right

		return None

