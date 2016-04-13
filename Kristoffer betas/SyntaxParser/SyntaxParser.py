import pickle
import os
from tabulate import *

def CKYparse(words, grammar):
	table = [["-" for x in range(len(words))] for x in range(len(words))] 
	header = []
	for word in words:
		tmp = word[:word.rfind("/")]
		tmp = unicode(tmp, 'utf-8')
		header.append(tmp)
	count = 0
	for j in range(len(words)):
		word = unicode(words[j], 'utf-8')
		tag = word[word.rfind("/")+1:]
		word = word[:word.rfind("/")]
		table[j][j] = tag
		for i in range(j):
			i = abs(i-j)-1
			print "i: [%s][%s]" %(i, j)
			T1 = table[i][j-1]
			print "T1: %s" %T1
			T2 = table[i+1][j]
			print "T2: %s" %T2
			count += 1
			table[i][j] = count
		print " ----------------------- "


	print tabulate(table, headers=header)


def unpickle(self):
	path = os.getcwd() + "/input/original_test_indland.in"
	picklefile = open(path, 'rb')
	articles = pickle.load(picklefile)
	picklefile.close()

	return articles

def getSentences(article):
	sentenceList = []
	for entry in article[1:]:
		# Split into sentences
		entry = entry.split("./TEGN")

		for sentences in entry:
			if len(sentences) < 3: 
				continue
			sentence = []
			words = sentences.split(" ")

			for word in words:
				if word[:1] == "\n":
					word = word[1:]
				if len(word) < 1: 
					continue
				sentence.append(word)
				# print "word: %s" %repr(word)
			sentenceList.append(sentence)
	return sentenceList



articles = unpickle(0)

for article in articles:
	sentences = getSentences(articles[article])
	for sentence in sentences:
		CKYparse(sentence, "lol")
		break
	break

# for lol in articles:
# 	sentences = articles[lol]
# 	test = sentences[4]
# 	test = test.split("./TEGN")
# 	print type(test)
# 	for y in test:
# 		print y
# 		print
# 	break