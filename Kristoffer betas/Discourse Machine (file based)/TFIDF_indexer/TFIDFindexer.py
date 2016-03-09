import os
import glob
import operator
import pickle
import time

def index(self):
	starttime = time.time()
	print ">>INDEX: TF-IDF indexing started."
	index = {}
	articlecounts = {}
	inputpath = os.getcwd() + "/XML_parser/output"

	doccount = 0
	totalwordcount = 0

	for file in glob.glob(os.path.join(inputpath, '*.txt')):
		doc = open(file, "r")
		doccount += 1
		wordcount = 0
		articleid = os.path.split(file)[1]

		for line in doc:
			#print "line: %s" % line
			line = line.lower().strip()

			if len(line) < 2:
				continue

			line = line.split(" ")

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

	indexpickle = pickle.dumps(index)
	countdb = open(os.path.dirname(os.path.abspath(__file__)) + '/inverted_index.in', 'wb')
	countdb.write(indexpickle)
	countdb.close()

	articlepickle = pickle.dumps(articlecounts)
	articledb = open(os.path.dirname(os.path.abspath(__file__)) + '/articlecounts.in', 'wb')
	articledb.write(articlepickle)
	articledb.close()

	print ">>INDEX: TF-IDF indexing completed in %s seconds." % round((time.time() - starttime), 3)

