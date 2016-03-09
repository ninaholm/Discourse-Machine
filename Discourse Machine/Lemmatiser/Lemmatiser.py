

class Lemmatiser:

	def __init__(self):
		pass
	
	def lemmatise_directory(self, dir_path):
		import subprocess
		import os
		import glob
		import string
		import time
		all_files = glob.glob(dir_path + "/*.txt")

		# Statistics and shit
		print ">>LEMMATISE: Tokenising and lemmatising", len(all_files), "documents."
		starttime = time.time()
		
		for input_file in all_files:
			#Set files and calls
			rtf_call = "Lemmatiser/CST_tools/rtfreader -T -E UTF8 -i " + input_file
			lem_call = "Lemmatiser/CST_tools/cstlemma -L -eU -l -p- -f Lemmatiser/CST_tools/flexrules -i " + input_file + ".segments"
			
			#Tokenise and lemmatize
			subprocess.call(rtf_call, shell=True)
			lem_dict = subprocess.check_output(lem_call, shell=True, stderr= subprocess.STDOUT)
			
			#Remove .segments file to save space
			os.remove(input_file + ".segments")

			output_file = input_file.replace(dir_path, "")

			#Save the lemmatized result in its own file
			output_file = "data/lemmatiser_output/" + output_file + ".lem"
			file_fin = open(output_file, "w")
			line = lem_dict.split("\n")
			for l in line[33:]:
				words = l.split("\t")
				if len(words) > 1:
					if words[1] not in string.punctuation and not words[1].isdigit():
						file_fin.write(words[1] + " ")
			file_fin.close()
		
		# Print final time stamp
		print ">>LEMMATISE: Lemmatising completed in", time.time() - starttime, "seconds"

			
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


	