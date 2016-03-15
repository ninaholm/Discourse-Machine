from XML_parser.XMLparser import parse
from TFIDF_indexer.TFIDFindexer import index
from TFIDF_searcher.TFIDFsearcher import searchArticles, searchTopWords
from Lemmatiser.Lemmatiser import *
import time

starttime = time.time()
# parsedCorpus = parse(0)
# print

# lemmatise_directory("data/xmlparser_output")
# print

indexes = index(0)
TFIDFindex = indexes[0]
ARTICLEindex = indexes[1]
print

articles = searchArticles(TFIDFindex, ARTICLEindex)
print

searchTopWords(TFIDFindex, ARTICLEindex, articles, 100)
print

print "Total time elapsed: %s seconds" % round((time.time() - starttime), 3)
print

# input_term = raw_input("Enter topic term: ")
# lem_input_term = lemmatise_input_term(input_term)
