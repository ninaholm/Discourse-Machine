from GrammarCreator import *
from TreebankParser import TreebankParser
import sys
import pickle


tbparser = TreebankParser()
test = False


# Count occurances of grammar rules
print ">>GRAMMARCREATOR: Counting the grammar rule occurances."
counted_grammar = tbparser.new_treebank_parser("ddt-1.0.xml")
if test: counted_grammar.print_counted_grammar()
if test: raw_input("Counted grammar printed. continue?")

print ">>GRAMMARCREATOR: Mapping the DDT tags to CST nonterminal tags."
terminal_grammar = tbparser.map_DDT_tags_to_CST_terminals()
if test: terminal_grammar.print_counted_grammar()
if test: raw_input("Terminal grammar printed. continue?")

print ">>GRAMMARCREATOR: Appending the two grammars."
# Adding the tag mapping to the counted grammar
for gr in terminal_grammar.rules:
	counted_grammar.rules[gr] = 1

# counted_grammar.print_counted_grammar()
if test: counted_grammar.print_counted_grammar()
if test: raw_input("Appended grammar printed. continue?")


print ">>GRAMMARCREATOR: Converting grammar to CNF and normalizing probabilities."
cnfgrammar = convert_to_probabilistic_chomsky(counted_grammar)

print ">>GRAMMARCREATOR: Compressing grammar."
final_grammar = compress(cnfgrammar)


final_grammar.print_grammar()


with open("grammar.out", 'w') as outputfile:
	pickle.dump(final_grammar, outputfile)


