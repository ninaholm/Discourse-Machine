import sys
import polyglot
from polyglot.text import Text, Word
from polyglot.mapping import Embedding
import pickle
import random
import time


# embeddings = Embedding.load("../Discourse Machine/data/lemmatiser_output/udland.in.tar.gz")
# neighbors = embeddings.nearest_neighbors("engells")
# print neighbors


def save_random_article():
	print ">>TEST: Unpickling data file"
	start_time = time.time()
	with open("../Discourse Machine/data/lemmatiser_output/udland.in") as file:
		data = pickle.load(file)
	print ">>TEST: Unpickled in", time.time() - start_time, "seconds"

	random_article = random.choice(data.keys())
	print ">>TEST: Working on article:", random_article

	with open("temp", "w") as file:
		pickle.dump(data[random_article], file)

print ">>TEST: Unpickling data file"
with open("temp") as file:
	data = pickle.load(file)

print ">>TEST: Stringing the article along"
string = " ".join(data[4])
string = string.decode('utf-8')
text = Text(string)

# print ">>TEST: POS-tagging the article"
# print text.pos_tags

print ">>TEST: Sentiment analysing the article"
print("{:<16}{}".format("Word", "Polarity")+"\n"+"-"*30)
for w in text.words:
	pol = w.polarity
	print w, pol
	if pol is not 0:
		print "{:<16}{:>2}".format(w.decode('utf-8'), pol)


#print("Language Detected: Code={}, Name={}\n".format(text.language.code, text.language.name))
