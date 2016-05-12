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
from SyntacticParser.SyntacticParser import *
import os
import pickle
import csv


class POSCorpus():
	def __init__(self, inputfiles, subsetList):
		self.articleDict = {}
		self.inputfiles = inputfiles
		self.subsetList = subsetList
		self.scores = []
		self.sentimentdict = self.getSentimentDict()

	def load(self):
		inputpath = os.getcwd() + "/data/postagger_output/"

		joinedSubset = {}
		for subset_term in self.subsetList:
			for articleid in subset_term[1]:
				# print "articleid: ", articleid
				joinedSubset[articleid] = True

		for inputfilename in self.inputfiles:
			print ">>INDEX: Unpickling: \t '%s'." %inputfilename
			path = os.path.join(inputpath, inputfilename)
			pickledData = open(path, "r")
			tmp = pickle.load(pickledData)
			for x in tmp:
				# print "0: ", tmp[x][0]
				# print "lol: ", tmp[x][4]
				# self.articleDict[x] = tmp[x]
				if x in joinedSubset:
					self.articleDict[x] = tmp[x]
			pickledData.close()

	def score_sentiment(self, term_subset):
		term, subset = term_subset
		print ">>SENTIMENTSCORE: Scoring sentiment for '%s'." % term
		sentences = []
		sentimentscore = 0
		
		for articleid in subset:
			article = self.articleDict[articleid]
			tmp = self.get_sentences(article, term)
			for x in tmp:
				sentences.append(x)
			break

		print ">>SENTIMENTSCORE: Found %s sentences."%len(sentences)

		parser = SyntacticParser()

		for sentence in sentences:
			t = parser.parse_sentence(sentence)

			if t is not None:
				print t.tree
				sentimentscore += t.get_sentiment_score(self.sentimentdict, term)

		self.scores.append((term,sentimentscore))

	def get_sentences(self, article, term):
		sentenceList = []

		for entry in article[1:]:
			# print entry, len(repr(entry))
			if len(repr(entry)) < 7:
				continue
			# Split into sentences
			entry = entry.split("./TEGN")

			for sentences in entry:
				sentimenthit = False
				termhit = False

				sentence = []
				words = sentences.split(" ")

				for word in words:
					if word[:1] == "\n":
						word = word[1:]
					if word == "N":
						continue
					if len(word) < 1: 
						continue
					if word[:word.rfind("/")] in self.sentimentdict:
						# print ">> SENTIMENTHIT", word[:word.rfind("/")], " = ", self.sentimentdict[word[:word.rfind("/")]]
						sentimenthit = True
					if word[:word.rfind("/")] == term:
						# print ">> TERMHIT", term
						termhit = True
					sentence.append(word.split("/"))
					# print word[:word.rfind("/")]
					# print "word: %s" %repr(word)
				# print "--" * 20
				if sentimenthit and termhit:
					sentenceList.append(sentence)

		return sentenceList

	def print_sentence(self, sentence):
		sentencestring = ""
		for x in sentence:
			sentencestring += x[0] + " "
		print sentencestring


	def getSentimentDict(self):
		dict_path = "Corpus/sentiment_dictionaries/universal_dictionary.csv"
		with open(dict_path, "r") as csvfile:
			dictionary = {}
			with open(dict_path, "r") as csvfile:
				csv_dict = csv.reader(csvfile)
				for row in csv_dict:
					dictionary[row[0].decode('utf-8')] = row[1]
		return dictionary