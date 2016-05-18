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
<<<<<<< HEAD
#from SyntacticParser.SyntacticParser import *
=======
from SyntacticParser.SyntacticParser import *
>>>>>>> f5158ee454ea3ca513b5dea1ece47671325a7b59
from log.logger import sentimentSentenceLog
import os
import pickle
import csv
import re
import time
<<<<<<< HEAD
import pyximport; pyximport.install()
from SyntacticParser.SyntacticParserOptimised import SyntacticParser
=======
>>>>>>> f5158ee454ea3ca513b5dea1ece47671325a7b59


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
			for articleid in tmp:
				# print "0: ", tmp[x][0]
				# print "lol: ", tmp[x][4]
				# self.articleDict[x] = tmp[x]
				if articleid in joinedSubset:
					self.articleDict[articleid] = tmp[articleid]
			pickledData.close()

	def score_sentiment(self, term_subset):
		starttime = time.time()
		term, subset = term_subset
		print ">>SENTIMENTSCORE: Scoring sentiment for '%s'." % term
		sentences = []
		sentimentscore = 0
		
		# Get senteces
		for articleid in subset:
			article = self.articleDict[articleid]
			tmp = self.get_sentences(article, term)
			for sentence in tmp:
				# print " ".join([y[:y.find("/")] for y in x])
				sentences.append(sentence)
		subsetTime = time.time()

		print ">>SENTIMENTSCORE: Found %s sentences."%len(sentences)


		parser = SyntacticParser()
		parsedSentencesCount = 0

		for sentence in sentences:
			# test_sentence = [x.split("/") for x in "To/NUM russere/N_INDEF_PLU tror/V_PRES ikke/ADV intet/ADJ ./TEGN".split(" ")]
			t = parser.parse_sentence(sentence)
			# print "sentence: ", self.print_sentence(sentence), "\n\n"

			if t is not None:
				# print t.tree
				score = t.get_sentiment_score(self.sentimentdict, term)
				if score != 0:
					parsedSentencesCount += 1
					if sentimentscore == 0:
						sentimentscore = score
					else:
						sentimentscore = (sentimentscore + score) / 2
<<<<<<< HEAD
					# print ">>SENTIMENTSCORE: ", self.print_sentence(sentence)
					# print ">>SENTIMENTSCORE: Current score is:", sentimentscore
					# print
		print ">>SENTIMENTSCORE: Final score is", sentimentscore
		print
					
=======
					print ">>SENTIMENTSCORE: ", self.print_sentence(sentence)
					print ">>SENTIMENTSCORE: Current score is:", sentimentscore
					print
					break
>>>>>>> f5158ee454ea3ca513b5dea1ece47671325a7b59
					

		sentencesCount = "%s%% (%s/%s)" %(round((parsedSentencesCount/float(len(sentences)))*100, 2), parsedSentencesCount, len(sentences))

		parseTime = round((time.time() - subsetTime), 3)
		subsetTime = round((subsetTime - starttime), 3)
		sentimentSentenceLog(term, sentencesCount, sentimentscore, self.inputfiles, subsetTime, parseTime)
		# self.scores.append((term,sentimentscore))

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
			y = x[0]
			if "|" in y:
				sentencestring += y[:y.find("|")] + " "
			else:
				sentencestring += y + " "
		return sentencestring


	def getSentimentDict(self):
		dict_path = "data/sentiment_dictionaries/information_manual_sent.csv"
		with open(dict_path, "r") as csvfile:
			dictionary = {}
			with open(dict_path, "r") as csvfile:
				csv_dict = csv.reader(csvfile)
				for row in csv_dict:
					dictionary[row[0].decode('utf-8')] = row[1]
		return dictionary




