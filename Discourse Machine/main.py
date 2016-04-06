from XML_parser.XMLparser import parse
from Word_indexer.Wordindexer import index
from TFIDF_searcher.TFIDFsearcher import searchArticles, searchTopWords
from Lemmatiser.new_Lemmatiser import *
from Sentiment_classifier.sentiment_classifier import run_sentiment_classifier
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


starttime = time.time()
# parsedCorpus = parse(0)
# print

#lemmatise_directory("data/original_data/information")
# print

indexes = index(0)
wordIndex = indexes[0]
articleIndex = indexes[1]
print

articles = searchArticles(wordIndex, articleIndex)
print

# searchTopWords(wordIndex, articleIndex, articles, 100)
# print

#run_frequent_neighbours(wordIndex)
#print

#Extract the list of article_ids
article_ids = []
data_folder = "data/lemmatiser_output/"
li = articles[0][1]
for l in li:
	article_ids.append(data_folder + l[0])

run_sentiment_classifier(article_ids, wordIndex)
print

print "Total time elapsed: %s seconds" % round((time.time() - starttime), 3)
print

# input_term = raw_input("Enter topic term: ")
# lem_input_term = lemmatise_input_term(input_term)
