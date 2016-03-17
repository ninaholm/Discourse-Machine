import glob

neg_dict = []
pos_dict = []
global topic_list; topic_list = {}

#Reading in dictionaries
def read_dictionaries(pos_dict_path, neg_dict_path):
	with open(pos_dict_path, "r") as file:
		global pos_dict; pos_dict = file.read().splitlines()
	with open(neg_dict_path, "r") as file:
		global neg_dict; neg_dict = file.read().splitlines()

def calculate_topic_score(article_list):
	for filename in article_list:
		topic_score = 0
		with open(filename, "r") as article:
			article = article.read()
			for word in neg_dict:
				if word in article:
					topic_score = topic_score - 1
			for word in pos_dict:
				if word in article:
					topic_score = topic_score + 1
		topic_list[filename] = topic_score

#print topic_list
def print_topics():
	score = 0
	for key in topic_list:
		score = score + topic_list[key]
	print ">>SENTIMENT: This subset's aggregated sentiment value is", score
	

def run_topic_categoriser(article_list):
	##set test variables
	#data_folder = "data/lemmatiser_output/"
	#article_list = glob.glob(data_folder + "*.txt")
	
	pos_path = "Topic_categoriser/positive_dict.txt"
	neg_path = "Topic_categoriser/negative_dict.txt"
	
	print ">>SENTIMENT: Reading positive/negative dictionaries."
	read_dictionaries(pos_path, neg_path)
	print ">>SENTIMENT: Calculating sentiment score for", len(article_list), "articles"
	calculate_topic_score(article_list)
	print_topics()
	

#run_topic_categoriser()


