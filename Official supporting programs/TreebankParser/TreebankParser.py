from bs4 import BeautifulSoup
import time
import pickle
import sys
import csv


class TreebankParser(object):

	def __init__(self):
		self.log = Logger()


	def extract_terminals(self, treebank_filename):
		with open("ddt-1.0.xml", "r") as file:
			treebank = BeautifulSoup(file.read(), "xml")

		terminals = {}
		for sentence in treebank.findAll('s'):
			terminals_xml = sentence.findAll('t')
			ve_test = False
			for t in terminals_xml:
				cat = t.get('cat')
				if cat in terminals:
					terminals[cat].append(t.get('lemma').encode('utf8'))
				else:
					terminals[cat] = [t.get('lemma').encode('utf8'),]

		return terminals



	def parse_treebank(self, treebank_filename):

		# Reading and xml-parsing the DDT file
		print ">>TREEBANK: Reading and xml-parsing the DDT file."
		with open(treebank_filename, "r") as file:
			treebank = BeautifulSoup(file.read(), "xml")
		print ">>LOG: Time spent is %s seconds" % self.log.time_since_last_check()

		grammar = Grammar()

		# Extracting grammar from sentences
		print ">>TREEBANK: Extracting grammar from sentences."
		for sentence in treebank.findAll('s'):
			terminals = {}
			nonterminals = {}
			# extract terminals
			terminals_xml = sentence.findAll('t')
			for t in terminals_xml:
				terminal = Terminal(t.get('id'), t.get('cat'), t.get('lemma'), t.get('word'))
				terminals[terminal.id] = terminal

			# extract nonterminals
			nonterminals_xml = sentence.findAll('nt')
			for nt in nonterminals_xml:
				nonterminal = Nonterminal(nt.get('id'), nt.get('cat'), nt.get('lemma'), nt.get('word'))
				edges = []
				for e in nt.findAll('edge'):
					edges.append([e.get('idref'), e.get('label')])
				nonterminal.add_edges(edges)
				nonterminals[nonterminal.id] = nonterminal

			# Count edge --> nonterminals
			for nt in nonterminals:
				edge_startpoint_cat = nonterminals[nt].category
				for e in nonterminals[nt].edges:
					if e[0] in nonterminals:
						edge_endpoint_cat = nonterminals[e[0]].category
					else:
						edge_endpoint_cat = terminals[e[0]].category

					gr = GrammarRule(e[1], [edge_startpoint_cat, edge_endpoint_cat])
					grammar.count_rule(gr)

			# Count nonterminal --> edges
			for nt in nonterminals:			
				if len(nonterminals[nt].edges) > 1:
					constituents = []
					for e in nonterminals[nt].edges:
						if e[1] != "--":
							constituents.append(e[1])

					gr = GrammarRule(nonterminals[nt].category, constituents)
					grammar.count_rule(gr)

		
		print ">>LOG: Time spent is %s seconds" % self.log.time_since_last_check()
		grammar.print_grammar()

		print ">>TREEBANK: Pickling the temporary grammar."
		with open("grammar.out", "w") as file:
			pickle.dump(grammar, file)
		print ">>LOG: Time spent is %s seconds" % self.log.time_since_last_check()

		print ">>TREEBANK: Done. Total runtime %s seconds" % (time.time() - self.log.starttime)

		return grammar




	def map_DDT_tags_to_CST_terminals(self):
		grammar = Grammar()
		with open("DDT-to-CST-mapping.csv", "r") as file:
			data = csv.reader(file)

			for row in data:
				gr = GrammarRule(row[1], [row[0]])
				grammar.rules[gr] = 1

		grammar.print_grammar()
		return grammar





class Terminal(object):
	def __init__(self, id, category, lemma, word):
		self.id = id
		self.category = category
		self.lemma = lemma
		self.word = word
		self.edges = []

	def print_info(self):
		print "ID: %s \t CAT: %s \t LEMMA: %s \t WORD: %s" % (self.id, self.category, self.lemma, self.word)


class Nonterminal(Terminal):
	def add_edges(self, edges_input):
		self.edges = edges_input




class GrammarRule(object):
	def __init__(self, left_side, constituents):
		self.constituents = constituents
		self.left_side = left_side

	def print_rule(self):
		s = self.left_side + " --->"
		for c in self.constituents:
			s = s + " " + c
		return s

	def __hash__(self):
		return hash((str(self.constituents), self.left_side))

	def __eq__(self, other):
		return (str(self.constituents), self.left_side) == (str(self.constituents), self.left_side)


class Grammar(object):
	def __init__(self):
		self.rules = {}

	def count_rule(self, gr):
		if gr in self.rules:
			self.rules[gr] = self.rules[gr] + 1
		else:
			self.rules[gr] = 1

	def print_grammar(self):
		for rule in self.rules:
			print rule.print_rule(), " \t", self.rules[rule]






class Logger(object):
	def __init__(self):
		self.time_keeper = time.time()
		self.starttime = time.time()

	def time_since_last_check(self):
		t = (time.time() - self.time_keeper)
		self.time_keeper = time.time()
		return t


tp = TreebankParser()
g = tp.map_DDT_tags_to_CST_terminals()
g.print_grammar()




