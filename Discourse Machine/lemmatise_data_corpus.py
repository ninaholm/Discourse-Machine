

class Lemmatiser:

	def __init__(self):
		import subprocess
		import os
		import glob

	def lemmatise_directory(self, dir_path):
		all_files = glob.glob(dir_path + "/*.txt")

		for input_file in all_files:
			#Set files and calls
			rtf_call = "CST_tools/rtfreader -T -E UTF8 -i " + input_file
			lem_call = "./CST_tools/cstlemma -L -f CST_tools/flexrules -i " + input_file + ".segments"

			#Tokenize and lemmatize
			subprocess.call(rtf_call, shell=True)
			lem_dict = subprocess.check_output(lem_call, shell=True)

			#Remove .segments file to save space
			os.remove(input_file + ".segments")

			output_file = input_file.replace("data/", "")

			#Save the lemmatized result in its own file
			output_file = "../data/lemmatiser_output/" + output_file + ".lem"
			file_fin = open(output_file, "w")
			line = lem_dict.split("\n")
			for l in line:
				words = l.split("\t")
				if len(words) > 1:
					file_fin.write(words[1] + " ")
			file_fin.close()

			
	def lemmatise_inpurt_term(self, input_term):
		import subprocess
		import sys

		# Get input term
		# input_term = sys.argv[1]

		# Write input_term to file
		temp_file = "temp"
		file = open(temp_file, "w")
		file.write(input_term)
		file.close()

		# Call the lemmatiser program
		lem_call = "./CST_tools/cstlemma -L -f CST_tools/flexrules -i " + temp_file
		lem = subprocess.check_output(lem_call, shell=True)

		# Extract the lemmatised term
		lem = lem.split("\n")
		lem = lem[2].split("\t")
		print "The input term was: \t\t" + input_term
		print "The lemmatised word is: \t" + lem[1]
		return lem[1]


	