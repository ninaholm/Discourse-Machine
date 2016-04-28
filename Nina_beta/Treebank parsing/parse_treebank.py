from bs4 import BeautifulSoup
import time
import pickle
import sys



class TreebankParser(object):

	def __init__(self):
		self.log = Logger()


	def save_test_sentence(self):
		print ">>TREEBANK: Reading the DDT file."
		with open("ddt-1.0.xml", "r") as file:
			input_file = file.read()

		print ">>TREEBANK: Parsing file as xml"
		treebank = BeautifulSoup(input_file, "xml")

		sentence = treebank.find('s')
		with open("test_sentence", "w") as file:
			file.write(str(sentence))

		print ">>LOG: Time spent is %s seconds" % self.log.time_since_last_check()




	def extract_terminals(self):
		with open("ddt-1.0.xml", "r") as file:
#		with open("test_sentence", "r") as file:
			treebank = BeautifulSoup(file.read(), "xml")

		terminals = {}
		ve_sentences = []
		for sentence in treebank.findAll('s'):
			# extract terminals
			terminals_xml = sentence.findAll('t')
			ve_test = False
			for t in terminals_xml:
				cat = t.get('cat')
				if cat == 'VE':
					ve_test = True
				if cat in terminals:
					terminals[cat].append(t.get('word').encode('utf8'))
				else:
					terminals[cat] = [t.get('word').encode('utf8'),]

			if ve_test:
				sentence = ""
				for t in terminals_xml:
					sentence = sentence + " " + t.get('word').encode('utf8')
				ve_sentences.append(sentence)

		with open("terminals_output", "w") as file:
			for s in ve_sentences:
				file.write(s + "\n")

		sys.exit()


		with open("terminals_output", "w") as file:
			file.write("ALL TERMINAL CATEGORIES:\n")
			file.write(" ".join(terminals.keys()) + "\n\n\n")

			for k in terminals.keys():
				words = " ".join(terminals[k])
				file.write(str(k) + "\n" + words + "\n\n")



	def run(self):
		
		print ">>TREEBANK: Reading and xml-parsing the DDT file."
		with open("ddt-1.0.xml", "r") as file:
			treebank = BeautifulSoup(file.read(), "xml")
		print ">>LOG: Time spent is %s seconds" % self.log.time_since_last_check()

		counter = 0
		grammar = Grammar()

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
#		grammar.print_grammar()

		print ">>TREEBANK: Pickling the temporary grammar."
		with open("temp_grammar", "w") as file:
			pickle.dump(grammar, file)
		print ">>LOG: Time spent is %s seconds" % self.log.time_since_last_check()

		print ">>TREEBANK: Total runtime %s seconds" % (time.time() - self.log.starttime)







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
#tp.run()
#tp.extract_terminals()

# with open("temp_grammar", "r") as file:
# 	grammar = pickle.load(file)

# grammar.print_grammar()




import csv
def map_DDT_tags_to_CST_terminals():
	grammar = Grammar()
	with open("DDT-to-CST-mapping.csv", "r") as file:
		data = csv.reader(file)

		for row in data:
			gr = GrammarRule(row[1], [row[0]])
			grammar.rules[gr] = 1

	grammar.print_grammar()
	return grammar


map_DDT_tags_to_CST_terminals()
