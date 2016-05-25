#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
import pickle
import time
import math
import csv
import re
from log.logger import indexLog, searchLog, sentimentArticleLog, sentimentSentenceLog

import random #for testing purposes

# Takes an array of inputfilenames, which is indexed into a dictionary with words as keys and [(articleid, count)] as values. 
# A dictionary of articles are also returned, with articleids as keys and totalwordcount as values.
# logdict[inputfile(s) + "-index"]: [Which file(s) has been indexed, # articles, # unique words, # average words/article, time to unpickle, time to index and time in total].

class Corpus:
	def __init__(self, inputfiles):
		self.wordIndex = {}	# {word: [(articleid, number of occurrences in article)]}
		self.articleIndex = {} # {articleid: (totalwordcount, sentimentscore)}
		self.inputfiles = inputfiles
		self.articleDict = self._import_data(inputfiles) # {articleid: [date, header, subheader, picture text, article body]}
		self.ngramterms = {}
		self.searchterms = [] # list of strings
		self.sentimentDict = {} # {sentimentWord: score}
		self.sentimentScore = 0


	def _import_data(self, inputfiles):
		inputpath = os.getcwd() + "/data/monster_output"
		articleDict = {}

		pickleTime = time.time()
		for inputfilename in inputfiles:
			print ">>INDEX: Unpickling: \t '%s'." %inputfilename
			path = os.path.join(inputpath, inputfilename)
			with open(path, "r") as pickledData:
				tmp = pickle.load(pickledData)
				articleDict.update(tmp)
		pickleTime = round((time.time() - pickleTime), 3)
		return articleDict


	def index(self):
		starttime = time.time() # logging purposes
		print ">>INDEX: Word indexing started."
		doccount = 0 # logging purposes
		totalwordcount = 0 # logging purposes

		indexTime = time.time() # logging purposes
		print ">>INDEX: Indexing %s articles." % len(self.articleDict)
		for articleid in self.articleDict:
			doccount += 1 # logging purposes
			wordcount = 0
			sentimentcount = 0

			for line in self.articleDict[articleid]:
				if len(line) < 1: continue
				sentence = line.split(" ")

				for i in range(len(sentence)):
					word = sentence[i]
					word = word[:word.find("/")]
					if "|" in word:
						word = word[:word.find("|")]
					if len(word) < 1: continue
					if word in self.sentimentDict: sentimentcount += int(self.sentimentDict[word])
					if word in self.ngramterms:
						comingwords = self._checkNgram(word, self.ngramterms[word], sentence, i, False)[0]

						if len(comingwords) > 0:
							word += "_" + "_".join(comingwords)
							i += len(comingwords)
							wordcount += len(comingwords)

					wordcount += 1
					if word in self.wordIndex:
						if articleid in self.wordIndex[word]: self.wordIndex[word][articleid] += 1 
						else: self.wordIndex[word][articleid] = 1
					else:
						self.wordIndex[word] = {articleid:1}

			totalwordcount += wordcount # logging purposes
			self.articleIndex[articleid] = (wordcount, sentimentcount)

		# Function done. Now printing and logging!
		wcount = 0
		for x in self.wordIndex:
			if len(self.wordIndex[x]) > 50:
				print x
				if wcount > 30:
					break
				else:
					wcount += 1

		indexTime = round((time.time() - indexTime), 3) # logging purposes

		print ">>INDEX: %s words in total." % totalwordcount
		print ">>INDEX: %s unique words indexed." % len(self.wordIndex)
		print ">>INDEX: Document average length is %s." % (totalwordcount / doccount)

		totalTime = round((time.time() - starttime), 3) # logging purposes

		print ">>INDEX: Word indexing completed in %s seconds. \n" % totalTime
		# print "pickletime: ", pickleTime
		print "indextime: ", indexTime
		print "doccount: ", doccount
		indexLog(self.inputfiles, len(self.articleDict), len(self.wordIndex), (totalwordcount / doccount), 0, indexTime, totalTime)


	# Clears the two indexes
	def clear_indices(self):
		self.wordIndex = {}
		self.articleIndex = {}


	# Returns the top 50% subset of articles wherein a search term and an opinion word are found.
	def search(self, searchTerm):
		starttime = time.time() # logging purposes
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

		totalTime = round((time.time() - starttime), 3) # logging purposes

		print ">>SEARCHARTICLES: Search has completed in %s seconds." % totalTime
		searchLog(term, len(subset), totalTime) # logging purposes
		sentimentArticleLog(term, self.sentimentscore) # logging purposes
		return subset


	def _checkNgram(self, word, restOfNgram, words, i, tagNeeded):
		comingwords = words[i+1:i+1+len(restOfNgram)]
		taggedwords = []
		taggedwords += comingwords
		tag = ""

		if len(comingwords) < len(restOfNgram): return [[],""]

		# Removes unnecessary tags from comingwords
		for i in range(len(comingwords)):
			nextword = comingwords[i][:comingwords[i].find("/")]
			comingwords[i] = nextword

		# Compares ngram to comingswords
		for j in range(len(restOfNgram)):
			if restOfNgram[j] != comingwords[j]: return [[],""] 

		if tagNeeded:
			tag = self._findBestTag(taggedwords)

		return [comingwords, tag]




	def get_sentences(self, article, term):
		sentenceList = []
		ngram = []
		if len(term.split("_")) > 1:
			tmp = term.split("_")
			term = tmp[0]
			ngram = tmp[1:]

		for entry in article[1:]:

			if len(repr(entry)) < 7: continue # bad data check
			
			entry = entry.replace("\n", "")
			sentences = re.split('(\./\./TEGN|\?/\?/TEGN)', entry)

			for strsentence in sentences:
				sentimenthit = False
				termhit = False

				output_sentence = []
				sentence = strsentence.split(" ")

				for i in range(len(sentence)):
					word = sentence[i]
					lemma = word[:word.find("/")]
					if lemma[:1] == "\n": lemma = lemma[1:]
					if lemma == "N" or len(lemma) < 1: continue
					if lemma in self.sentimentDict: sentimenthit = True
					if lemma == term:
						if len(ngram) > 0:
							comingwords, tag = self._checkNgram(lemma, ngram, sentence, i, True)
							if len(comingwords) > 0:
								lemma += "_" + "_".join(comingwords)
								word = lemma + "/DONTCARE/" + tag
								for j in range(len(comingwords)):
									sentence[i+1+j] = "" # Nullifies comingwords from sentence
								termhit = True
							# print ">> TERMHIT", term
						else:
							termhit = True

					postaggedlemma = (re.sub('/[^>]+/', '/', word)).split("/")
					output_sentence.append(postaggedlemma)

				if sentimenthit and termhit: sentenceList.append(output_sentence)
				
		return sentenceList



	def _findBestTag(self, taggedwords):
		preferredTags = {
		"V_GERUND":5,  "V_IMP":5,
		"V_INF":5, "V_INF_PAS":5,
		"V_PARTC_PAST":5, "V_PARTC_PRES":5,
		"V_PAST":5, "V_PAST_PAS":5,
		"V_PRES":5, "V_PRES_PAS":5,
		"EGEN":4, "EGEN_GEN":4, "NNP":4,
		"N_DEF_PLU":3, "N_DEF_PLU_GEN":3,
		"N_DEF_SING":3,"N_DEF_SING_GEN":3,
		"N_INDEF":3,"N_INDEF_PLU":3,
		"N_INDEF_PLU_GEN":3,"N_INDEF_SING":3,
		"N_INDEF_SING_GEN":3,"N_PLU":3,
		"N_SING":3,"N_SING_GEN":3, "N":3,
		"ADJ":2, "ADJ_GEN":2, 
		"ADV":1, "NAMEX_ADV[1]":1}

		tag = [0,"TAG"]
		for word in taggedwords:
			tmptag = word[word.rfind("/")+1:]
			if tmptag in preferredTags:
				if preferredTags[tmptag] > tag[0]:
					tag = [preferredTags[tmptag],tmptag]

		if tag[1] == "TAG":
			tag[1] = taggedwords[len(taggedwords)-1][word.rfind("/")+1:]
			print "No preferred tag. Last word in n-gram's tag chosen", tag[1]

		return tag[1]



	def print_sentence(self, sentence):
		sentencestring = ""
		for x in sentence:
			y = x[0]
			if "|" in y:
				sentencestring += y[:y.find("|")] + " "
			else:
				sentencestring += y + " "
		return sentencestring



	def score_sentiment(self, term_subset, parser):
		starttime = time.time()
		term, articleSubset = term_subset
		print ">>SENTIMENTSCORE: Scoring sentiment for '%s'." % term
		sentences = []
		sentimentscore = 0
		bowscore = 0
		parsedSentencesCount = 0 # logging purposes

		# Extract sentences from list of articles
		for articleid in articleSubset:
			article = self.articleDict[articleid]
			for s in self.get_sentences(article, term):
				for sentence in s:
					for word in sentence:
						if word[0] in self.sentimentDict:
							bowscore += int(self.sentimentDict[word[0]])
				sentences.append(s)


		subsetTime = time.time()
		print ">>SENTIMENTSCORE: Found %s sentences."%len(sentences)

		# Parse all sentences
		for sentence in sentences:
			t = parser.parse_sentence(sentence)

			if t is not None:
				score = t.get_sentiment_score(self.sentimentDict, term)
				if score != 0:
					parsedSentencesCount += 1  # logging purposes
					if sentimentscore == 0: sentimentscore = score
					else: sentimentscore = (sentimentscore + score) / 2

		# Set BOW score
		if len(sentences) == 0:
			bowscore = "0 (0)"
			sentencesCount = "0.0% (0/0)"  # logging purposes
		else:
			bowscore = "%s (%s)" %(round(bowscore/float(len(sentences)),3),bowscore)
			sentencesCount = "%s%% (%s/%s)" %(round((parsedSentencesCount/float(len(sentences)))*100, 2), parsedSentencesCount, len(sentences))  # logging purposes

		print ">>SENTIMENTSCORE: BOW SCORE IS: ", bowscore
		print ">>SENTIMENTSCORE: Final score is", sentimentscore
		print

		parseTime = round((time.time() - subsetTime), 3)  # logging purposes
		subsetTime = round((subsetTime - starttime), 3) # logging purposes
		sentimentSentenceLog(term, sentencesCount, sentimentscore, bowscore, self.inputfiles, subsetTime, parseTime) # logging purposes

		return (bowscore, sentimentscore)
