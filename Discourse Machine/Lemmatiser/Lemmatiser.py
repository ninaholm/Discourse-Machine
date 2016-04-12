import subprocess
import os
import glob
import string
import time
import pickle

tools_path = "Lemmatiser/CST_tools/"
input_file = "Lemmatiser/temp"
tokenized_input_file = input_file + ".segments"
split_word = "OUOUOUOFFLFL".lower()


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

	output = " ".join(output)
	return output


def tokenize():
	global input_file
	rtf_call = "Lemmatiser/CST_tools/rtfreader -T -E UTF8 -i " + input_file
	subprocess.call(rtf_call, shell=True)


def write_to_file(input_content_list):
	global input_file
	with open(input_file, "w") as fi:
		for item in input_content_list:
			fi.write(item)
			fi.write("\n" + split_word + "\n")

def split_up_output(first_item, input_content_string):
	output_list = []
	output_list.append(first_item)
	input_content_string = input_content_string.replace("\n" + split_word + "/NNP", split_word)
	for thing in input_content_string.split(split_word)[1:]:
		output_list.append(thing[2:])
	return output_list

def postag():
	global tokenized_input_file
	pos_tools_path = tools_path + "postagger/Bin_and_Data/"
	pos_call = "./TOOLS_PATH/tagger TOOLS_PATH/FINAL.LEXICON " + tokenized_input_file + " TOOLS_PATH/BIGBIGRAMLIST TOOLS_PATH/LEXRULEOUTFILE TOOLS_PATH/CONTEXT-RULEFILE -S"
	pos_call = pos_call.replace("TOOLS_PATH/", pos_tools_path) # Insert correct tools_path

	pos_dict = subprocess.check_output(pos_call, shell=True)
	return pos_dict


def parse_directory(function_to_call, dir_path):
	all_files = glob.glob(dir_path + "/*.in")

	# Statistics
	if function_to_call == "pos":
		print ">>LEMMATISE: Tokenising and pos-tagging", len(all_files), "corpora."
	elif function_to_call == "lem":
		print ">>LEMMATISE: Tokenising and lemmatising", len(all_files), "corpora."
	starttime = time.time()

	for input_file in all_files:
		print ">>LEMMATISE: Unpickling file", input_file.split("/")[-1]
		with open(input_file, "r") as file:
			articles = pickle.load(file)
		
		print ">>LEMMATISE: Corpus contains", len(articles), "articles"
		for article in articles:
			date = articles[article][0]
			write_to_file(articles[article])
			tokenize()
			if function_to_call == "pos":
				temp = postag()
			elif function_to_call == "lem":
				temp = lemmatise()
			articles[article] = split_up_output(date, temp)

		if function_to_call == "pos":
			output_path = "data/postagger_output/"
		elif function_to_call == "lem":
			output_path = "data/lemmatiser_output/"

		with open(output_path + input_file.split("/")[-1], "w") as file:
			pickle.dump(articles, file)

	# Print final time stamp
	print ">>LEMMATISE: Preprocessing completed in", time.time() - starttime, "seconds"


def postag_directory(dir_path):
	print ">>LEMMATISE: Starting POS-tagging..."
	parse_directory("pos", dir_path)

def lemmatise_directory(dir_path):	
	print ">>LEMMATISE: Starting lemmatising..."
	parse_directory("lem", dir_path)





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

