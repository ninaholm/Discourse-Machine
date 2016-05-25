
from log.logger import sentimentSentenceLog
from Corpus.Corpus import Corpus
import pyximport; pyximport.install()
from SyntacticParser.SyntacticParserOptimised import SyntacticParser
import os
import glob
import pickle
import time
import csv

class PipelineHandler():
	def __init__(self, corpora):
		self.corpora = corpora
		self.sentiment_scores = []
		self.parser = SyntacticParser()
		self.searchterms, self.ngramterms = self._getSearchTerms() # list of strings
		self.sentimentDict = self._getSentimentDict() # {sentimentWord: score}


	def run(self):

		for corpus in self.corpora:
			subsetList = []
			c = Corpus(corpus)
			c.ngramterms = self.ngramterms
			c.sentimentDict = self.sentimentDict
			c.index()

			for term in self.searchterms:
				subset = c.search(term)
				if len(subset) == 0: continue
				else: subsetList.append((term, subset))

			c.clear_indices() # Saves memory

			for term_subset in subsetList:
				bowscore, sentimentscore = c.score_sentiment(term_subset, self.parser)
				self.sentiment_scores.append([term_subset[0], bowscore, sentimentscore])

		self.print_scores()


	def print_scores(self):
		for entry in self.sentiment_scores:
			print entry[0] + "\t| BOW score: " + str(entry[1]) + "\t| Syntactic score: " + str(entry[2])


			

	def _getSentimentDict(self):
		dict_path = "data/sentiment_dictionaries/information_manual_sent.csv"
		dictionary = {}
		with open(dict_path, "r") as csvfile:
			csv_dict = csv.reader(csvfile)
			for row in csv_dict:
				dictionary[row[0].decode('utf-8')] = row[1]
		return dictionary


	def _getSearchTerms(self):
		searchterms = []
		ngramterms = {}
		with open(os.getcwd() + "/data/searchterms.txt", "r") as searchtermsfile:
			for term in searchtermsfile:
				if len(term.split(" ")) > 1:
					startterm = term.split(" ")[0].strip().lower()
					finalterm = startterm
					ngramterms[startterm] = []
					for gram in [x.strip() for x in term.split(" ")][1:]:
						ngramterms[startterm].append(gram)
						finalterm += "_" + gram.lower()
					searchterms.append(finalterm)
				else:
					searchterms.append(str(term).strip().lower())

		print ">>SEARCHTERMS: %s." %(" | ".join(searchterms))
		return (searchterms, ngramterms)

