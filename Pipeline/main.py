# from Sentiment_classifier.sentiment_classifier import run_sentiment_classifier
from log.logger import makeLog, createLog, logChoice
from PipelineHandler.PipelineHandler import PipelineHandler
import time
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

logChoice = logChoice(0)

starttime = time.time()

if logChoice == True:
	createLog(0)

# corpora = [["indland.in", "udland.in", "debat.in", "kultur.in"], ["telegram.in"]]
corpora = [["indland.in", "udland.in", "debat.in", "kultur.in"]]
# corpora = [["test_indland.in"], ["test_udland.in"]]
# corpora = [["indland.in"],["udland.in"],["debat.in"],["kultur.in"]]
# corpora = [["debat.in"]]
# corpora = [["indland.in"]]


posc = PipelineHandler(corpora)
posc.run()

print "DONE."


totalTime = round((time.time() - starttime), 3)
print "Total time elapsed: %s seconds" % totalTime
print

if logChoice == True:
	makeLog(totalTime)

