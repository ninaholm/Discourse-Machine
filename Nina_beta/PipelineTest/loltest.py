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









# t = timeit.Timer(stmt="''.join(('fish', 'cat'))", setup="")
# print "Join:", t.timeit()


# t = timeit.Timer(stmt="hash(('fish', 'cat'))", setup="")
# print "Hash tuple:", t.timeit()

# t = timeit.Timer(stmt="hash(('fishcat'))", setup="")
# print "Hash string:", t.timeit()

# tpl = ('fish', 'cat')
# print hash(tpl)

# sys.exit()


# with open("SyntacticParser/grammar.in", "r") as gfile:
# 	g = pickle.load(gfile)

# new_grammar = Grammar()

# for bc_key in g.rules:
# 	for rule in g.rules[bc_key]:
# 		if len(rule.constituents) == 2:
# 			tpl = (rule.constituents[0], rule.constituents[1])
			
# 			h = hash(tpl)
# 			if h in new_grammar.rules:
# 				new_grammar.rules[h].append(rule)
# 			else:
# 				new_grammar.rules[h] = [rule]

# new_grammar.print_grammar()



# sys.exit()



print ">>MAIN: Compiling SyntacticParser"
import pyximport; pyximport.install()
#from helloworld import *
from syntactictestnumpy import SyntacticParser


parser = SyntacticParser()


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

illegal_parses = 0
empty_sentences = 0
tests = 10


starttime = datetime.now()

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


statistics = []
illegal_parses = 0
empty_sentences = 0
stop = 100
parser.test = False
for s in sentences[:stop]:
	if len(s) == 0: empty_sentences += 1
	else:
		t = parser.parse_sentence(s)
		if t is None: illegal_parses += 1
		if t is not None: print t.tree
		#statistics.append([len(s), parser.counter, (len(s)*len(s)*len(s)*14000)])
		statistics.append(parser.counter2)

sys.exit()


import matplotlib.pyplot as plt
# x = [x[0] for x in statistics]
# y = [y[1] for y in statistics]


tmp = {}
for item in statistics:
	item = (item - (item%1000))
	if item in tmp: tmp[item] += 1
	else: tmp[item] = 1

lst = []
for item in tmp:
	lst.append([tmp[item], item])

x = [x[0] for x in lst]
y = [y[1] for y in lst]
plt.bar(y, x, width=900, edgecolor="blue")
plt.show()




sys.exit()




# with open('syntactictestlog.csv', 'wb') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     for entry in statistics:
# 	    wr.writerow(entry)

print
final_time = (datetime.now() - starttime)
print ">>MAIN: %s total number of sentences." % stop
print ">>MAIN: %s empty sentences." % (empty_sentences) 
print ">>MAIN: %s, or %s%%, unparsable sentences." % (illegal_parses, illegal_parses*100/stop)
print ">>MAIN: Total time spent is %s." % final_time
print "Average time per sentence:", (float(str(final_time.seconds) + str(final_time.microseconds)) / (1000000)) / (stop-empty_sentences) / tests
print ">>MAIN: Total time spent on:"
print ".........TOTAL: running CKY: \t\t\t", parser.cky_logger.time_counter
print ".........TOTAL: building the tree: \t\t", parser.tree_logger.time_counter
print ".........filling out first row: \t\t", parser.cky_logger9.time_counter
print ".........getting cross products of b and c: \t", parser.cky_logger1.time_counter
print ".........splitting triple: \t\t\t", parser.cky_logger2.time_counter
print ".............empty timer: \t\t\t", parser.cky_logger7.time_counter
print ".........getting basic variables: \t\t", parser.cky_logger3.time_counter
print ".........joining coordinates: \t\t\t", parser.cky_logger4.time_counter
print ".........building rules and prob arrays: \t", parser.cky_logger5.time_counter
print ".........appending to bigmatrix: \t\t", parser.cky_logger6.time_counter
print





