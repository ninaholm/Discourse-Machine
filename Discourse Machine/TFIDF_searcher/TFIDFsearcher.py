#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
import operator
import math
import pickle
import time
from Lemmatiser.Lemmatiser import *

# Takes the previously created indexes and searches them for a given searchterm. 
# Returns a subset of articles, in a list of tuples (articleid, TFIDF score), for the top 50% (based on TFIDF) of articles where the term exists. 
# logdict[searchTerm + "search"] = [total runningtime, # articles]

def searchArticles(wordIndex, articleIndex, searchTerm):
	starttime = time.time()
	print ">>SEARCHARTICLES: Search for top TF-IDF values has started."

	
	resultspath = os.getcwd() + "/TFIDF_searcher/articleresults.txt"

	totaldoccount = len(articleIndex)



	results = []

	term = str(searchTerm).strip()
	# term = lemmatise_input_term(term)
	if term in wordIndex:
		articlehits = wordIndex[term]
		doccount = len(articlehits)
		IDF = math.log10(totaldoccount / float(doccount))

		for article in articlehits:
			wordcount = articlehits[article]
			articlewordcount = articleIndex[article]
			TF = wordcount / float(articlewordcount)
			TFIDF = TF * IDF
			results.append((article, TFIDF))
			# print "TFIDF: %s * %s = %s" % (TF, IDF, TFIDF)
	else:
		print ">>SEARCHARTICLES: '%s' 0 articles. Search terminated." %term
		return results
	if len(results) < 2:
		print ">>SEARCHARTICLES: '%s' too few articles. Search terminated." %term
		results = []
		return results
	# Sort results on their TFIDF rating, in decreasing order.
	results = sorted(results, key=lambda result: result[1], reverse=True)
	print ">>SEARCHARTICLES: '%s' \t %s articles." % (term, len(results))

	# Deletes the bottom 50% of our search results
	results = results[0:len(results)/2]
	
	# resultfile = open(resultspath, "w")
	# for result in results:
	#  	resultfile.write(result[0] + "\n")
	# 	for articles in result[1]:
	# 		resultfile.write(str(articles[0]) + " : " + str(articles[1]) + "\n")
	# resultfile.close()
	totalTime = round((time.time() - starttime), 3)

	print ">>SEARCHARTICLES: Search has completed in %s seconds." % totalTime
	log(term, len(results), totalTime)
	
	return results



def searchTopWords(wordIndex, articleIndex,articles,num):
	starttime = time.time()
	print ">>SEARCHWORDS: Search for topic's topwords has started."

	resultspath = os.getcwd() + "/TFIDF_searcher/topwordresults.txt"
	resultfile = open(resultspath, "w")
	totaldoccount = len(articleIndex)

	results = []

	for topic in articles:
		term = topic[0]

		articleids = {}

		for article in topic[1]:
			# print "articleids[%s] = articleIndex[%s] = %s" % (str(article[0]), str(article[0]), str(articleIndex[article[0]]))
			articleids[article[0]] = articleIndex[article[0]]


		# for article in topic[1]:
		# 	articleids.append(article[0])
			
		tmpresult = {}

		for value in wordIndex:
			word = value
			if len(word) == 0:
				continue
			articlehits = wordIndex[value]

			IDF = math.log10(len(articleIndex) / float(len(articlehits)))

			for article in articlehits:				
				if article in articleids:
					wordcount = articlehits[article]
					articlewordcount = articleIndex[article]
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


def log(term, articleNum, totalTime):
	path = os.getcwd() + "/log/tmplogarray.in"
	picklefile = open(path, 'rb')
	logarray = pickle.load(picklefile)
	picklefile.close()

	data = [term, articleNum, totalTime]
	logarray.append(data)

	picklefile = open(path, 'wb')
	pickle.dump(logarray, picklefile)
	picklefile.close()
	








