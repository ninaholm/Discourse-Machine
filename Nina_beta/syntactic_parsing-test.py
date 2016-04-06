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
	return [["[" +str(x) + "," + str(y) + "]" for x in range(n)] for y in range(n)] 


def print_matrix(sentence_matrix):
	for entry in sentence_matrix:
		for cell in entry:
			print cell, "\t",
		print


def build_grammar():
	grammar_rules = []
	# grammar_rules.append(["S", "NP VP"])
	# grammar_rules.append(["VP", "VERB NP"])
	# grammar_rules.append(["NP", "PRON NOM"])
	# grammar_rules.append(["NOM", "ADJ NOUN"])
	# grammar_rules.append(["PP", "ADP PROPN"])
	# grammar_rules.append(["NP", "NP PP"])
	# grammar_rules.append(["NP", "NOUN"])
	# grammar_rules.append(["NP", "PROPN"])
	# grammar_rules.append(["VP", "VERB NP"])
	grammar_rules.append(["NEXUS", "PRON VERB"])
	# grammar_rules.append(["S", "NEXUS NP"])
	grammar_rules.append(["S", "NEXUS VP"])
	# grammar_rules.append(["NP", "PRON NOUN"])
	grammar_rules.append(["VP", "VERB ADJ"])
	grammar_rules.append(["", ""])
	grammar_rules.append(["", ""])

	grammar_tree = {}
	for entry in grammar_rules:
		grammar_tree[entry[1]] = entry[0]

	return grammar_tree


def in_grammar(construction):
	if construction in grammar_tree:
		return grammar_tree[construction]
	else:
		return None


grammar_tree = build_grammar()

sentence = "Jeg var en glad student" # Set simple test sentence
sentence = "Jeg er glad" # Set simple test sentence
print sentence

pos_sentence = Text(sentence).pos_tags # POS-tag sentence
sentence_matrix = build_sentence_matrix(len(pos_sentence))
# print_matrix(sentence_matrix)



for j in range(0, len(sentence_matrix)):
	sentence_matrix[j][j] = pos_sentence[j][1]
	
	for i in range(j-1,-1,-1):
		current_cell_to_fill = sentence_matrix[i][j]
		print current_cell_to_fill

		construction = sentence_matrix[i+1][j] + sentence_matrix[i][j-1]
		sentence_matrix[i][j] = in_grammar(construction)

		# for k in range(j-1, i-1, -1):
		# 	current_cell_2 = sentence_matrix[i][k]

		# 	construction = current_cell_2 + " " + sentence_matrix[j][j]
		# 	print construction
		# 	r = in_grammar(construction)
		# 	print r
		# 	if r is not None:
		# 		sentence_matrix[i][j] = r

	print_matrix(sentence_matrix)
			


			#print current_cell_1, " ---- ", current_cell_2

#			construction = sentence_matrix[i][k] + " " + sentence_matrix[k][j]
#			print construction
	print







# while True:
# 	temp_sentence = ""
# 	for i in range(0, len(sentence_matrix)-1):
# 		construction = pos_sentence[i][1] + " " + pos_sentence[i+1][1]
# 		print construction
# 		rule = in_grammar(construction)
# 		if rule is not None:
# 			sentence_matrix[i][i+1] = rule
# 			print_matrix(sentence_matrix)








# print ">>TEST: Sentiment analysing the article"
# print("{:<16}{}".format("Word", "Polarity")+"\n"+"-"*30)
# for w in text.words:
# 	pol = w.polarity
# 	print w, pol
# 	if pol is not 0:
# 		print "{:<16}{:>2}".format(w.decode('utf-8'), pol)


#print("Language Detected: Code={}, Name={}\n".format(text.language.code, text.language.name))
