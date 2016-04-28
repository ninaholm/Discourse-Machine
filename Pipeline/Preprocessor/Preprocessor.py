import subprocess
import os
import glob
import string
import time
import pickle



class Preprocessor():

	def __init__(self):
		self.tools_path = ""
		self.input_file = "Lemmatiser/temp"
		self.tokenized_input_file = self.input_file + ".segments"
		self.split_word = "OUOUOUOFFLFL".lower() # used to write several strings to one file
		self.log = _Logger()
		self.output_path = ""


	def lemmatise_directory(self, dir_path):
		lem = Lemmatiser(); lem.run(dir_path)

	def postag_directory(self, dir_path):
		ptag = POStagger(); ptag.run()


	def _tokenize(self):
		rtf_call = "Lemmatiser/CST_tools/rtfreader -T -E UTF8 -i " + self.input_file
		subprocess.call(rtf_call, shell=True)


	def _write_to_file(self, input_content_list):
		with open(self.input_file, "w") as fi:
			for item in input_content_list:
				fi.write(item)
				fi.write("\n" + self.split_word + "\n")

	def _split_up_output(self, first_item, input_content_string):
		output_list = []
		output_list.append(first_item)
		for thing in input_content_string.split(self.split_word)[1:]:
			output_list.append(thing[2:])
		return output_list


	def _parse_directory(self, function_to_call, dir_path):
		all_files = glob.glob(dir_path + "/*.in")

		# Statistics
		print ">>PREPROCESS: Processing", len(all_files), "corpora."

		# load corpora
		for input_file in all_files:
			input_filename = input_file.split("/")[-1]

			self.log.new_corpus()
			print ">>PREPROCESS: Unpickling file", input_filename
			with open(input_file, "r") as file:
				articles = pickle.load(file)
			self.log.unpickling_time = time.time() - self.log.corpus_starttime

			print ">>PREPROCESS: Corpus contains", len(articles), "articles"

			for article in articles:
				date = articles[article][0]
				self._write_to_file(articles[article])
				t = time.time() # Grab timestamp
				self._tokenize()
				self.log.time_counter[0].append(time.time() - t) # Add timestamp to log
				t = time.time() # Grab timestamp
				temp = function_to_call()
				self.log.time_counter[1].append(time.time() - t) # Add timestamp to log
				articles[article] = self._split_up_output(date, temp)

			with open(self.output_path + input_filename, "w") as file:
				pickle.dump(articles, file)

			self.log.save_stats(input_filename, len(articles)) # save statistics to log



class POStagger(Preprocessor):
	def __init__(self):
		self.tools_path = "Lemmatiser/CST_tools/postagger/Bin_and_Data/"

	def _postagged_splitword(self):
		return string.replace("\n" + self.split_word + "/NNP", self.split_word)

	def _postag(self):
		pos_call = "./TOOLS_PATH/tagger TOOLS_PATH/FINAL.LEXICON " + self.tokenized_input_file + " TOOLS_PATH/BIGBIGRAMLIST TOOLS_PATH/LEXRULEOUTFILE TOOLS_PATH/CONTEXT-RULEFILE -S"
		pos_call = pos_call.replace("TOOLS_PATH/", self.tools_path) # Insert correct tools_path

		pos_dict = subprocess.check_output(pos_call, shell=True)
		return pos_dict

	def run(self):
		print ">>PREPROCESS: Starting POS-tagging..."
		self.log.start()
		self._parse_directory(self._postag, dir_path)
		self.log.save_elapsed_time()
		print ">>PREPROCESS: Preprocessing completed in", str(log.elapsed_time), "seconds"




class Lemmatiser(Preprocessor):
	def __init(self):
		self.tools_path = "Lemmatiser/CST_tools/"
		self.output_path = "data/lemmatiser_output/"


	def run(self, dir_path):
		print ">>PREPROCESS: Starting lemmatising..."
		self.log.start()
		self._parse_directory(self._lemmatise, dir_path)
		self.log.save_elapsed_time()
		print ">>PREPROCESS: Preprocessing completed in", str(log.elapsed_time), "seconds"


	def lemmatise_input_term(self, input_term):
		# Write input_term to file
		with open(self.input_file, "w") as file:
			file.write(input_term)
	
		# Call the lemmatiser program
		lem_call = "./Lemmatiser/CST_tools/cstlemma -L -eU -l -p- -f Lemmatiser/CST_tools/flexrules -i " + self.input_file
		lem = subprocess.check_output(lem_call, shell=True, stderr=subprocess.STDOUT)

		# Extract the lemmatised term
		lem = lem.split("\n")
		lem = lem[33].split("\t")
		print ">>PREPROCESS: Lemmatising term", input_term, "as", lem[1]
		return lem[1]


	def _lemmatise(self):
		lem_call = "Lemmatiser/CST_tools/cstlemma -L -eU -l -p- -f Lemmatiser/CST_tools/flexrules -i " + self.tokenized_input_file
		lem_dict = subprocess.check_output(lem_call, shell=True, stderr= subprocess.STDOUT).split("\n")

		#Clean the meta from the output
		output = []
		for l in lem_dict[33:]:
			words = l.split("\t")
			if len(words) > 1:
				if words[1] is "." or (words[1] not in string.punctuation and not words[1].isdigit()):
					output.append(words[1])

		output = " ".join(output)
		return output





class _Logger():

	def __init__(self):
		starttime = None

	def start(self):
		self.starttime = time.time()

	def new_corpus(self):
		self.corpus_starttime = time.time()
		self.time_counter = []
		for i in range(3):
			self.time_counter.append([])

	def save_stats(self, corpus_name, len_articles):
		with open("log/preprocess_log", "a") as file:
			file.write("CORPUS: \t\t" + corpus_name + "\n")
			file.write("Number of articles: \t" + str(len_articles) + "\n")
			file.write("Unpickling data: \t" + str(self.unpickling_time) + "\n")
			file.write("Tokenizing: \t\t" + str(sum(self.time_counter[0])) + " seconds\n")
			file.write("POS-tagging: \t\t" + str(sum(self.time_counter[1])) + " seconds\n")
			file.write("Lemmatising: \t\t" + str(sum(self.time_counter[2])) + " seconds\n")
			file.write("Elapsed for corpus: \t" +  str(time.time() - self.corpus_starttime))
			file.write("\n - - - - - - - - - - - - - \n")
		
	def save_elapsed_time(self):
		self.elapsed_time = time.time() - log.starttime
		with open("log/preprocess_log", "a") as file:
			file.write("Total elapsed time: \t" +  str(time.time() - self.starttime))
			file.write("\n\n ################################################### \n\n")
