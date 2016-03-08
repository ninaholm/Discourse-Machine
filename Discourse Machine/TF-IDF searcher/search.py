import os
import glob
import operator
import math
import pickle

invertedindexpath = os.getcwd() + "/TF-IDF indexer/inverted_index.in"
articleindexpath = os.getcwd() + "/TF-IDF indexer/articlecounts.in"

# invertedindexpath = os.getcwd() + "/inverted_index.txt"
# articleindexpath = os.getcwd() + "/articlecounts.txt"

tempIndex = open(invertedindexpath, "rb")
string = ""
for line in tempIndex:
	string += line
invertedindex = pickle.loads(string)
tempIndex.close()

tempIndex = open(articleindexpath, "rb")
string = ""
for line in tempIndex:
	string += line
articleindex = pickle.loads(string)
tempIndex.close()

totaldoccount = len(articleindex)

term = str(raw_input("term? "))

tmpresult = []

if hash(term) in invertedindex:
	articlehits = invertedindex[hash(term)][1]
	doccount = len(articlehits)
	IDF = math.log10(totaldoccount / float(doccount))

	for article in articlehits:
		wordcount = articlehits[article]
		articlewordcount = articleindex[article]
		TF = wordcount / float(articlewordcount)
		TFIDF = TF * IDF
		tmpresult.append((article,TFIDF))
		print "TFIDF: %s * %s = %s" % (TF, IDF, TFIDF)

# Sort results on their TFIDF rating, in decreasing order.
results = sorted(tmpresult, key=lambda result: result[1], reverse=True)

# Print the top 50% of our results
for result in results[0:len(results)/2]:
	print result