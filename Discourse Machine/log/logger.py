#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf8
import os
import time
from time import gmtime, strftime
import pickle
from tabulate import *
from operator import itemgetter
import sys

def log(totalTime):
	logarray = unpickle(0)
	corpora = []
	sentimentheader = ["TERM"]
	sentimentdict = {}
	lenlimit = len(logarray[0])

	log = open(os.getcwd() + "/log/log.txt", 'a')

	for x in logarray:
		if len(x) == lenlimit:
			corpora.append([x])
			continue
		corpora[len(corpora)-1].append(x)

	mainMeta = getMainMeta(corpora, totalTime)
	log.write(mainMeta)
	corporaCount = 0

	for corpus in corpora:
		corporaCount += 1
		corpusmetadata = ""
		articleNum = 0
		corpusheader = ["TERM", "# ARTICLES", "SEARCH", "SENTIMENT", "SCORE"]
		corpuscontent = []
		for data in corpus: 
			if len(data) == lenlimit:
				corpusmetadata = "Corpus:\t\t\t %s \nArticles:\t\t %s\nUnique words:\t\t %s\nAvg. word/article:\t %s\nPickle time:\t\t %s s\nIndex time:\t\t %s s\nTotal time:\t\t %s s\n\n" %(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
				articleNum = data[1]
				sentimentheader.append(data[0])
				continue
			term = data[0]
			score = data[4]

			# data[1] = str(data[1])
 			data[2] = str(data[2]) + " s"
			data[3] = str(data[3]) + " s"
			corpuscontent.append(data[0:5])

			if term in sentimentdict:
				sentimentdict[term].append(score)
			else:
				sentimentdict[term] = [score]
		sentimentdict = padSentimentTable(sentimentdict, corporaCount)
		corpuscontent.sort(key=itemgetter(0))
		timetable = table(corpusheader, corpuscontent)
		log.write("-" * 75 + "\n")
		log.write(corpusmetadata)
		log.write(timetable + "\n\n")

	sentimentcontent = []

	for key in sentimentdict:
		arr = [key]
		for score in sentimentdict[key]:
			arr.append(score)
		sentimentcontent.append(arr)

	# print sentimentcontent

	for scores in sentimentcontent:
		empty = True
		avg = 0
		count = 0
		for x in scores: 
			if type(x) != int:
				continue
			if x == 0:
				empty = False
			empty = False
			count += 1
			avg += x
		if empty == True:
			scores.append("-")
		if avg == 0:
			scores.append("0")
		else:
			avg = int(avg / count)
			scores.append(avg)
	sentimentheader.append("Average")
	sentimentcontent = sorted(sentimentcontent, key=lambda result: sentimentcontent[1], reverse=True)

	sentimenttable = table(sentimentheader, sentimentcontent)

	log.write("+" * 75 + "\n\n")
	log.write("OVERALL SENTIMENT TABLE \n")
	log.write(sentimenttable + "\n\n")

	log.close()

def unpickle(self):
	path = os.getcwd() + "/log/tmplogarray.in"
	picklefile = open(path, 'rb')
	logarray = pickle.load(picklefile)
	picklefile.close()

	return logarray

def table(header, content):
	for rows in content:
		term = rows[0]
		term = unicode(term, 'utf-8')
		rows[0] = term

	return tabulate(content, headers=header,tablefmt='orgtbl')

def getMainMeta(corpora, totalTime):
	corpusNum = len(corpora)

	divider = "#" * 100

	# Should be recoded to not be hardcoded to the global dict!!!
	dictsize = 0
	dictionary = open(os.getcwd() + "/Sentiment_classifier/sentiment_dictionaries/universal_dictionary.csv", 'r')
	for lol in dictionary:
		dictsize += 1

	timedate = strftime("%H:%M:%S %d-%m-%Y")

	mainMeta = "\n%s\n\nTime:\t\t %s \nCorpora:\t %s \nDict. size:\t %s \nTime elapsed:\t %s s\n\n" %(divider, timedate, corpusNum, dictsize, totalTime)
	return mainMeta

def createLog(self):
	path = os.getcwd() + "/log/tmplogarray.in"
	logarray = []
	picklefile = open(path, 'wb')
	pickle.dump(logarray, picklefile)
	picklefile.close()

def fillUnfound(sentimentdict, corporaCount):
	searchterms = open(os.getcwd() + "/TFIDF_searcher/searchterms.txt")
	terms = []
	for term in searchterms:
		terms.append(term.strip())

	for term in terms:
		if term not in sentimentdict:
			sentimentdict[term] = []
			for x in range(corporaCount):
				sentimentdict[term].append("-")
	return sentimentdict

def padSentimentTable(sentimentdict, corporaCount):
	searchterms = open(os.getcwd() + "/TFIDF_searcher/searchterms.txt")
	terms = []
	for term in searchterms:
		term = term.strip()

		if term not in sentimentdict:
			sentimentdict[term] = []

		if len(sentimentdict[term]) != corporaCount:
			sentimentdict[term].append("-")

	return sentimentdict

def logChoice(self):

	while True:
		sys.stdout.write('\r' + "\r>> ENTER = \tNO LOG.\n>> ANY KEY = \tLOG.\n>> Enter choice..." + ' ' * 1)
		sys.stdout.flush() # important
		userinput = raw_input()

		if userinput == "":
			# sys.stdout.flush() # important
			print ">> Logging has been disabled\n"
			return False
		elif userinput != "":
			# sys.stdout.flush() # important
			print "\r>> Logging has been enabled.\n"
			return True
		else:
			print "Wrong input. Try again."




