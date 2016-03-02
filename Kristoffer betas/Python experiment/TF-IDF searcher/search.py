import os
import glob
import operator
import math
import pickle

invertedindexpath = os.getcwd() + "/TF-IDF indexer/inverted_index.in"
articleindexpath = os.getcwd() + "/TF-IDF indexer/articlecounts.in"
searchtermspath = os.getcwd() + "/TF-IDF searcher/searchterms.txt"

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

searchterms = open(searchtermspath, "r")

results = []

for term in searchterms:
	term = str(term).strip()
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
			# print "TFIDF: %s * %s = %s" % (TF, IDF, TFIDF)
	else:
		print "The term '%s' does not exist in the corpus." %term
	if len(tmpresult) < 1:
		continue
	# Sort results on their TFIDF rating, in decreasing order.
	tmpresult = sorted(tmpresult, key=lambda result: result[1], reverse=True)
	# Deletes the bottom 50% of our search results
	tmpresult = tmpresult[0:len(tmpresult)/2]
	if len(tmpresult) > 0:
		results.append((term,tmpresult))


for result in results:
	print result[0]
	for articles in result[1]:
		print articles