
from log.logger import sentimentSentenceLog
from Corpus.Corpus import Corpus
import pyximport; pyximport.install()
from SyntacticParser.SyntacticParserOptimised import SyntacticParser


class PipelineHandler():
	def __init__(self, corpora):
		self.corpora = corpora
		self.sentiment_scores = []
		self.parser = SyntacticParser()


	def run(self):

		for corpus in self.corpora:
			subsetList = []
			c = Corpus(corpus)
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


				
