from XML_parser.XMLparser import parse
from Word_indexer.Wordindexer import index
from TFIDF_searcher.TFIDFsearcher import searchArticles, searchTopWords
from Lemmatiser.Lemmatiser import lemmatise_directory, lemmatise_input_term, postag_directory
from Sentiment_classifier.sentiment_classifier import run_sentiment_classifier
from log.logger import log, createLog, logChoice
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

logChoice = logChoice(0)

starttime = time.time()
# parsedCorpus = parse(0)
# print

postag_directory("data/test")
# print

sys.exit()

if logChoice == True:
	createLog(0)

# inputfiles = [["indland.in"], ["udland.in"], ["debat.in"],["kultur.in"]]
inputfiles = [["test_indland.in"], ["test_udland.in"]]


# Loops through the chosen corpora and returns sentimentscore for every searchterm in them.
for inputfile in inputfiles:
	indexes = index(inputfile) # Send an array consisting of filenames of the inputfiles you want indexed!
	wordIndex = indexes[0]
	articleIndex = indexes[1]
	print

	# Reads searchterms for upcoming loop.
	searchterms = []
	searchtermsfile = open(os.getcwd() + "/TFIDF_searcher/searchterms.txt", "r")
	for term in searchtermsfile:
		searchterms.append(str(term).strip())

	# Loops through all searchterms and calculates their sentimentscore for the current corpus.
	for term in searchterms:
		articles = searchArticles(wordIndex, articleIndex, term)
		print

		if len(articles) == 0:
			continue
		# searchTopWords(wordIndex, articleIndex, articles, 100)
		# print

		#Extract the list of article_ids
		article_ids = []
		for x in articles:
			article_ids.append(x[0])

		# run sentiment classifier on the searchterms's articlesubset
		run_sentiment_classifier(article_ids, wordIndex, term)
		print

	print "-" * 50

totalTime = round((time.time() - starttime), 3)
print "Total time elapsed: %s seconds" % totalTime
print

if logChoice == True:
	log(totalTime)
# input_term = raw_input("Enter topic term: ")
# lem_input_term = lemmatise_input_term(input_term)
