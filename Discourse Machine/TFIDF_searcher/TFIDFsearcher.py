import os
import glob
import operator
import math
import pickle
import time
from Lemmatiser.Lemmatiser import *


def searchArticles(TFIDFindex, ARTICLEindex):
	starttime = time.time()
	print ">>SEARCHARTICLES: Search for top TF-IDF values has started."

	searchtermspath = os.getcwd() + "/TFIDF_searcher/searchterms.txt"
	resultspath = os.getcwd() + "/TFIDF_searcher/articleresults.txt"

	totaldoccount = len(ARTICLEindex)

	searchterms = open(searchtermspath, "r")

	results = []

	for term in searchterms:
		term = str(term).strip()
		# term = lemmatise_input_term(term)
		tmpresult = []
		if term in TFIDFindex:
			articlehits = TFIDFindex[term][1]
			doccount = len(articlehits)
			IDF = math.log10(totaldoccount / float(doccount))

			for article in articlehits:
				wordcount = articlehits[article]
				articlewordcount = ARTICLEindex[article]
				TF = wordcount / float(articlewordcount)
				TFIDF = TF * IDF
				tmpresult.append((article, TFIDF))
				# print "TFIDF: %s * %s = %s" % (TF, IDF, TFIDF)
		else:
			print ">>SEARCHARTICLES: '%s' \t 0 articles." %term
		if len(tmpresult) < 1:
			continue
		# Sort results on their TFIDF rating, in decreasing order.
		tmpresult = sorted(tmpresult, key=lambda result: result[1], reverse=True)
		print ">>SEARCHARTICLES: '%s' \t %s articles." % (term, len(tmpresult))

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

	print ">>SEARCHARTICLES: Search has completed in %s seconds." % round((time.time() - starttime), 3)
	
	return results



def searchTopWords(TFIDFindex, ARTICLEindex,articles,num):
	starttime = time.time()
	print ">>SEARCHWORDS: Search for topic's topwords has started."

	resultspath = os.getcwd() + "/TFIDF_searcher/topwordresults.txt"
	resultfile = open(resultspath, "w")
	totaldoccount = len(ARTICLEindex)

	results = []

	for topic in articles:
		term = topic[0]

		articleids = {}

		for article in topic[1]:
			# print "articleids[%s] = ARTICLEindex[%s] = %s" % (str(article[0]), str(article[0]), str(ARTICLEindex[article[0]]))
			articleids[article[0]] = ARTICLEindex[article[0]]


		# for article in topic[1]:
		# 	articleids.append(article[0])
			
		tmpresult = {}

		for value in TFIDFindex:
			word = TFIDFindex[value][0]
			if len(word) == 0:
				continue
			articlehits = TFIDFindex[value][1]

			IDF = math.log10(len(ARTICLEindex) / float(len(articlehits)))

			for article in articlehits:				
				if article in articleids:
					wordcount = articlehits[article]
					articlewordcount = ARTICLEindex[article]
					TF = wordcount / float(articlewordcount)
					TFIDF = TF * IDF
					if word in tmpresult:
						tmpresult[word] = (tmpresult[word] + TFIDF) / 2
					else:
						tmpresult[word] = TFIDF

					# print word
					# print "%s : %s" % (article, wordcount)

		tmpresult = sorted(tmpresult.items(), key=operator.itemgetter(1), reverse=True)

		topwords = []
		avg = 0

		for word in tmpresult[0:num]:
			avg += float(word[1])
			topwords.append(word[0])

		avg = avg / num

		results.append(topwords)

		resultfile.write(str(topic[0]) + "\n")
		for word in topwords:
			resultfile.write("\t" + word + "\n")

		print ">>SEARCHWORDS: '%s's topwords avg. TFIDF: %s" % (topic[0], avg)		
	
	resultfile.close()

	print ">>SEARCHWORDS: Search for topwords has completed in %s seconds." % round((time.time() - starttime), 3)

	# return results













