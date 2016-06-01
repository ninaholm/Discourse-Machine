# -*- coding: utf-8 -*-

import pickle
from Grammar import *
from SentenceTree import SentenceTree
from datetime import datetime, timedelta

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
		grammar_rules = dict(self.grammar)
		sentence_matrix = [[{} for x in range(n)] for y in range(n)] # Create CKY matrix
		sentence_length = len(sentence)
		
		# Fill out the NTs resolving to terminals
		for i in range(1, sentence_length+1):
			if sentence[i-1][1] not in grammar_rules: # ignore non-existing tags
				print ">>PARSE: Encountered illegal tag: %s. Disregarding sentence." % sentence[i-1][1]
				print sentence
				return None

			sentence_matrix[0][i][0] = (sentence[i-1][0]) # Enter word into sentence matrix
			for j in range(len(grammar_rules[sentence[i-1][1]])):
				r = grammar_rules[sentence[i-1][1]][j]
				# 0: rulehead | 1: probability | 2: left coordinates | 3: right coordinates
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
							bc_prob = float(b_dict[bc[0]][1]) * float(c_dict[bc[1]][1])

							b_option_coord = [split_point, substring_start, bc[0]]
							c_option_coord = [substring_length - split_point, substring_start + split_point, bc[1]]
							
							rules = [x.rule_head for x in grammar_rules[bc]]
							probs = [(x.prob * bc_prob) for x in grammar_rules[bc]]

							for j in range(k):
								# 0: rulehead | 1: probability | 2: left coordinates | 3: right coordinates
								new_rule = [rules[j], probs[j], b_option_coord, c_option_coord]
								if rules[j] in sentence_matrix[substring_length][substring_start]:
									if sentence_matrix[substring_length][substring_start][rules[j]][1] < probs[j]:
										sentence_matrix[substring_length][substring_start][rules[j]] = new_rule
								else: sentence_matrix[substring_length][substring_start][rules[j]] = new_rule


		if len(sentence_matrix[len(sentence_matrix)-1][1]) == 0:
			return None
		return sentence_matrix



	def _print_matrix(self, sentence_matrix):
		for row in sentence_matrix[1:]:
			maximums = []
			for cell in row:
				lst = [cell[k] for k in cell.keys()]
				cell_to_print = "[-- 0.00]"
				if len(lst) > 0:
					maximum = [(x[0][:2], str(round(x[1], 2))) for x in lst if x[1]==max([x[1] for x in lst])][0]
					cell_to_print = "[" + " ".join(maximum) + "]"
				maximums.append(cell_to_print)
			print " ".join(maximums)



	# Returns a dictionary containing the grammar used by the CKY parser
	def _import_grammar(self):
		with open("SyntacticParser/grammar.in", "r") as gfile:
			grammar = pickle.load(gfile)
		
		return grammar

	# Builds sentence tree from sentence_matrix
	def build_sentence_tree(self, sentence_matrix):
		st = SentenceTree()
		st.build_tree(sentence_matrix)
		return st
