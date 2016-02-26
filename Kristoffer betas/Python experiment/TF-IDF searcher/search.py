import os
import glob
import operator
import math

invertedindexpath = os.getcwd() + "/TF-IDF indexer/inverted_index.txt"
articleindexpath = os.getcwd() + "/TF-IDF indexer/articlecounts.txt"

# invertedindexpath = os.getcwd() + "/inverted_index.txt"
# articleindexpath = os.getcwd() + "/articlecounts.txt"

invertedindex = open(invertedindexpath, "r")
articleindex = open(articleindexpath, "r")

totaldoccount = 0
for line in articleindex:
	totaldoccount += 1
articleindex.close()

term = raw_input("term? ")
term = str(hash("det"))

tmpresult = []

for line in invertedindex:
	if line.startswith(term):
		line = line.split(" ")
		doccount = len(line) - 4 # -4 since there are 4 entries in the array, that aren't articles.
		IDF = math.log10(totaldoccount / float(doccount))
		# print "IDF: %s / %s = %s" %(totaldoccount, doccount, IDF)
		for word in line:
			# print "LINE: %s" %line
			# print "LENGTH: %s" %len(line)
			if word.startswith("["):
				word = word.translate(None, "[]")
				word = word.split(":")
				#print "word %s" %word
				TF = 0
				articleindex = open(articleindexpath, "r")
				for line in articleindex:
					if line.startswith(word[0]):
						line = line.translate(None, ":")
						line = line.split(" ")
						#print "articlehit: %s" %line
						TF = line[2]
				articleindex.close()

				#print "TF = %s / %s" % (word[1], TF)
				TF = float(word[1]) / float(TF)
				TFIDF = TF * IDF
				# print "TF-IDF: %s * %s = %s" %(TF, IDF, TFIDF)
				word[1] = TFIDF
				tmpresult.append(tuple(word))
					
results = sorted(tmpresult, key=lambda result: result[1], reverse=True)

for lol in results[0:len(results)/2]:
	print lol