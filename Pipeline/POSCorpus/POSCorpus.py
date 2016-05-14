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
import re


class POSCorpus():
	def __init__(self, inputfiles, subsetList):
		self.articleDict = {}
		self.inputfiles = inputfiles
		self.subsetList = subsetList
		self.scores = []
		self.sentimentdict = self.getSentimentDict()

	def load(self):
		print ">>INDEX: Building corpus for syntactic analysis."
		inputpath = os.getcwd() + "/data/monster_output/"

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
		
		# Get senteces
		for articleid in subset:
			article = self.articleDict[articleid]
			tmp = self.get_sentences(article, term)
			for x in tmp:
				# print " ".join([y[:y.find("/")] for y in x])
				sentences.append(x)


		print ">>SENTIMENTSCORE: Found %s sentences."%len(sentences)

		parser = SyntacticParser()

		for sentence in sentences:
			# s = "To/NUM russere/N_INDEF_PLU tror/V_PRES ikke/ADV intet/ADJ ./TEGN"
			t = parser.parse_sentence(sentence)

			if t is not None:
				print t.tree
				sentimentscore += t.get_sentiment_score(self.sentimentdict, term)
			print "SENTIMENTSCORE: Current score is:", sentimentscore

		self.scores.append((term,sentimentscore))

	def get_sentences(self, article, term):
		sentenceList = []

		for entry in article[1:]:

			# why?
			if len(repr(entry)) < 7:
				continue
			
			entry = entry.replace("\n", "")
			sentences = re.split('(\./\./TEGN|\?/\?/TEGN)', entry)

			for sentence in sentences:
				sentimenthit = False
				termhit = False

				output_sentence = []
				words = sentence.split(" ")

				for word in words:
					lemma = word[:word.find("/")]

					if lemma[:1] == "\n": lemma = lemma[1:]
					if lemma == "N": continue
					if len(lemma) < 1: continue
					if lemma in self.sentimentdict:
						# print ">> SENTIMENTHIT:", lemma
						sentimenthit = True
					if lemma == term:
						# print ">> TERMHIT", term
						termhit = True

					postaggedlemma = (re.sub('/[^>]+/', '/', word)).split("/")

					output_sentence.append(postaggedlemma)
					# print lemma[:lemma.rfind("/")]
					# print "lemma: %s" %repr(lemma)
				# print "--" * 20
				if sentimenthit and termhit:
					# print " ".join([x[:x.find("/")] for x in output_sentence])
					sentenceList.append(output_sentence)
				
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




