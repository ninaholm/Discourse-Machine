# XML -> .RTF parser for the RCV2_Multilingual_Corpus. Only parsing headline, byline and text.

import glob
import os
import sys
import time

def parse(self):
	starttime = time.time()
	print ">>PARSE: Started parsing."

	outputpath = os.getcwd() + "/data/xmlparser_output/"

	count = 0

	inputpath = os.getcwd() + "/data/original_data"

	for filename in glob.glob(os.path.join(inputpath, '*.xml')):
		count += 1

		sys.stdout.write(">>PARSE: %s documents. \r" % (count) )
		sys.stdout.flush()

		doc = open(filename, "r")

		docname = filename[filename.rfind("/")+1:filename.rfind(".xml")]
		txt = open(outputpath + docname + ".txt", 'w')

		for line in doc:
			if len(line) < 1:
				continue

			if line.startswith("<headline>"):
				endIndex = line.find("</headline>")
				txt.write(line[10:endIndex].strip() + "\n")

			if line.startswith("<byline>"):
				endIndex = line.find("</byline>")
				txt.write(line[8:endIndex].strip() + "\n")

			if line.startswith("<p>"):
				endIndex = line.find("</p>")
				txt.write(line[3:endIndex].strip()  + "\n")

		doc.close()	
	print 
	print ">>PARSE: Parsing completed in %s seconds." % round((time.time() - starttime), 3)
