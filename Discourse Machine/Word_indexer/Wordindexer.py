#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import glob
import operator
import pickle
import time

# Takes an array of inputfilenames, which is indexed into a dictionary with words as keys and [(articleid, count)] as values. 
# A dictionary of articles are also returned, with articleids as keys and totalwordcount as values.
# logdict[inputfile(s) + "-index"]: [Which file(s) has been indexed, # articles, # unique words, # average words/article, time to unpickle, time to index and time in total].

def index(inputfiles):
	starttime = time.time()
	print ">>INDEX: Word indexing started."
	index = {}
	articlecounts = {}
	inputpath = os.getcwd() + "/data/lemmatiser_output"

	doccount = 0
	totalwordcount = 0
	inputdata = {}

	pickleTime = time.time()
	for inputfilename in inputfiles:
		print ">>INDEX: Unpickling: \t '%s'." %inputfilename
		path = os.path.join(inputpath, inputfilename)
		pickledData = open(path, "r")
		tmp = pickle.load(pickledData)
		inputdata.update(tmp)
		pickledData.close()
	pickleTime = round((time.time() - pickleTime), 3)

	indexTime = time.time()
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
					if articleid in index[word]:
						index[word][articleid] += 1 
					else:
						index[word][articleid] = 1
				else:
					index[word] = {articleid:1}
				# print "articleid: %s" % index[word]
		totalwordcount += wordcount
		articlecounts[articleid] = wordcount
	indexTime = round((time.time() - indexTime), 3)

	print ">>INDEX: %s words in total." % totalwordcount
	print ">>INDEX: %s unique words indexed." % len(index)
	print ">>INDEX: Document average length is %s." % (totalwordcount / doccount)

	returndicts = [index, articlecounts]
	totalTime = round((time.time() - starttime), 3)

	print ">>INDEX: Word indexing completed in %s seconds." % totalTime
	log(inputfiles, len(inputdata), len(index), (totalwordcount / doccount), pickleTime, indexTime, totalTime)

	return returndicts

def log(inputfile, articleNum, uWordsNum, avgWord, pickleTime, indexTime, totalTime):
	path = os.getcwd() + "/log/tmplogarray.in"
	picklefile = open(path, 'rb')
	logarray = pickle.load(picklefile)
	picklefile.close()
	inputfilestring = ""
	for x in inputfile:
		inputfilestring += x + "_"

	data = [inputfilestring, articleNum, uWordsNum, avgWord, pickleTime, indexTime, totalTime]
	logarray.append(data)
	
	picklefile = open(path, 'wb')
	pickle.dump(logarray, picklefile)
	picklefile.close()



