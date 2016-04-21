import sys
import polyglot
from polyglot.text import Text, Word
from polyglot.mapping import Embedding
import pickle
import random
import time
import re


# Global variables
grammar_tree = {}


def save_random_article():
	print ">>TEST: Unpickling data file"
	start_time = time.time()
	with open("../Discourse Machine/data/lemmatiser_output/udland.in") as file:
		data = pickle.load(file)
	print ">>TEST: Unpickled in", time.time() - start_time, "seconds"

	random_article = random.choice(data.keys())
	print ">>TEST: Working on article:", random_article

	with open("rand_article", "w") as file:
		pickle.dump(data[random_article], file)


# Set default coding to uft-8
reload(sys)
sys.setdefaultencoding('utf-8')


def load_data():
	print ">>TEST: Unpickling data file"
	with open("rand_article") as file:
		data = pickle.load(file)

	print ">>TEST: Stringing the article together"
	string = " ".join(data[4])
	string = re.sub('\|.*? ', ' ', string) # resolve lemma ambiguity by taking the first option
	string = string.decode('utf-8')
	text = Text(string)

	return text

	sentences = string.split(".") # Break up article into sentences
	sentence = sentences[3] # Extract test sentence





def build_sentence_matrix(n):
#	return [[False for x in range(n)] for y in range(n)]
	return [["[" +str(x) + "," + str(y) + "]" for x in range(n)] for y in range(n)]


def print_matrix(sentence_matrix):
	for entry in sentence_matrix:
		for cell in entry:
			print cell, "\t",
		print


def build_grammar():
	grammar_rules = []
	grammar_dict = {}

	grammar_dict["NP VP"] = [["S", 0.4]]
	grammar_dict["NEXUS VP"] = [["S", 0.2]]
	grammar_dict["VERB NP"] = [["VP", 0.4]]
	grammar_dict["PRON NOM"] = [["NP", 0.4]]
	grammar_dict["ADJ NOUN"] = [["NOM", 0.4]]
	grammar_dict["ADP PROPN"] = [["PP", 0.4]]
	grammar_dict["NP PP"] = [["NP", 0.4]]
	grammar_dict["PRON VERB"] = [["NEXUS", 0.4]]
	grammar_dict["NP VERB"] = [["NEXUS", 0.4]]
	grammar_dict["NEXUS NP"] = [["S", 0.4]]
	grammar_dict["NEXUS VP"] = [["S", 0.4]]
	grammar_dict["PRON NOUN"] = [["NP", 0.4]]
	grammar_dict["VERB ADJ"] = [["VP", 0.4]]
	grammar_dict["PRON VP"] = [["S", 0.2]]


	return grammar_dict




grammar_tree = build_grammar()

sentence = "Jeg er en glad studerende" # Set simple test sentence
print sentence

pos_sentence = Text(sentence).pos_tags # POS-tag sentence
print pos_sentence
sentence_matrix = build_sentence_matrix(len(pos_sentence)+1)
print_matrix(sentence_matrix)
print

sentence_length = len(pos_sentence)

# Fill out the NTs resolving to terminals
for i in range(1, sentence_length+1):
	sentence_matrix[1][i] = pos_sentence[i-1][1]

print ">>PARSE: With the filled-in terminal tags"
print_matrix(sentence_matrix)
print

# GO GO CKY ALGORITHM
for substring_length in range(2, sentence_length+1):
	print "New substring of length...", substring_length
	for substring_start in range(1, (sentence_length - substring_length)+2):
		for split_point in range(1, substring_length):
			b = sentence_matrix[split_point][substring_start]
			c = sentence_matrix[substring_length - split_point][substring_start + split_point]
			grammar_rule = (str(b[0]) + " " + str(c)[0])
			print "Evaluating...", grammar_rule
			if grammar_rule in grammar_tree:
				print "Using rule..."
				m = 0
				for nt in grammar_tree[grammar_rule]:
					if b[1] * c[1] * nt[1] > m:
						sentence_matrix[substring_length][substring_start] = grammar_tree[grammar_rule]
	print_matrix(sentence_matrix)

print ">>PARSE: The finished product."
print_matrix(sentence_matrix)




