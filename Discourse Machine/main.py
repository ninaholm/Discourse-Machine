from XML_parser.XMLparser import parse
from TFIDF_indexer.TFIDFindexer import index
from TFIDF_searcher.TFIDFsearcher import searchArticles, searchTopWords
from Lemmatiser.new_Lemmatiser import *
from Topic_categoriser.topic_categoriser import run_topic_categoriser
#from Topic_categoriser.frequent_neighbours import *
import time

starttime = time.time()
# parsedCorpus = parse(0)
# print

#lemmatise_directory("data/original_data/information")
# print

# indexes = index(0)
# TFIDFindex = indexes[0]
# ARTICLEindex = indexes[1]
# #print

# articles = searchArticles(TFIDFindex, ARTICLEindex)
# #print

# searchTopWords(TFIDFindex, ARTICLEindex, articles, 100)
# print

#run_frequent_neighbours(TFIDFindex)
#print

#Extract the list of article_ids
# article_ids = []
# data_folder = "data/lemmatiser_output/"
# li = articles[0][1]
# for l in li:
# 	article_ids.append(data_folder + l[0])

# run_topic_categoriser(article_ids)
# print

print "Total time elapsed: %s seconds" % round((time.time() - starttime), 3)
print

# input_term = raw_input("Enter topic term: ")
# lem_input_term = lemmatise_input_term(input_term)
