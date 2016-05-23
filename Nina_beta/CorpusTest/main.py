# from Sentiment_classifier.sentiment_classifier import run_sentiment_classifier
from log.logger import makeLog, createLog, logChoice
from Corpus.corpus import *
from POSCorpus.POSCorpus import *
import time
import os
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

logChoice = logChoice(0)

starttime = time.time()

if logChoice == True:
	createLog(0)

# inputfiles = [["indland.in", "udland.in", "debat.in", "kultur.in"], ["telegram.in"]]
# inputfiles = [["indland.in", "udland.in", "debat.in", "kultur.in"]]
# inputfiles = [["test_indland.in"], ["test_udland.in"]]
# inputfiles = [["indland.in"],["udland.in"],["debat.in"],["kultur.in"]]
# inputfiles = [["debat.in"]]
inputfiles = [["indland.in"]]


posc = PipelineHandler(inputfiles)
posc.run()

print "DONE."

sys.exit()


# Loops through the chosen corpora and returns sentimentscore for every searchterm in them.
for inputfile in inputfiles:
	subSetList = []

	while True:
		c = Corpus(inputfile)
		print
		c.build_indices()

		# Loops through all searchterms and calculates their sentimentscore for the current corpus.
		for term in c.searchterms:
			subset = c.search(term)

			if len(subset) == 0:
				continue
			else:
				subSetList.append((term, subset))
		break
	print

	posc = PipelineHandler(inputfiles)
	posc.run()
	print
	sys.exit()

	for term_subset in subSetList:
		posc.score_sentiment(term_subset)

	print "#" * 50





totalTime = round((time.time() - starttime), 3)
print "Total time elapsed: %s seconds" % totalTime
print

if logChoice == True:
	makeLog(totalTime)

