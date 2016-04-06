import glob
import csv
import sys



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
	sentiment_score = 0
	for word in dictionary:
		if word in WORDindex:
			for article in WORDindex[word]:
				if article in article_list:
					sentiment_score = sentiment_score + int(dictionary[word]) * int(WORDindex[word][article])

	return sentiment_score


def run_sentiment_classifier(article_list, WORDindex):
	reload(sys)
	sys.setdefaultencoding('utf-8')

	dict_path = "Sentiment_classifier/sentiment_dictionaries/universal_dictionary.csv"
	
	print ">>SENTIMENT: Sentiment analysis started."
	print ">>SENTIMENT: Reading universal sentiment dictionary."
	dictionary = read_dictionary(dict_path)

	print ">>SENTIMENT: Calculating sentiment score for %s articles" % len(article_list)
	sentiment_score = calculate_sentiment_score(dictionary, article_list, WORDindex)
	
	print ">>SENTIMENT: This subset's aggregated sentiment value is", sentiment_score
	




