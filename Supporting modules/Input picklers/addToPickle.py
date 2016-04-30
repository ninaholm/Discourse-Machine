#!/usr/bin/python
# -*- coding: utf-8 -*-

# This scripts needs to be placed in a folder with the existing pickled dicitionary (<filename>.in) and the .txts files of articles need to be added!
# It unpickles the dictionary, add all the new .txts files and repickles the dictionary.

import glob
import os
import sys
import time
import pickle

starttime = time.time()
print ">>ADD TO PICKLE: Started adding new data to pickle."

basepath = os.getcwd()
picklefilename = ""

for filename in os.listdir(basepath):
	if filename.endswith(".in"):
		picklefilename = filename

pickledict = open(picklefilename, 'rb')
olddict = pickle.load(pickledict)
pickledict.close()

print ">>ADD TO PICKLE: Existing pickled dict (%s) has %s articles." %(picklefilename, len(olddict))

newdict = {}
for filename in glob.glob(os.path.join(os.getcwd(), '*.txt')):
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

	newdict[key] = doclist

	# print "\n -------------------------------------------------------- \n"
	# print "0. timestamp: %s \n" %doclist[0]
	# print "1. heading: %s \n" %doclist[1]
	# print "2 subheading: %s \n" %doclist[2]
	# print "3 pictext: %s \n" %doclist[3]
	# print "4 article: %s \n" %doclist[4]
	# print "\n -------------------------------------------------------- \n"

print ">>ADD TO PICKLE: %s new articles to be added." % len(newdict)

olddict.update(newdict)

links_pickle = open("new" + picklefilename, 'wb')
pickle.dump(olddict, links_pickle)
links_pickle.close()
print(">>ADD TO PICKLE: The updated dictionary has been saved to '%s' with %s articles in total." % ("new" + picklefilename, len(olddict)))

# print 
# print ">>PICKLE: Pickling completed in %s seconds." % round((time.time() - starttime), 3)
