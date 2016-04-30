from GrammarCreator import *
from TreebankParser import TreebankParser
import sys
import pickle


tbparser = TreebankParser()
test = True


# Count occurances of grammar rules
print ">>GRAMMARCREATOR: Counting the grammar rule occurances."
counted_grammar = tbparser.new_treebank_parser("ddt-1.0.xml")
counted_grammar.print_counted_grammar()
if test: raw_input("continue?")

print ">>GRAMMARCREATOR: Mapping the DDT tags to CST nonterminal tags."
terminal_grammar = tbparser.map_DDT_tags_to_CST_terminals()

print ">>GRAMMARCREATOR: Appending the two grammars."
# Adding the tag mapping to the counted grammar
for gr in terminal_grammar.rules:
	counted_grammar.rules[gr] = 1

counted_grammar.print_counted_grammar()
if test: raw_input("continue?")


print ">>GRAMMARCREATOR: Converting grammar to CNF and normalizing probabilities."
final_grammar = convert_to_probabilistic_chomsky(counted_grammar)

final_grammar.print_grammar()

if test: sys.exit()


with open("grammar.out", 'w') as outputfile:
	pickle.dump(final_grammar, outputfile)


