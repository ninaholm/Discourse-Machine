#!/usr/bin/python
# -*- coding: utf-8 -*-
from polyglot.text import Text
import os
import glob

basepath = os.getcwd() + "/data/"

paths = [name for name in os.listdir(basepath) if os.path.isdir(os.path.join(basepath, name))]



for path in paths:
	inputpath = basepath + path
	for filename in glob.glob(os.path.join(inputpath, '*.txt')):
		doc = open(filename, 'r')
		text = ""
		for line in doc:
			if len(line) < 2: 
				continue
			text += line

		POS = Text(text)
		doc.close()

		firstPOS = ["",""]
		secondPOS = ["",""]

		for w in POS.pos_tags:
			first = firstPOS[1]
			second = secondPOS[1]
			third = w[1]

			# print "first: %s" % first
			# print "second: %s" %second
			# print "third: %s" %third
			NOUNS = ["NOUN", "PNOUN"]

			#1 ADJ NOUN *
			# if first == "ADJ" and second in NOUNS:
			# 	print "ADJ NOUN * \t: %s %s" %(firstPOS[0], secondPOS[0])
			#2 ADV ADJ NOT-NOUN
			if first == "ADV" and second == "ADJ" and third not in NOUNS:
				print "ADV ADJ NOT-NOUN: %s %s %s" %(firstPOS[0], secondPOS[0], w[0])

			#3 ADJ ADJ NOT-NOUN
			if first == "ADJ" and second == "ADJ" and third not in NOUNS:
				print "ADJ ADJ NOT-NOUN: %s %s %s" %(firstPOS[0], secondPOS[0], w[0])
			#4 NOUN ADJ NOT-NOUN
			if first in NOUNS and second == "ADJ" and third not in NOUNS:
				print "NOUN ADJ NOT-NOUN: %s %s %s" %(firstPOS[0], secondPOS[0], w[0])
			#5 ADV VERB * 
			# if first == "ADV" and second == "VERB":
			# 	print "ADV VERB *: %s %s" %(firstPOS[0], secondPOS[0])

			firstPOS = secondPOS
			secondPOS = w


		# doc = open(filename[:-4] + "thirdGED.txt", "w")
		# for w in POS.pos_tags:
		# 	word = w[0].encode("utf-8")
		# 	third = w[1].encode("utf-8")
		# 	print third
		# 	if third == "PUNCT":
		# 		doc.write("%s " %(word))
		# 		continue
		# 	doc.write("%s[%s] " %(word, third))

			# print("{:<18}{}".format(word, third)+"\n")
		# doc.close()
		print "\n ---------------------------- \n"