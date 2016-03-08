# XML -> .RTF parser for the RCV2_Multilingual_Corpus. Only parsing headline, byline and text.

import glob
import os
import sys
import time

def parse(self):
	starttime = time.time()
	print ">>PARSE: Started parsing."

	count = 0

	path = os.path.dirname(os.path.abspath(__file__)) + '/input'

	parsedCorpus = {}

	for filename in glob.glob(os.path.join(path, '*.xml')):
		count += 1

		sys.stdout.write(">>PARSE: %s documents. \r" % (count) )
		sys.stdout.flush()

		doc = open(filename, "r")

		articlestring = ""

		for line in doc:
			if len(line) < 1:
				continue

			if line.startswith("<headline>"):
				endIndex = line.find("</headline>")
				# txt.write(line[10:endIndex].strip() + "\n")
				articlestring += line[10:endIndex].strip() + " "

			if line.startswith("<byline>"):
				endIndex = line.find("</byline>")
				# txt.write(line[8:endIndex].strip() + "\n")
				articlestring += line[8:endIndex].strip() + " "

			if line.startswith("<p>"):
				endIndex = line.find("</p>")
				# txt.write(line[3:endIndex].strip()  + "\n")
				articlestring += line[3:endIndex].strip() + " "

		parsedCorpus[filename] = articlestring
		doc.close()	
	print 
	print ">>PARSE: Parsing completed in %s seconds." % round((time.time() - starttime), 3)

	return parsedCorpus
