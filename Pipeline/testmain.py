# from Sentiment_classifier.sentiment_classifier import run_sentiment_classifier
from log.logger import makeLog, createLog, logChoice
from Corpus.corpus import *
from POSCorpus.POSCorpus import *
import time
import os
import sys


inputfiles = [["original_test_indland.in"]]
subsetList = [("venstre", [""])]

# Loops through the chosen corpora and returns sentimentscore for every searchterm in them.
for inputfile in inputfiles:
	c = POSCorpus(inputfile, subsetList)
	c.load()
	c.score_sentiment(subsetList[0])
	

	# Loops through all searchterms and calculates their sentimentscore for the current corpus.
	# for term in c.searchterms:
	# 	subCorpusArticleList = c.search(term)
	# 	print

	# 	if len(subCorpusArticleList) == 0:
	# 		continue


	# print "-" * 50

# totalTime = round((time.time() - starttime), 3)
# print "Total time elapsed: %s seconds" % totalTime


