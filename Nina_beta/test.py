import sys
import polyglot
from polyglot.text import Text, Word
from polyglot.mapping import Embedding



# embeddings = Embedding.load("../Discourse Machine/data/lemmatiser_output/udland.in.tar.gz")
# neighbors = embeddings.nearest_neighbors("engells")
# print neighbors

text = Text("Vi gik en meget lang tur i dag.")
#print text.words
print text.pos_tags

text = Text("The movie was a huge blast of fun.")
print("{:<16}{}".format("Word", "Polarity")+"\n"+"-"*30)
for w in text.words:
    print("{:<16}{:>2}".format(w, w.polarity))


#print("Language Detected: Code={}, Name={}\n".format(text.language.code, text.language.name))
