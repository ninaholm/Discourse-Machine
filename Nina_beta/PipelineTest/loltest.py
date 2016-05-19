# -*- coding: utf-8 -*-


import time
import sys
from SyntacticParser.Grammar import *
from datetime import datetime
import re
from log.logger import makeLog, createLog, logChoice
import pickle



def function(values):
	pass


test = [['NCP', 1.6890549574946627e-13, '1:2:0', '7:3:0'], ['VAP', 2.6890549574946627e-17, '1:2:0', '7:3:0'], ['VAP', 3.1606174132225905e-16, '1:2:0', '7:3:1'], ['VAP', 2.6748472859920607e-13, '1:2:0', '7:3:10'], ['VAP', 8.569254136414964e-14, '1:2:0', '7:3:7'], ['VAP', 4.1207132860318137e-13, '1:2:0', '7:3:13'], ['VAP', 6.426940602311224e-14, '1:2:0', '7:3:3'], ['VAP', 7.366842682581958e-18]]

print max([x[1] for x in test])

values = set(map(lambda x:x[0], test))
newlist = [[y for y in test if y[0]==x] for x in values]

new_dict = {}
for i in range(len(newlist)):
	new_dict[newlist[i][0][0]] = [x[1] for x in newlist[i]]

print new_dict

b_list = [x for x in test if x[1]==max([y[1] for y in new_dict[x]])]

print b_list


sys.exit()



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
	stop = 100
	illegal_parses = 0
	empty_sentences = 0
	for s in sentences[:stop]:
		if len(s) == 0: empty_sentences += 1
		else:
			t = parser.parse_sentence(s)
			if t is None: illegal_parses += 1



stop = 100
illegal_parses = 0
empty_sentences = 0
for s in sentences[:stop]:
	if len(s) == 0: empty_sentences += 1
	else:
		t = parser.parse_sentence(s)
		if t is None: illegal_parses += 1
		#if t is not None: print t.tree


# import timeit
# t = timeit.Timer(stmt="run_test()", setup="from __main__ import run_test")
# print (t.timeit(tests) / tests)




print
final_time = (datetime.now() - starttime)
print ">>MAIN: %s total number of sentences." % stop
print ">>MAIN: %s empty sentences." % (empty_sentences) 
print ">>MAIN: %s, or %s%%, unparsable sentences." % (illegal_parses, illegal_parses*100/stop)
print ">>MAIN: Total time spent is %s." % final_time
print "Average time per sentence:", (float(str(final_time.seconds) + str(final_time.microseconds)) / (1000000)) / (stop-empty_sentences) / tests
print ">>MAIN: Total time spent on:"
print ".........running CKY:", parser.cky_logger.time_counter
print ".........building the tree:", parser.tree_logger.time_counter
print ".........OPTION 1: numpy prob calculator:", parser.cky_logger1.time_counter
print ".........OPTION 2: list comprehension calculator:", parser.cky_logger2.time_counter
print





