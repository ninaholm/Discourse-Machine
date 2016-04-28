#!/usr/bin/python
# -*- coding: utf-8 -*-

# Walks through a given folder's subfolders and makes a pickled dictionary for each of the subfolders .txt files. 
# The dictionary = {articleid : [timestamp, headline, subheading, pictext, articlebody]}
# Pickle filename = foldername
# basepath = the folder, which contain the subfolders you want pickled.

import glob
import os
import sys
import time
import pickle

def pickleInput(self):
	starttime = time.time()
	print ">>PICKLE: Started pickling input."

	basepath = os.getcwd() + "/data/xmlparser_output/"

	paths = [name for name in os.listdir(basepath) if os.path.isdir(os.path.join(basepath, name))]

	print paths

	for path in paths:
		print(">>PICKLE: Pickling '%s'." % (path))
		inputpath = basepath + path

		dict = {}
		for filename in glob.glob(os.path.join(inputpath, '*.txt')):
			doc = open(filename, "r")
			count = 0
			doclist = ["","","","",""]
			body = False

			for lines in doc:
				arr = lines.split("\n")
				# print "count: %s" %count
				# print "len: %s" %len(arr[0])
				if count == 0:
					# print "headline: %s" % arr[0] 
					doclist[1] = arr[0]
					count += 1
					continue
				if count == 1:
					if len(arr[0]) <= 1:
						count +=1 
						continue
					# print "subheading: %s" % arr[0]
					doclist[2] = arr[0]
					count += 1
					continue
				if count > 1 and body == False:
					if len(arr[0]) <= 1:
						body = True 
						continue
					# print "pictext: %s" % arr[0]
					doclist[3] += arr[0]
				if count > 1 and body == True:
					# print "body: %s" % arr[0]
					doclist[4] += arr[0] 

			key = filename[filename.rfind("/")+1:filename.rfind(".txt")]

			count = 0
			timestamp = ""
			for letter in key:
				if letter.isdigit() and count < 6:
					timestamp += letter
					count += 1

			doclist[0] = timestamp[:4] + "/" + timestamp[4:]

			dict[key] = doclist

			# print "\n -------------------------------------------------------- \n"
			# print "0. timestamp: %s \n" %doclist[0]
			# print "1. heading: %s \n" %doclist[1]
			# print "2 subheading: %s \n" %doclist[2]
			# print "3 pictext: %s \n" %doclist[3]
			# print "4 article: %s \n" %doclist[4]
			# print "\n -------------------------------------------------------- \n"

		filename = path + ".in"
		links_pickle = open(basepath + filename, 'wb')
		pickle.dump(dict, links_pickle)
		links_pickle.close()
		print(">>PICKLE: '%s' is pickled (%s articles)." % (path, len(dict)))

	print 
	print ">>PICKLE: Pickling completed in %s seconds." % round((time.time() - starttime), 3)

pickleInput(0)