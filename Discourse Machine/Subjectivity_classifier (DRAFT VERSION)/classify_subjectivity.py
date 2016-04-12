import glob
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


all_data = []

def get_data():
	data_folder = "../data/lemmatiser_output/"
	data_folder = "../data/xmlparser_output/"
	file_list = glob.glob(data_folder + "*.txt")

	for f in file_list:
		with open(f, "r") as fi:
			global all_data
			all_data.append(fi.read().split("."))

def is_subjective(sentence):
	sentence = sentence.split(" ")
	for word in sentence:
		if word in subj_dict:
			return True
	
def get_subj_dict(filename):
	subj_dict = {}
	with open(filename, "r") as fi:
		for word in fi.readlines():
			subj_dict[word.replace("\n", "")] = True
	return subj_dict

def print_stats():
	print ">>SUBJ_CLASSIFIER: Extracting sentences from", len(all_data), "articles"
	print ">>SUBJ_CLASSIFIER: Number of subjective words are", len(subj_dict)
	
	
	
print "getting data"
get_data()
print "getting dicts"
subj_dict = dict(get_subj_dict("positive_dict.txt"), **get_subj_dict("negative_dict.txt"))


print_stats()

subj_list = []
for art in all_data:
	for line in art:
		if is_subjective(line):
			subj_list.append(line)

with open("subjective_lines.txt", "w") as fi:
	for line in subj_list:
		fi.write(line + "\n")







