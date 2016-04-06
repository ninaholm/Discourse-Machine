import glob
import csv



#Reading in dictionaries
def read_dictionary(dict_path):
	with open(dict_path, "r") as csvfile:
		dictionary = {}
		with open(dict_path, "r") as csvfile:
			csv_dict = csv.reader(csvfile)
			for row in csv_dict:
				dictionary[row[0].decode('utf-8')] = row[1]
	return dictionary


def calculate_sentiment_score(dictionary, article_list, WORDindex):
	topic_score = 0
	for word in dictionary:
		for article in WORDindex[word]:
			if article in article_list:
				topic_score = topic_score + dictionary[word]
		
	return topic_score


def run_sentiment_classifier(article_list, WORDindex):

	dict_path = "Sentiment_classifier/sentiment_dictionaries/universal_dictionary.csv"
	dict_path = "../Discourse Machine/Sentiment_classifier/sentiment_dictionaries/universal_dictionary.csv"
	
	print ">>SENTIMENT: Reading universal sentiment dictionary."
	dictionary = read_dictionary(dict_path)

	print ">>SENTIMENT: Calculating sentiment score for %s articles" % len(article_list)
	topic_score = calculate_sentiment_score(dictionary, article_list, WORDindex)
	
	print ">>SENTIMENT: This subset's aggregated sentiment value is", score
	

run_sentiment_classifier(["fish", "bob"], {})



