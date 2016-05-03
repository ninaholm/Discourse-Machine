from GrammarComb import Grammar, GrammarRule
import pickle
import os
import sys

def testlol(self):
	inputfile = open(os.getcwd() + "/SyntacticParser/grammar.in", 'rb')
	g = Grammar()
	print g
	sys.module['Grammar'] = SyntacticParser.GrammarComb.Grammar
 
	grammar = pickle.load(inputfile)
	inputfile.close()

	for lol in grammar.rules:
		print lol