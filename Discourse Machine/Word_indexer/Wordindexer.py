#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
import operator
import pickle
import time

def index(self):
	starttime = time.time()
	print ">>INDEX: Word indexing started."
	index = {}
	articlecounts = {}
	inputpath = os.getcwd() + "/data/lemmatiser_output"

	doccount = 0
	totalwordcount = 0
	inputdata = {}

	for file in glob.glob(os.path.join(inputpath, '*.in')):
		print ">>INDEX: Unpickling: \t '%s'." %os.path.split(file)[1]
		pickledData = open(file, "r")
		tmp = pickle.load(pickledData)
		inputdata.update(tmp)
		pickledData.close()

	print ">>INDEX: Indexing %s articles." % len(inputdata)
	for doc in inputdata:
		doccount += 1
		wordcount = 0
		articleid = doc

		for line in inputdata[doc]:
			#print "line: %s" % line
			if len(line) < 1:
				continue

			for word in line:
				if len(word) < 1:
					continue
				wordcount += 1
				if word in index:
					if articleid in index[word][1]:
						index[word][1][articleid] += 1 
					else:
						index[word][1][articleid] = 1
				else:
					index[word] = [word, {articleid:1}]
				# print "articleid: %s" % index[word]
		totalwordcount += wordcount
		articlecounts[articleid] = wordcount

	print ">>INDEX: %s words in total." % totalwordcount
	print ">>INDEX: %s unique words indexed." % len(index)
	print ">>INDEX: Document average length is %s." % (totalwordcount / doccount)

	returndicts = [index, articlecounts]

	print ">>INDEX: Word indexing completed in %s seconds." % round((time.time() - starttime), 3)

	return returndicts
