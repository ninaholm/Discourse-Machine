# XML -> .RTF parser for the RCV2_Multilingual_Corpus. Only parsing headline, byline and text.

import glob
import os

path = os.getcwd() + '/input'

for filename in glob.glob(os.path.join(path, '*.xml')):
	doc = open(filename, "r")

	docname = filename[filename.rfind("/")+1:filename.rfind(".xml")]
	txt = open(os.getcwd() + '/output/' + docname + ".rtf", 'w')
	txt.write("{\\rtf1\\ansi\\deff0" + "\n")

	for line in doc:
		if len(line) < 1:
			continue

		if line.startswith("<headline>"):
			endIndex = line.find("</headline>")
			txt.write(line[10:endIndex].strip() + "\\line \n")

		if line.startswith("<byline>"):
			endIndex = line.find("</byline>")
			txt.write(line[8:endIndex].strip() + "\\line \n")

		if line.startswith("<p>"):
			endIndex = line.find("</p>")
			txt.write(line[3:endIndex].strip()  + "\\line \n")

	txt.write("}")
	doc.close()
