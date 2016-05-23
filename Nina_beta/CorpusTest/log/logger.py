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

def makeLog(totalTime):
	logarray = unpickle(0)
	corpora = []
	sentimentheader = ["TERM"]
	sentimentdict = {}
	timeheader = []
	timecontent = [[]]

	log = open(os.getcwd() + "/log/log.txt", 'a')

	for x in logarray:
		if x[0].endswith(".in_"):
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
		corpusheader = ["TERM", "# ARTICLES", "SUBSET/SENTENCE/PARSE", "B.O.W. (article/sentence)", "SENTENCES", "PARSESCORE"]
		corpuscontent = []
		for data in corpus: 
			if data[0].endswith(".in_"):
				corpusmetadata = "Corpus:\t\t\t\t\t\t %s \nArticles:\t\t\t\t\t %s\nUnique words:\t\t\t\t %s\nAvg. word/article:\t\t\t %s\nPickle time:\t\t\t\t %s s\nIndex time:\t\t\t\t\t %s s\n" %(data[0], data[1], data[2], data[3], data[4], data[5])
				articleNum = data[1]
				sentimentheader.append(data[0])
				timeheader.append(data[0])
				timecontent[0].append(data[6])
				continue
			term = data[0]

			data[3] = "%s (%s) / %s" %(round((data[3] / float(data[1])),3),data[3], data[6])

			score = data[5]

			# data[1] = str(data[1])
 			data[2] = str(data[2])
			corpuscontent.append(data[0:9])

			if term in sentimentdict:
				sentimentdict[term].append(score)
			else:
				sentimentdict[term] = [score]

		sentimentdict = padSentimentTable(sentimentdict, corporaCount)
		# corpuscontent.sort(key=itemgetter(0))
		totalSentenceCount = 0
		totalParsedCount = 0
		itCount = 0
		parseAvg = 0
		subsetTime = 0
		sentenceTime = 0
		parseTime = 0

		for x in corpuscontent:
			itCount += 1
			parseAvg += x[5]
			subsetTime += float(x[2])
			sentenceTime += x[7]
			parseTime += x[8]
			x[2] = "%s / %s / %s s" %(x[2],x[7],x[8])
			del x[8], x[7], x[6]
			num = x[4]
			totalParsedCount += int(num[num.find("(")+1:num.rfind("/")])
			totalSentenceCount += int(num[num.find("/")+1:num.rfind(")")])
			
		
		sentenceAvg = round((totalParsedCount/float(totalSentenceCount))*100,2)
		parseAvg = round(parseAvg/float(itCount),3)
		corpusmetadata += "Search (subset) time: \t\t %s s\nSearch (sentence) time: \t %s s\nParse time: \t\t\t\t %s s\nAvg. sentence success: \t\t %s%%\nAvg. parse score: \t\t\t %s\n\n" %(subsetTime, sentenceTime, parseTime, sentenceAvg, parseAvg)


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

	for rows in timecontent:
		avg = 0
		count = 0
		for value in rows:
			avg += value
			count += 1
		avg = avg / count
		rows.append(avg)
	timeheader.append("Average")
	
	log.write("~" * 90 + "\n\n")
	log.write("OVERALL TIME TABLE \n")
	log.write(table(timeheader, timecontent) + "\n\n")

	for scores in sentimentcontent:
		empty = True
		avg = 0
		count = 0
		for x in scores: 
			if type(x) != float:
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
			avg = float(avg / count)
			scores.append(avg)
	sentimentheader.append("Average")
	print sentimentcontent
	sentimentcontent = sorted(sentimentcontent, key=lambda result: sentimentcontent[0][1], reverse=True)

	sentimenttable = table(sentimentheader, sentimentcontent)

	log.write("+" * 90 + "\n\n")
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
		if type(term) == float:
			continue
		term = unicode(term, 'utf-8')
		rows[0] = term

	return tabulate(content, headers=header,tablefmt='orgtbl')

def getMainMeta(corpora, totalTime):
	corpusNum = len(corpora)

	# Should be recoded to not be hardcoded to the global dict!!!
	dictsize = 0
	dictionary = open(os.getcwd() + "/data/sentiment_dictionaries/information_manual_sent.csv", 'r')
	for lol in dictionary:
		dictsize += 1

	timedate = strftime("%H:%M:%S %d-%m-%Y")

	mainMeta = "\n\nTime:\t\t %s \nCorpora:\t %s \nDict. size:\t %s \nTime elapsed:\t %s s\n\n" %(timedate, corpusNum, dictsize, totalTime)
	return mainMeta

def createLog(self):
	path = os.getcwd() + "/log/tmplogarray.in"
	logarray = []
	picklefile = open(path, 'wb')
	pickle.dump(logarray, picklefile)
	picklefile.close()

def fillUnfound(sentimentdict, corporaCount):
	searchterms = open(os.getcwd() + "/data/searchterms.txt")
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
	searchterms = open(os.getcwd() + "/data/searchterms.txt")
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
			logMessage(0)
			return True
		else:
			print "Wrong input. Try again."

def logMessage(self):
	print "Enter logmessage: "
	userinput = raw_input()
	log = open(os.getcwd() + "/log/log.txt", 'a')
	log.write("\n")
	log.write("#" * 50)
	log.write("\n\nLogmessage: " + userinput)
	log.close()


def indexLog(inputfile, articleNum, uWordsNum, avgWord, pickleTime, indexTime, totalTime):
	path = os.getcwd() + "/log/tmplogarray.in"
	picklefile = open(path, 'rb')
	logarray = pickle.load(picklefile)
	picklefile.close()
	inputfilestring = ""
	for x in inputfile:
		inputfilestring += x + "_"

	data = [inputfilestring, articleNum, uWordsNum, avgWord, pickleTime, indexTime, totalTime]
	logarray.append(data)
	
	picklefile = open(path, 'wb')
	pickle.dump(logarray, picklefile)
	picklefile.close()

def searchLog(term, articleNum, totalTime):
	path = os.getcwd() + "/log/tmplogarray.in"
	picklefile = open(path, 'rb')
	logarray = pickle.load(picklefile)
	picklefile.close()

	data = [term, articleNum, totalTime]
	logarray.append(data)

	picklefile = open(path, 'wb')
	pickle.dump(logarray, picklefile)
	picklefile.close()

def sentimentArticleLog(term, sentiment):
	path = os.getcwd() + "/log/tmplogarray.in"
	picklefile = open(path, 'rb')
	logarray = pickle.load(picklefile)
	picklefile.close()

	if logarray[len(logarray)-1][0] == term:
		logarray[len(logarray)-1].append(sentiment)

	picklefile = open(path, 'wb')
	pickle.dump(logarray, picklefile)
	picklefile.close()

def sentimentSentenceLog(term, sentences, sentimentscore, bowscore, inputfile, sentenceTime, parseTime):
	path = os.getcwd() + "/log/tmplogarray.in"
	picklefile = open(path, 'rb')
	logarray = pickle.load(picklefile)
	picklefile.close()

	inputfilestring = ""
	for x in inputfile:
		inputfilestring += x + "_"

	foundCorpus = False

	for x in range(len(logarray)):
		
		if logarray[x][0] == inputfilestring:
			# print "if %s == %s" %(logarray[x][0],inputfilestring)
			foundCorpus = True
			continue
		if foundCorpus:
			# print "term if %s == %s" %(logarray[x][0],term)
			if logarray[x][0] == term:
				logarray[x].append(sentences)
				logarray[x].append(sentimentscore)
				logarray[x].append(bowscore)
				logarray[x].append(sentenceTime)
				logarray[x].append(parseTime)
				break

	picklefile = open(path, 'wb')
	pickle.dump(logarray, picklefile)
	picklefile.close()

