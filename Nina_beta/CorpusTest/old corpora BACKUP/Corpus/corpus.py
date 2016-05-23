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

import random #for testing purposes

# Takes an array of inputfilenames, which is indexed into a dictionary with words as keys and [(articleid, count)] as values. 
# A dictionary of articles are also returned, with articleids as keys and totalwordcount as values.
# logdict[inputfile(s) + "-index"]: [Which file(s) has been indexed, # articles, # unique words, # average words/article, time to unpickle, time to index and time in total].

class Corpus:
	def __init__(self, inputfiles):
		self.wordIndex = {}
		self.articleIndex = {}
		self.inputfiles = inputfiles
		self.ngramterms = {}
		self.searchterms = self._getSearchTerms()
		self.sentimentdict = self._getSentimentDict()
		self.sentimentscore = 0

	def build_indices(self):
		starttime = time.time()
		print ">>INDEX: Word indexing started."
		inputpath = os.getcwd() + "/data/monster_output"

		doccount = 0
		totalwordcount = 0
		inputdata = {}

		pickleTime = time.time()
		for inputfilename in self.inputfiles:
			print ">>INDEX: Unpickling: \t '%s'." %inputfilename
			path = os.path.join(inputpath, inputfilename)
			with open(path, "r") as pickledData:
				tmp = pickle.load(pickledData)
				inputdata.update(tmp)
		pickleTime = round((time.time() - pickleTime), 3)

		indexTime = time.time()
		print ">>INDEX: Indexing %s articles." % len(inputdata)
		for articleid in inputdata:
			doccount += 1
			# if doccount > 3695:
			# 	break
			wordcount = 0
			sentimentcount = 0

			for line in inputdata[articleid]:
				if len(line) < 1: continue
				words = line.split(" ")

				for i in range(len(words)):
					word = words[i]
					word = word[:word.find("/")]
					if len(word) < 1: continue
					if word in self.sentimentdict: sentimentcount += int(self.sentimentdict[word])
					if word in self.ngramterms:
						comingwords = self._checkNgram(word, words, i)
						if len(comingwords) > 0:
							for x in comingwords:
								word += "_" + x
						
					wordcount += 1
					if word in self.wordIndex:
						if articleid in self.wordIndex[word]:
							self.wordIndex[word][articleid] += 1 
						else:
							self.wordIndex[word][articleid] = 1
					else:
						self.wordIndex[word] = {articleid:1}

				# for word in line.split(" "):
				# 	word = word[:word.find("/")]
				# 	if len(word) < 1:
				# 		continue
				# 	if word in self.sentimentdict:
				# 		sentimentcount += int(self.sentimentdict[word])
				# 	wordcount += 1
				# 	if word in index:
				# 		if articleid in index[word]:
				# 			index[word][articleid] += 1 
				# 		else:
				# 			index[word][articleid] = 1
				# 	else:
				# 		index[word] = {articleid:1}
					# print "articleid: %s" % index[word]

			totalwordcount += wordcount
			self.articleIndex[articleid] = (wordcount, sentimentcount)

		indexTime = round((time.time() - indexTime), 3)

		print ">>INDEX: %s words in total." % totalwordcount
		print ">>INDEX: %s unique words indexed." % len(self.wordIndex)
		print ">>INDEX: Document average length is %s." % (totalwordcount / doccount)

		totalTime = round((time.time() - starttime), 3)

		print ">>INDEX: Word indexing completed in %s seconds. \n" % totalTime
		print "pickletime: ", pickleTime
		print "indextime: ", indexTime
		print "doccount: ", doccount
		indexLog(self.inputfiles, len(inputdata), len(self.wordIndex), (totalwordcount / doccount), pickleTime, indexTime, totalTime)


	# Returns the subset of articles wherein a search term and an opinion word are found.
	def search(self, searchTerm):
		starttime = time.time()
		totaldoccount = len(self.articleIndex)
		subset = []

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
				subset.append((article, TFIDF))
				# print "TFIDF: %s * %s = %s" % (TF, IDF, TFIDF)
		else:
			print ">>SEARCHARTICLES: '%s' has 0 articles. Search terminated." %term
			return subset
		if len(subset) < 2:
			print ">>SEARCHARTICLES: '%s' has %s article(s). Search terminated." %(term,len(subset))
			return []

		# Sort subset on their TFIDF rating, in decreasing order.
		subset = sorted(subset, key=lambda result: result[1], reverse=True)
		print ">>SEARCHARTICLES: '%s' has %s articles (%s returned)." % (term, len(subset), (len(subset) / 2))

		# Deletes the bottom 50% of our search subset
		subset = subset[0:len(subset)/2]
		self.sentimentscore = 0

		# Removes TFIDF values from the remaining articles and adds up the sentimentscore
		for i in range(len(subset)):
			x = subset[i]
			self.sentimentscore += self.articleIndex[x[0]][1]
			subset[i] = x[0]

		totalTime = round((time.time() - starttime), 3)

#		print ">>SEARCHARTICLES: Search has completed in %s seconds." % totalTime
		searchLog(term, len(subset), totalTime)
		sentimentArticleLog(term, self.sentimentscore)
		return subset

	def _getSentimentDict(self):
		dict_path = "data/sentiment_dictionaries/information_manual_sent.csv"
		with open(dict_path, "r") as csvfile:
			dictionary = {}
			with open(dict_path, "r") as csvfile:
				csv_dict = csv.reader(csvfile)
				for row in csv_dict:
					dictionary[row[0].decode('utf-8')] = row[1]
		return dictionary

	def _getSearchTerms(self):
		searchterms = []
		searchtermsfile = open(os.getcwd() + "/data/searchterms.txt", "r")
		for term in searchtermsfile:
			if len(term.split(" ")) > 1:
				startterm = term.split(" ")[0].strip()
				self.ngramterms[startterm] = []
				for x in term.split(" ")[1:]:
					gram = x.strip()
					self.ngramterms[term.split(" ")[0].strip()].append(gram)
					startterm += "_" + gram
				searchterms.append(startterm)
			else:
				searchterms.append(str(term).strip())

		print ">>SEARCHTERMS: %s." %(" | ".join(searchterms))
		return searchterms

	def _checkNgram(self, word, words, i):
		nextwords = self.ngramterms[word]
		comingwords = words[i+1:i+1+len(nextwords)]

		if len(comingwords) < len(nextwords): return []

		for i in range(len(comingwords)):
			tmpword = comingwords[i]
			tmpword = tmpword[:tmpword.find("/")]
			comingwords[i] = tmpword

		for x in range(len(nextwords)):
			if nextwords[x] != comingwords[x]: return [] 
		return comingwords


