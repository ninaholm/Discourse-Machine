# -*- coding: utf-8 -*-


import time
import sys
from SyntacticParser.Grammar import *
from datetime import datetime
import re
from log.logger import makeLog, createLog, logChoice
import pickle
import timeit
import csv
import matplotlib.pyplot as plt





print ">>MAIN: Compiling SyntacticParser"
import pyximport; pyximport.install()
#from helloworld import *
from syntactictestnumpy import SyntacticParser


parser = SyntacticParser()

# grammar_rules = parser.grammar.rules

# nonterminals = {}
# left_sides = {}
# for gr in grammar_rules:
# 	for rule in grammar_rules[gr]:
# 		left_sides[rule.left_side] = 0
# 		nonterminals[rule.constituents[0]] = 0
# 		if len(rule.constituents) > 1:
# 			nonterminals[rule.constituents[1]] = 0

# print "Length of grammar:", len(grammar_rules)
# print "Number of left_side nonterminals:", len(left_sides)
# print "Number of right_side nonterminals:", len(nonterminals)

# sys.exit()





def get_all_sentences(article):
	sentenceList = []
	for entry in article[1:]:
		if len(repr(entry)) < 7: continue
		
		entry = entry.replace("\n", "")
		sentences = re.split('(\./\./TEGN|\?/\?/TEGN)', entry)

		for sentence in sentences:
			output_sentence = []
			words = sentence.split(" ")

			for word in words:
				lemma = word[:word.find("/")]

				if lemma[:1] == "\n": lemma = lemma[1:]
				if lemma == "N": continue
				if lemma == ".": continue
				if len(lemma) < 1: continue

				postaggedlemma = (re.sub('/[^>]+/', '/', word)).split("/")
				output_sentence.append(postaggedlemma)

			sentenceList.append(output_sentence)
			
	return sentenceList



print ">>MAIN: Syntactically parsing a test corpus"
# Test corpus
corp = "data/test/test_monster_output_indland.in"
#corp = "data/monster_output/indland.in"
with open(corp) as file:
	data = pickle.load(file)


print ">>MAIN: Number of articles in corpus is", len(data)
print ">>MAIN: Now grabbing sentences from articles."
starttime = datetime.now()
sentences = []
for article in data:
	tmp = get_all_sentences(data[article])
	for s in tmp:
		sentences.append(s)

print ">>MAIN: Grabbed %s sentences." % (len(sentences))
print ">>MAIN: Time spent is", (datetime.now() - starttime)
print



def run_test():
	stop = 10
	illegal_parses = 0
	empty_sentences = 0
	for s in sentences[:stop]:
		if len(s) == 0: empty_sentences += 1
		else:
			t = parser.parse_sentence(s)
			if t is None: illegal_parses += 1
			if t is not None: print t.tree




# import timeit
# t = timeit.Timer(stmt="run_test()", setup="from __main__ import run_test")
# print "Average time for %s sentences and %s tests: %s" % (stop, tests, (t.timeit(tests) / tests))
# print
# sys.exit()


# Getting sentences of a specific length
# tmp = []
# for s in sentences:
# 	if len(s) < 30:
# 		tmp.append(s)
# sentences = tmp

starttime = datetime.now()

# Running the actual parse
statistics = []
illegal_parses = 0
empty_sentences = 0
stop = len(sentences)
stop = 10
parser.test = False
for s in sentences[:stop]:
	if len(s) == 0: empty_sentences += 1
	else:
		t = parser.parse_sentence(s)
		if t is None: illegal_parses += 1
		if t is not None: print t.tree
		# statistics.append([len(s), parser.counter1])
		#statistics.append([len(s), parser.time_counter1.microseconds, parser.time_counter2.microseconds])


print
final_time = (datetime.now() - starttime)
print ">>MAIN: %s total number of sentences." % stop
print ">>MAIN: %s empty sentences." % (empty_sentences) 
print ">>MAIN: %s, or %s%%, unparsable sentences." % (illegal_parses, illegal_parses*100/(stop-empty_sentences))
print ">>MAIN: Total time spent is %s." % final_time
print "Average time per sentence:", (float(str(final_time.seconds) + str(final_time.microseconds)) / (1000000)) / (stop-empty_sentences)
print ">>MAIN: Total time spent on:"
print ".........TOTAL: running CKY: \t\t", parser.cky_logger.time_counter
print ".........TOTAL: building the tree: \t", parser.tree_logger.time_counter
print ".........Grammar loop: \t\t\t", parser.cky_logger1.time_counter
print ".........Cross product: \t\t", parser.cky_logger2.time_counter
print





# # Graph: runs through innermost loop
# x = [x[0] for x in statistics] # sentence length
# y = [y[1] for y in statistics] # Empirical counter
# z = [(z[0]**3)*len(parser.grammar.rules) for z in statistics] # Running time of grammar loop solution
# w = [(w[0]**3)*11065**2 for w in statistics] # Worst case for our solution

# handle_1 = plt.scatter(x, y, color="blue", label='Cross product', s=2)
# handle_2, = plt.plot(x, z, "r--", color="red", label='Grammar Loop')
# handle_2.set_antialiased(True)
# #plt.legend(handles=[handle_1, handle_2])
# plt.title('No. of runs through innermost loop')
# plt.ylabel('No. of runs through innermost loop')
# plt.xlabel('Length of sentence')

# plt.axis([-10.0,100.0, -10.0,4000000.0])
# # ax = p.gca()
# # ax.set_autoscale_on(False)

# plt.show()


# sys.exit()




# Graph: Plot the actual runtime based on the timecounters
import matplotlib.pyplot as plt
x = [x[0] for x in statistics]
y = [y[1] for y in statistics]
z = [z[2] for z in statistics]

handle_1 = plt.scatter(x, y, color="blue", label='Cross product', s=2)
handle_2 = plt.scatter(x, z, color="red", label='Grammar Loop', s=2)
plt.legend(handles=[handle_1, handle_2])
plt.title('Actual runtime comparison')
plt.ylabel('Runtime in microseconds')
plt.xlabel('Length of sentence')
plt.show()



sys.exit()




# with open('syntactictestlog.csv', 'wb') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     for entry in statistics:
# 	    wr.writerow(entry)





