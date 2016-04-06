import csv

dict_path = "../Discourse Machine/Sentiment_classifier/sentiment_dictionaries/universal_dictionary.csv"

dictionary = {}

with open(dict_path, "r") as csvfile:
		csv_dict = csv.reader(csvfile)
		for row in csv_dict:
			global dictionary; dictionary[row[0]] = row[1]

print dictionary