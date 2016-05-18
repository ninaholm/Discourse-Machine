#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
import operator
import pickle
import time
import math
import csv
from log.logger import indexLog, searchLog, sentimentArticleLog

# Takes an array of inputfilenames, which is indexed into a dictionary with words as keys and [(articleid, count)] as values. 
# A dictionary of articles are also returned, with articleids as keys and totalwordcount as values.
# logdict[inputfile(s) + "-index"]: [Which file(s) has been indexed, # articles, # unique words, # average words/article, time to unpickle, time to index and time in total].

class Corpus:
	def __init__(self, inputfiles):
		self.wordIndex = {}
		self.articleIndex = {}
		self.inputfiles = inputfiles
		self.searchterms = self.getSearchTerms()
		self.sentimentdict = self.getSentimentDict()
		self.sentimentscore = 0

	def index(self):
		starttime = time.time()
		print ">>INDEX: Word indexing started."
		index = {}
		articlecounts = {}
		inputpath = os.getcwd() + "/data/monster_output"

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
			sentimentcount = 0
			articleid = doc

			for line in inputdata[doc]:
				#print "line: %s" % line
				if len(line) < 1:
					continue

				for word in line.split(" "):
					word = word[:word.find("/")]
					if len(word) < 1:
						continue
					if word in self.sentimentdict:
						sentimentcount += int(self.sentimentdict[word])
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
			articlecounts[articleid] = (wordcount, sentimentcount)
		indexTime = round((time.time() - indexTime), 3)

		print ">>INDEX: %s words in total." % totalwordcount
		print ">>INDEX: %s unique words indexed." % len(index)
		print ">>INDEX: Document average length is %s." % (totalwordcount / doccount)

		self.wordIndex = index
		self.articleIndex = articlecounts

		totalTime = round((time.time() - starttime), 3)

		print ">>INDEX: Word indexing completed in %s seconds. \n" % totalTime
		indexLog(self.inputfiles, len(inputdata), len(index), (totalwordcount / doccount), pickleTime, indexTime, totalTime)


	def search(self, searchTerm):
		starttime = time.time()
		totaldoccount = len(self.articleIndex)
		results = []

		term = str(searchTerm).strip()
		# term = lemmatise_input_term(term)
		if term in self.wordIndex:
			articlehits = self.wordIndex[term]
			doccount = len(articlehits)
			IDF = math.log10(totaldoccount / float(doccount))

			for article in articlehits:
				wordcount = articlehits[article]
				articlewordcount = self.articleIndex[article][0]
				TF = wordcount / float(articlewordcount)
				TFIDF = TF * IDF
				results.append((article, TFIDF))
				# print "TFIDF: %s * %s = %s" % (TF, IDF, TFIDF)
		else:
			print ">>SEARCHARTICLES: '%s' has 0 articles. Search terminated." %term
			return results
		if len(results) < 2:
			print ">>SEARCHARTICLES: '%s' has %s article(s). Search terminated." %(term,len(results))
			results = []
			return results

		# Sort results on their TFIDF rating, in decreasing order.
		results = sorted(results, key=lambda result: result[1], reverse=True)
		print ">>SEARCHARTICLES: '%s' has %s articles (%s returned)." % (term, len(results), (len(results) / 2))

		# Deletes the bottom 50% of our search results
		results = results[0:len(results)/2]
		self.sentimentscore = 0

		# Removes TFIDF values from the remaining articles and adds up the sentimentscore
		for i in range(len(results)):
			x = results[i]
			self.sentimentscore += self.articleIndex[x[0]][1]
			results[i] = x[0]

		totalTime = round((time.time() - starttime), 3)

#		print ">>SEARCHARTICLES: Search has completed in %s seconds." % totalTime
		searchLog(term, len(results), totalTime)
		sentimentArticleLog(term, self.sentimentscore)
		return results

	def getSentimentDict(self):
		dict_path = "data/sentiment_dictionaries/information_manual_sent.csv"
		with open(dict_path, "r") as csvfile:
			dictionary = {}
			with open(dict_path, "r") as csvfile:
				csv_dict = csv.reader(csvfile)
				for row in csv_dict:
					dictionary[row[0].decode('utf-8')] = row[1]
		return dictionary

	def getSearchTerms(self):
		searchterms = []
		searchtermsfile = open(os.getcwd() + "/data/searchterms.txt", "r")
		for term in searchtermsfile:
			searchterms.append(str(term).strip())
		print ">>SEARCHTERMS: %s." %(" | ".join(searchterms))
		return searchterms





