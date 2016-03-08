import os
import glob
import operator
import math
import pickle
import time


def search(TFIDFindex, ARTICLEindex):
	starttime = time.time()
	print ">>SEARCH: Search for top TF-IDF values has started."

	TFIDFindexpath = os.getcwd() + "/TFIDF_indexer/inverted_index.in"
	ARTICLEindexpath = os.getcwd() + "/TFIDF_indexer/articlecounts.in"
	searchtermspath = os.getcwd() + "/TFIDF_searcher/searchterms.txt"
	resultspath = os.getcwd() + "/TFIDF_searcher/results.txt"

	# TFIDFindexpath = os.getcwd() + "/inverted_index.txt"
	# ARTICLEindexpath = os.getcwd() + "/articlecounts.txt"

	# print ">>SEARCH: Loading TF-IDF index."
	# tempIndex = open(TFIDFindexpath, "rb")
	# string = ""
	# for line in tempIndex:
	# 	string += line
	# TFIDFindex = pickle.loads(string)
	# tempIndex.close()

	# print ">>SEARCH: Loading article count index."
	# tempIndex = open(ARTICLEindexpath, "rb")
	# string = ""
	# for line in tempIndex:
	# 	string += line
	# ARTICLEindex = pickle.loads(string)
	# tempIndex.close()

	totaldoccount = len(ARTICLEindex)

	searchterms = open(searchtermspath, "r")

	results = []

	for term in searchterms:
		term = str(term).strip()
		tmpresult = []
		if hash(term) in TFIDFindex:
			articlehits = TFIDFindex[hash(term)][1]
			doccount = len(articlehits)
			IDF = math.log10(totaldoccount / float(doccount))

			for article in articlehits:
				wordcount = articlehits[article]
				articlewordcount = ARTICLEindex[article]
				TF = wordcount / float(articlewordcount)
				TFIDF = TF * IDF
				tmpresult.append((article,TFIDF))
				# print "TFIDF: %s * %s = %s" % (TF, IDF, TFIDF)
		else:
			print ">>SEARCH: '%s' \t 0 articles." %term
		if len(tmpresult) < 1:
			continue
		# Sort results on their TFIDF rating, in decreasing order.
		tmpresult = sorted(tmpresult, key=lambda result: result[1], reverse=True)
		print ">>SEARCH: '%s' \t %s articles." % (term, len(tmpresult))

		# Deletes the bottom 50% of our search results
		tmpresult = tmpresult[0:len(tmpresult)/2]
		if len(tmpresult) > 0:
			results.append((term,tmpresult))

	resultfile = open(resultspath, "w")
	for result in results:
	 	resultfile.write(result[0] + "\n")
		for articles in result[1]:
			resultfile.write(str(articles[0]) + " : " + str(articles[1]) + "\n")
	resultfile.close()
	print ">>SEARCH: Search has completed in %s seconds." % round((time.time() - starttime), 3)