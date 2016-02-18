#apt-get install python-pip

#pip install subprocess

import subprocess

import os


all_files = os.listdir("data")

for file in all_files:

	#Set files and calls
	input_file = "data/" + file

	rtf_call = "CST_tools/rtfreader -T -i " + input_file

	lem_call = "./CST_tools/cstlemma/src/cstlemma -L -f CST_tools/flexrules -i " + input_file + ".segments"


	#Tokenize and lemmatize

	subprocess.call(rtf_call, shell=True)

	lem_dict = subprocess.check_output(lem_call, shell=True)



	#Remove .segments file to save space

	os.remove(input_file + ".segments")



	#Save the lemmatized result in its own file
	output_file = "data/output/" + file + ".lem"

	file_fin = open(output_file, "w")

	line = lem_dict.split("\n")

	for l in line:

		words = l.split("\t")

		if len(words) > 1:

			file_fin.write(words[1] + " ")

	file_fin.close()




