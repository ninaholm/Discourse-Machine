# POSCorpus:
# 	articleDict = {articleid : POStagged articles}
# 	sentimentscore = [(term:score)]
# 	searchterms = [(term:subsetlist)]

# 	load(inputfiles):
# 		Loads the POS tagged articles and filters them (based on joined subsetlists) into the articleDict.

# 	score_sentiment(term, subsetlist):
# 		Calls get_sentences()
# 		Feeds the syntactic parser every sentence get_sentences() returns and adds up the score.
# 		Returns final score to main.

# 	get_sentences(term, subsetlist):
# 		Reads through all articles in the subsetlist and returns every sentence with the term in it.

# 		returns [sentences]
#from SyntacticParser.SyntacticParser import *
from log.logger import sentimentSentenceLog
from multiprocessing import *
import os
import pickle
import csv
import re
import time
import numpy
from Corpus.corpus import Corpus
import pyximport; pyximport.install(setup_args={"include_dirs":numpy.get_include()},reload_support=True)
from SyntacticParser.SyntacticParserOptimised import SyntacticParser


class PipelineHandler():
	def __init__(self, inputfiles):
		self.inputfiles = inputfiles
		self.sentiment_scores = []
		self.parser = SyntacticParser()


	def run(self):

		for inputfile in self.inputfiles:
			subsetList = []
			c = Corpus(inputfile)
			c.index()

			for term in c.searchterms:
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


				







# def multiParse(self, sentence):
# 	sentimentscore = []
# 	parser = SyntacticParser()
# 	# test_sentence = [x.split("/") for x in "To/NUM russere/N_INDEF_PLU tror/V_PRES ikke/ADV intet/ADJ ./TEGN".split(" ")]
# 	t = parser.parse_sentence(sentence)
# 	print "sentence: ", self.print_sentence(sentence), "\n\n"

# 	if t is not None: return t.get_sentiment_score(self.sentimentdict, term)
# 	else: return 0



# def multiSentence(subset):
# 	term = "dansk_folkeparti"
# 	sentences = []
# 	for articleid in subset:
# 		article = POSCorpus.articleDict[articleid]
# 		tmp = POSCorpus.get_sentences(article, term)
# 		for sentence in tmp:
# 			for word in sentence:
# 				if word[0] in POSCorpus.sentimentdict:
# 					bowscore += int(POSCorpus.sentimentdict[word[0]])
# 			# print " ".join([y[:y.find("/")] for y in x])
# 			sentences.append(sentence)
# 	return sentences

