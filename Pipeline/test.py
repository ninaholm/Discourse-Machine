from Corpus.corpus import *
from log.testlogger import makeLog, createLog, logChoice
from Preprocessor.Preprocessor import Lemmatiser
import time
import os
import sys
from guppy import hpy

# hp = hpy()
reload(sys)
sys.setdefaultencoding('utf-8')

# [avg runtime, avg index, avg search]
testdata = [0]

# lem = Lemmatiser()
# print lem.lemmatise_input_term("enhedslisten")

inputfiles = [["indland.in", "udland.in", "debat.in", "kultur.in"]]

# inputfiles = [["indland.in"], ["udland.in"], ["debat.in"],["kultur.in"]]
# inputfiles = [["test_indland.in"], ["test_udland.in"]]
# inputfiles = [["debat.in"], ["indland.in"]]


def main(self):
	createLog(0)
	starttime = time.time()
	# Loops through the chosen corpora and returns sentimentscore for every searchterm in them.
	for inputfile in inputfiles:
		subSetList = []

		while True:
			c = Corpus(inputfile)
			# print
			c.index()

			# # Loops through all searchterms and calculates their sentimentscore for the current corpus.
			# for term in c.searchterms:
			# 	subset = c.search(term)

			# 	if len(subset) == 0:
			# 		continue
			# 	else:
			# 		subSetList.append((term, subset))
			break
		print

		# posc = POSCorpus(inputfile, subSetList)
		# posc.load()
		# print

		# for term_subset in subSetList:
		# 	posc.score_sentiment(term_subset)

		print "#" * 50

	totalTime = round((time.time() - starttime), 3)
	print "Total time elapsed: %s seconds" % totalTime

	if testdata[0] == 0:
		testdata[0] = totalTime
	else:
		testdata[0] = (totalTime + testdata[0]) / 2
	print testdata[0]
	# makeLog(totalTime)

def testLog(testdata):
	print "testlol"

for x in range(5):
	main(0)
	





