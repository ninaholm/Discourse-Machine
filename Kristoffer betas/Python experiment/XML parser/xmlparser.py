# XML -> .RTF parser for the RCV2_Multilingual_Corpus. Only parsing headline, byline and text.

import glob
import os

path = os.path.dirname(os.path.abspath(__file__)) + '/input'

for filename in glob.glob(os.path.join(path, '*.xml')):
	doc = open(filename, "r")

	docname = filename[filename.rfind("/")+1:filename.rfind(".xml")]
	txt = open(os.path.dirname(os.path.abspath(__file__)) + '/output/' + docname + ".txt", 'w')

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
