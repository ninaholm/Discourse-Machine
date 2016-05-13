# -*- coding: utf-8 -*-

from log.logger import makeLog, createLog, logChoice
from Corpus.corpus import *
from SyntacticParser.SyntacticParser import SyntacticParser, SentenceTree
from SyntacticParser.Grammar import *
import time
from datetime import datetime
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
#sys.modules()


parser = SyntacticParser()

# Test sentences
s1 = "Regeringen/N_DEF_SING freml\xc3\xa6gger/V_PRES sit/PRON_POSS nye/ADJ arbejdsprogram/N_INDEF_SING"
s2 = "Danmark/EGEN er/V_PRES blandt/PR\xc3\x86P de/PRON_DEMO 10/NUM rigeste/ADJ lande/N_INDEF_PLU i/PR\xc3\x86P verden/N_INDEF_SING"

if True:
	s = "To/NUM russere/N_INDEF_PLU tror/V_PRES ikke/ADV intet/ADJ ./TEGN"

	t = parser.parse_sentence(s)
	if t is not None:
		print t.tree
		print t.get_sentiment_score({}, "russere")

	sys.exit()





print ">>MAIN: Syntactically parsing a test corpus"
# Test corpus
with open("data/original_test_indland.in") as file:
	data = pickle.load(file)

# Building a list of sentences to parse
sentences = []
for article in data:
	sen = data[article][4].split("\n")
	for s in sen:
		sentences.append(s)

print ">>MAIN: Number of sentences is:", len(sentences)
print

counter = 0
illegal_parses = 0
empty_sentences = 0
stop = len(sentences)

for s in sentences:
	if len(s) == 0: empty_sentences += 1
	else:
		t = parser.parse_sentence(s)
		if t is None: illegal_parses += 1
#		raw_input("continue?")
		counter += 1
		if counter % 100 == 0:
			print ">>MAIN: Now parsed %s sentences in %s time" % (counter, datetime.now() - parser.log.starttime)
		if counter == stop:
			break


print
final_time = (datetime.now() - parser.log.starttime)
print ">>MAIN: %s total number of sentences." % stop
print ">>MAIN: %s empty sentences." % (empty_sentences) 
print ">>MAIN: %s, or %s%%, unparsable sentences." % (illegal_parses, illegal_parses*100/stop)
print ">>MAIN: Total time spent is %s." % final_time
print ">>TOTAL TIME SPENT ON:"
print "......Running CKY:", parser.cky_logger.time_counter
print "......Building trees:", parser.tree_logger.time_counter
print "Average time per sentence:", (float(str(final_time.seconds) + str(final_time.microseconds)) / (1000000)) / (stop-empty_sentences)
print