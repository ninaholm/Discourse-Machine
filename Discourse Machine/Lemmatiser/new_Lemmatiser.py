import subprocess
import os
import glob
import string
import time
import pickle

tools_path = "Lemmatiser/CST_tools/"
input_file = "Lemmatiser/temp"
tokenized_input_file = input_file + ".segments"


def lemmatise():
	global tokenized_input_file
	lem_call = "Lemmatiser/CST_tools/cstlemma -L -eU -l -p- -f Lemmatiser/CST_tools/flexrules -i " + tokenized_input_file
	lem_dict = subprocess.check_output(lem_call, shell=True, stderr= subprocess.STDOUT)

	#Clean the meta from the output
	output = []
	lem_dict = lem_dict.split("\n")
	for l in lem_dict[33:]:
		words = l.split("\t")
		if len(words) > 1:
			if words[1] is "." or words[1] not in string.punctuation and not words[1].isdigit():
				output.append(words[1])

	return output

def write_to_file(input_content):
	global input_file
	with open(input_file, "wr") as fi:
		fi.write(input_content)

def tokenize():
	global input_file
	rtf_call = "Lemmatiser/CST_tools/rtfreader -T -E UTF8 -i " + input_file
	subprocess.call(rtf_call, shell=True)


def postag():
	global tokenized_input_file
	pos_tools_path = tools_path + "postagger/Bin_and_Data/"
	pos_call = "./TOOLS_PATH/tagger TOOLS_PATH/FINAL.LEXICON " + tokenized_input_file + " TOOLS_PATH/BIGBIGRAMLIST TOOLS_PATH/LEXRULEOUTFILE TOOLS_PATH/CONTEXT-RULEFILE -S"
	pos_call = pos_call.replace("TOOLS_PATH/", pos_tools_path) # Insert correct tools_path

	pos_dict = subprocess.check_output(pos_call, shell=True)
	return pos_dict

def postag_directory(dir_path):
	all_files = glob.glob(dir_path + "/*.in")

	# Statistics
	print ">>LEMMATISE: Tokenising and pos-tagging", len(all_files), "corpora."
	starttime = time.time()

	for input_file in all_files:
		print ">>LEMMATISE: Unpickling file", input_file.split("/")[-1]
		with open(input_file, "r") as file:
			articles = pickle.load(file)
		
		print ">>LEMMATISE: Corpus contains", len(articles), "articles"
		for article in articles:
			art_content = articles[article]
			for i in range(1, len(art_content)):
				write_to_file(art_content[i]); tokenize()
				art_content[i] = postag()
			articles[article] = art_content
			print articles[article]
			raw_input("press enter")
			
		
		with open("data/lemmatiser_output/" + input_file.split("/")[-1], "w") as file:
			pickle.dump(articles, file)


def lemmatise_directory(dir_path):	
	all_files = glob.glob(dir_path + "/*.in")

	# Statistics
	print ">>LEMMATISE: Tokenising and lemmatising", len(all_files), "corpora."
	starttime = time.time()

	for input_file in all_files:
		print ">>LEMMATISE: Unpickling file", input_file.split("/")[-1]
		with open(input_file, "r") as file:
			articles = pickle.load(file)
		
		print ">>LEMMATISE: Corpus contains", len(articles), "articles"
		for article in articles:
			art_content = articles[article]
			for i in range(1, len(art_content)):
				write_to_file(art_content[i]); tokenize()
				art_content[i] = lemmatise()
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

