import csv

folder_prefix = "Topic_categoriser/"




def run_frequent_neighbours(index):
	neg_dict = []
	pos_dict = []
	with open(folder_prefix + "venstre_sentiment_dictionary.csv", "r") as file:
		content = csv.reader(file, delimiter=",")
		for row in content:
			if int(row[1]) < 0:
				neg_dict.append(row[0])
			else if int(row[1]) > 0:
				pos_dict.append(row[1])
	
	test = neg_dict
#	test = [for w in neg_dict]
	print neg_dict
	print "boom!"
	




