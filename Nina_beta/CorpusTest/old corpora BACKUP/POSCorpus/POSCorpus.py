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
import pyximport; pyximport.install(setup_args={"include_dirs":numpy.get_include()},reload_support=True)
from SyntacticParser.SyntacticParserOptimised import SyntacticParser


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
		sentimentarr = []
		sentimentscore = 0
		bowscore = 0
		
		# Get sentences
		# p = Pool(4)
		# sentences += (p.map(multiSentence,subset))

		for articleid in subset:
			article = self.articleDict[articleid]
			tmp = self.get_sentences(article, term)
			for sentence in tmp:
				for word in sentence:
					if word[0] in self.sentimentdict:
						bowscore += int(self.sentimentdict[word[0]])
				# print " ".join([y[:y.find("/")] for y in x])
				sentences.append(sentence)
		subsetTime = time.time()

		print ">>SENTIMENTSCORE: Found %s sentences."%len(sentences)

		# p = Pool(4)
		# sentimentarr += (p.map(self.multiParse,sentences))
		# for x in sentimentarr:
		# 	if x != 0:
		# 		sentimentscore += x
		# 		parsedSentencesCount += 1

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
					# if score > 0.5:
					# 	print t.tree
					# 	print "score: %s" %score
					# 	print self.print_sentence(sentence)
					# 	print
					parsedSentencesCount += 1
					if sentimentscore == 0:
						sentimentscore = score
					else:
						sentimentscore = (sentimentscore + score) / 2
					# if parsedSentencesCount > 3:
					# 	break
					# print ">>SENTIMENTSCORE: ", self.print_sentence(sentence)
					# print "sentence: ", sentence
					# print t.tree
					# print ">>SENTIMENTSCORE: Current score is:", sentimentscore
					# print
		if len(sentences) == 0:
			bowscore = "0 (0)"
			sentencesCount = "0.0% (0/0)"
		else:
			bowscore = "%s (%s)" %(round(bowscore/float(len(sentences)),3),bowscore)
			sentencesCount = "%s%% (%s/%s)" %(round((parsedSentencesCount/float(len(sentences)))*100, 2), parsedSentencesCount, len(sentences))

		print ">>SENTIMENTSCORE: BOW SCORE IS: ", bowscore
		print ">>SENTIMENTSCORE: Final score is", sentimentscore
		print


		parseTime = round((time.time() - subsetTime), 3)
		subsetTime = round((subsetTime - starttime), 3)
		sentimentSentenceLog(term, sentencesCount, sentimentscore, bowscore, self.inputfiles, subsetTime, parseTime)
		# self.scores.append((term,sentimentscore))

	def multiParse(self, sentence):
		sentimentscore = []
		parser = SyntacticParser()
		# test_sentence = [x.split("/") for x in "To/NUM russere/N_INDEF_PLU tror/V_PRES ikke/ADV intet/ADJ ./TEGN".split(" ")]
		t = parser.parse_sentence(sentence)
		print "sentence: ", self.print_sentence(sentence), "\n\n"

		if t is not None:
			# print t.tree
			score = t.get_sentiment_score(self.sentimentdict, term)
			return score
		else:
			return 0
				


	def get_sentences(self, article, term):
		sentenceList = []
		ngrams = []
		if len(term.split("_")) > 1:
			tmp = term.split("_")
			term = tmp[0]
			ngrams = tmp[1:]

		for entry in article[1:]:

			# why?
			if len(repr(entry)) < 7:
				continue
			
			entry = entry.replace("\n", "")
			sentences = re.split('(\./\./TEGN|\?/\?/TEGN)', entry)

			for sentence in sentences:
				sentimenthit = False
				termhit = False

				# print "sentence:", sentence, "\n\n"

				output_sentence = []
				words = sentence.split(" ")

				for i in range(len(words)):
					word = words[i]
					lemma = word[:word.find("/")]
					if lemma[:1] == "\n": lemma = lemma[1:]
					if lemma == "N": continue
					if len(lemma) < 1: continue
					if lemma in self.sentimentdict:
						# print ">> SENTIMENTHIT:", lemma
						sentimenthit = True
					if lemma == term:
						if len(ngrams) > 0:
							comingwords, tag = self.checkNgram(lemma, ngrams, words, i)
							if len(comingwords) > 0:
								for x in comingwords:
									lemma += "_" + x
								tmpword = lemma + word[word.find("/"):]
								word = lemma + "/DONTCARE/" + tag
								for x in range(len(comingwords)):
									words[i+1+x] = ""
								termhit = True
							# print ">> TERMHIT", term
						else:
							termhit = True

					postaggedlemma = (re.sub('/[^>]+/', '/', word)).split("/")

					output_sentence.append(postaggedlemma)
					# print lemma[:lemma.rfind("/")]
					# print "lemma: %s" %repr(lemma)
				# print "--" * 20
				if sentimenthit and termhit:
					# print "orig: ", sentence
					# print "output", output_sentence
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

	def checkNgram(self, word, nextwords, words, i):
		comingwords = words[i+1:i+1+len(nextwords)]
		tagwords = []
		tagwords += comingwords
		if len(comingwords) < len(nextwords):
			return [[],""]


		for i in range(len(comingwords)):
			tmpword = comingwords[i]
			tmpword = tmpword[:tmpword.find("/")]
			comingwords[i] = tmpword

		for x in range(len(nextwords)):
			if nextwords[x] != comingwords[x]:
				return [[],""] 

		tag = self.findBestTag(tagwords)

		return [comingwords, tag]

	def findBestTag(self, comingwords):
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
		for word in comingwords:
			tmptag = word[word.rfind("/")+1:]
			if tmptag in preferredTags:
				if preferredTags[tmptag] > tag[0]:
					tag = (preferredTags[tmptag],tmptag)

		if tag[1] == "TAG":
			tag[1] = comingwords[len(comingwords)-1][word.rfind("/")+1:]
			print "No preferred tag. Last word in n-gram's tag chosen", tag[1]

		return tag[1]

def multiSentence(subset):
	term = "dansk_folkeparti"
	sentences = []
	for articleid in subset:
		article = POSCorpus.articleDict[articleid]
		tmp = POSCorpus.get_sentences(article, term)
		for sentence in tmp:
			for word in sentence:
				if word[0] in POSCorpus.sentimentdict:
					bowscore += int(POSCorpus.sentimentdict[word[0]])
			# print " ".join([y[:y.find("/")] for y in x])
			sentences.append(sentence)
	return sentences

