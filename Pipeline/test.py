# from Sentiment_classifier.sentiment_classifier import run_sentiment_classifier
from log.logger import makeLog, createLog, logChoice
from Corpus.corpus import *
import time
import os
import sys
from guppy import hpy

hp = hpy()
reload(sys)
sys.setdefaultencoding('utf-8')

logChoice = logChoice(0)
testdata = [0]


if logChoice == True:
	createLog(0)

# inputfiles = [["indland.in"], ["udland.in"], ["debat.in"],["kultur.in"]]
inputfiles = [["test_indland.in"], ["test_udland.in"]]

def main(self):
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
	if testdata[0] == 0:
		testdata[0] = totalTime
	else:
		testdata[0] = (totalTime + testdata[0]) / 2
	print testdata[0]

for x in range(10):
	main(0)



