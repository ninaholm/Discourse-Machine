import os
import glob
import operator
import time

def index(parsedCorpus):
	starttime = time.time()
	print ">>INDEX: TF-IDF indexing started."
	index = {}
	articlecounts = {}
	inputpath = os.getcwd() + "/XML_parser/output"

	doccount = 0
	totalwordcount = 0

	for doc in parsedCorpus:
		doccount += 1
		wordcount = 0

		articleid = os.path.split(doc)[1]

		line = parsedCorpus[doc].lower().strip().split()


		# line = parsedCorpus[doc].split(" ").lower().strip()



		for word in line:
			if len(word) < 1:
				continue
			wordcount += 1
			word = word.translate(None, "!@#$,.'")
			word = word.translate(None, '<[]():^%">?*/_+')

			if hash(word) in index:
				if articleid in index[hash(word)][1]:
					index[hash(word)][1][articleid] += 1 
				else:
					index[hash(word)][1][articleid] = 1
		
			else:
				index[hash(word)] = [word, {articleid:1}]
			#print "articleid: %s" % index[hash(word)]
		totalwordcount += wordcount
		articlecounts[articleid] = wordcount

	print ">>INDEX: %s words in total." % totalwordcount
	print ">>INDEX: %s unique words indexed." % len(index)
	print ">>INDEX: Document average length is %s." % (totalwordcount / doccount)

	returndicts = [index, articlecounts]

	print ">>INDEX: TF-IDF indexing completed in %s seconds." % round((time.time() - starttime), 3)

	return returndicts
