#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
import operator
import pickle
import time
import math
from log.logger import indexLog, searchLog

# Takes an array of inputfilenames, which is indexed into a dictionary with words as keys and [(articleid, count)] as values. 
# A dictionary of articles are also returned, with articleids as keys and totalwordcount as values.
# logdict[inputfile(s) + "-index"]: [Which file(s) has been indexed, # articles, # unique words, # average words/article, time to unpickle, time to index and time in total].

class Corpus:
	def __init__(self, inputfiles):
		self.wordIndex = {}
		self.articleIndex = {}
		self.inputfiles = inputfiles

	def index(self):
		starttime = time.time()
		print ">>INDEX: Word indexing started."
		index = {}
		articlecounts = {}
		inputpath = os.getcwd() + "/data/lemmatiser_output"

		doccount = 0
		totalwordcount = 0
		inputdata = {}

		pickleTime = time.time()
		for inputfilename in self.inputfiles:
			print ">>INDEX: Unpickling: \t '%s'." %inputfilename
			path = os.path.join(inputpath, inputfilename)
			pickledData = open(path, "r")
			tmp = pickle.load(pickledData)
			inputdata.update(tmp)
			pickledData.close()
		pickleTime = round((time.time() - pickleTime), 3)

		indexTime = time.time()
		print ">>INDEX: Indexing %s articles." % len(inputdata)
		for doc in inputdata:
			doccount += 1
			wordcount = 0
			articleid = doc

			for line in inputdata[doc]:
				#print "line: %s" % line
				if len(line) < 1:
					continue

				for word in line:
					if len(word) < 1:
						continue
					wordcount += 1
					if word in index:
						if articleid in index[word]:
							index[word][articleid] += 1 
						else:
							index[word][articleid] = 1
					else:
						index[word] = {articleid:1}
					# print "articleid: %s" % index[word]
			totalwordcount += wordcount
			articlecounts[articleid] = wordcount
		indexTime = round((time.time() - indexTime), 3)

		print ">>INDEX: %s words in total." % totalwordcount
		print ">>INDEX: %s unique words indexed." % len(index)
		print ">>INDEX: Document average length is %s." % (totalwordcount / doccount)

		self.wordIndex = index
		self.articleIndex = articlecounts

		totalTime = round((time.time() - starttime), 3)

		print ">>INDEX: Word indexing completed in %s seconds." % totalTime
		indexLog(self.inputfiles, len(inputdata), len(index), (totalwordcount / doccount), pickleTime, indexTime, totalTime)


	def search(searchTerm):
		starttime = time.time()
		print ">>SEARCHARTICLES: Search for top TF-IDF values has started."

		
		resultspath = os.getcwd() + "/TFIDF_searcher/articleresults.txt"

		totaldoccount = len(Corpus.articleIndex)

		results = []

		term = str(searchTerm).strip()
		# term = lemmatise_input_term(term)
		if term in Corpus.wordIndex:
			articlehits = Corpus.wordIndex[term]
			doccount = len(articlehits)
			IDF = math.log10(totaldoccount / float(doccount))

			for article in articlehits:
				wordcount = articlehits[article]
				articlewordcount = Corpus.articleIndex[article]
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

		for x in results:
			print x[0]
		
		# resultfile = open(resultspath, "w")
		# for result in results:
		#  	resultfile.write(result[0] + "\n")
		# 	for articles in result[1]:
		# 		resultfile.write(str(articles[0]) + " : " + str(articles[1]) + "\n")
		# resultfile.close()
		totalTime = round((time.time() - starttime), 3)

		print ">>SEARCHARTICLES: Search has completed in %s seconds." % totalTime
		searchLog(term, len(results), totalTime)
		
		return results



