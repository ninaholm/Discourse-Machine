#apt-get install python-pip

#pip install subprocess

import subprocess

import os



#Set files and calls

input_file = "data/test_file.txt"

rtf_call = "rtfreader -T -i " + input_file

lem_call = "./cstlemma/src/cstlemma -L -f flexrules -i " + input_file + ".segments"



#Tokenize and lemmatize

subprocess.call(rtf_call, shell=True)

lem_dict = subprocess.check_output(lem_call, shell=True)



#Remove .segments file to save space

os.remove(input_file + ".segments")



#Save the lemmatized result in its own file

file_fin = open(input_file + ".fin", "w")

line = lem_dict.split("\n")

for l in line:

	words = l.split("\t")

	if len(words) > 1:

		file_fin.write(words[1] + " ")



file_fin.close()

