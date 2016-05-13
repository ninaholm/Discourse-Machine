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

lem = Lemmatiser()
print lem.lemmatise_input_term("enhedslisten")

inputfiles = [["indland.in", "udland.in", "debat.in", "kultur.in"]]

# inputfiles = [["indland.in"], ["udland.in"], ["debat.in"],["kultur.in"]]
# inputfiles = [["test_indland.in"], ["test_udland.in"]]
# inputfiles = [["debat.in"], ["indland.in"]]


def main(self):
	createLog(0)
	starttime = time.time()
	# Loops through the chosen corpora and returns sentimentscore for every searchterm in them.
	for inputfile in inputfiles:
		c = Corpus(inputfile)
		c.index()

		# Loops through all searchterms and calculates their sentimentscore for the current corpus.
		for term in c.searchterms:
			subCorpusArticleList = c.search(term)
			print

			if len(subCorpusArticleList) == 0:
				continue

	totalTime = round((time.time() - starttime), 3)
	print "Total time elapsed: %s seconds" % totalTime

	if testdata[0] == 0:
		testdata[0] = totalTime
	else:
		testdata[0] = (totalTime + testdata[0]) / 2
	print testdata[0]
	makeLog(totalTime)

def testLog(testdata):
	print "testlol"

for x in range(10):
	main(0)
	break





