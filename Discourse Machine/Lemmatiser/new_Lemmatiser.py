import subprocess
import os
import glob
import string
import time
import pickle



def lemmatise(input_content):
	
	input_file = "Lemmatiser/temp"
	
	with open(input_file, "wr") as fi:
		fi.write(input_content)
		
	#Set files and calls
	rtf_call = "Lemmatiser/CST_tools/rtfreader -T -E UTF8 -i " + input_file
	lem_call = "Lemmatiser/CST_tools/cstlemma -L -eU -l -p- -f Lemmatiser/CST_tools/flexrules -i " + input_file + ".segments"

	#Tokenise and lemmatize
	subprocess.call(rtf_call, shell=True)
	lem_dict = subprocess.check_output(lem_call, shell=True, stderr= subprocess.STDOUT)

	#Remove .segments file to save space
	os.remove(input_file + ".segments")

	#Clean the meta from the output
	output = []
	lem_dict = lem_dict.split("\n")
	for l in lem_dict[33:]:
		words = l.split("\t")
		if len(words) > 1:
			if words[1] is "." or words[1] not in string.punctuation and not words[1].isdigit():
				output.append(words[1])

	return output




def lemmatise_directory(dir_path):	
	all_files = glob.glob(dir_path + "/*.in")

	# Statistics
	print ">>LEMMATISE: Tokenising and lemmatising", len(all_files), "documents."
	starttime = time.time()

	for input_file in all_files:
		print ">>LEMMATISE: Grabbing file", input_file.split("/")[-1]
		with open(input_file, "r") as file:
			articles = pickle.load(file)
		
		for article in articles:
			art_content = articles[article]
			for i in range(1, len(art_content)):
				art_content[i] = lemmatise(art_content[i])
			articles[article] = art_content
		
		with open("data/lemmatiser_output/" + input_file.split("/")[-1], "w") as file:
			pickle.dump(articles, file)
		

	# Print final time stamp
	print ">>LEMMATISE: Lemmatising completed in", time.time() - starttime, "seconds"



def lemmatise_input_term(input_term):
	import subprocess
	import sys

	# Get input term
	# input_term = sys.argv[1]

	# Write input_term to file
	temp_file = "Lemmatiser/temp"
	file = open(temp_file, "w")
	file.write(input_term)
	file.close()

	# Call the lemmatiser program
	lem_call = "./Lemmatiser/CST_tools/cstlemma -L -eU -l -p- -f Lemmatiser/CST_tools/flexrules -i " + temp_file
	lem = subprocess.check_output(lem_call, shell=True, stderr=subprocess.STDOUT)

	# Extract the lemmatised term
	lem = lem.split("\n")
	lem = lem[33].split("\t")
	print ">>LEMMATISE: Lemmatising term", input_term, "as", lem[1]
	return lem[1]


