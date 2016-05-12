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
import os
import pickle

class POSCorpus():
	def __init__(self, inputfiles, subsetList):
		self.articleDict = {}
		self.inputfiles = inputfiles
		self.subsetList = []
		self.scores = []

	def load(self):
		inputpath = os.getcwd() + "/data/postagger_output/"

		joinedSubset = {}
		for tuple in self.subsetList:
			for articleid in tuple[1]:
				joinedSubset[articleid] = True

		for inputfilename in self.inputfiles:
			print ">>INDEX: Unpickling: \t '%s'." %inputfilename
			path = os.path.join(inputpath, inputfilename)
			pickledData = open(path, "r")
			tmp = pickle.load(pickledData)
			for x in tmp:
				# print "0: ", tmp[x][0]
				# print "lol: ", tmp[x][4]
				self.articleDict[x] = tmp[x]
				# if x in joinedSubset:
				# 	articleDict[x] = tmp[x]
			pickledData.close()

	def score_sentiment(self, subsetList):
		term, subset = subsetList
		sentences = []
		sentimentscore = 0
		
		for articleid in subset:
			# article = self.articleDict[articleid]
			article = self.articleDict.popitem()

			sentences.append(self.get_sentences(article))

		# for sentence in sentences:
		# 	sentimentscore += syntacticParser(sentence)

		# self.scores.append((term,sentimentscore))

	def get_sentences(self, article):
		sentenceList = []
		for entry in article[1][1:]:
			# print entry, len(repr(entry))
			if len(repr(entry)) < 7:
				continue
			# Split into sentences
			entry = entry.split("./TEGN")

			for sentences in entry:
				sentence = []
				words = sentences.split(" ")

				for word in words:
					if word[:1] == "\n":
						word = word[1:]
					if word == "N":
						continue
					if len(word) < 1: 
						continue
					sentence.append(word)
					# print "word: %s" %repr(word)
				print sentence
				sentenceList.append(sentence)

		return sentenceList
