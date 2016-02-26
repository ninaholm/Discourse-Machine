import os
import glob
import operator


index = {}
articlecounts = {}
inputpath = os.getcwd() + "/XML parser/output"
print "tfidf inputpath: %s" % inputpath

doccount = 0

for file in glob.glob(os.path.join(inputpath, '*.txt')):
	doc = open(file, "r")
	doccount += 1
	wordcount = 0
	articleid = os.path.split(file)[1]

	for line in doc:
		#print "line: %s" % line
		line = line.lower().strip()

		if len(line) < 2:
			continue

		line = line.split(" ")

		for word in line:
			if len(word) < 1:
				continue
			wordcount += 1
			word = word.translate(None, "!@#$,.'")
			word = word.translate(None, '<[]():^%">?*/_+')

			if hash(word) in index:
				if articleid in index[hash(word)][1]:
					index[hash(word)][1][articleid] += 1 
				else:
					index[hash(word)][1][articleid] = 1
		
			else:
				index[hash(word)] = [word, {articleid:1}]
			#print "articleid: %s" % index[hash(word)]

	articlecounts[articleid] = wordcount

sorted_index = sorted(index.items(), key=operator.itemgetter(0))

countdb = open(os.path.dirname(os.path.abspath(__file__)) + '/inverted_index.txt', 'w')

for entries in sorted_index:
	articles = ""
	for x in entries[1][1]:
		articles += "[%s:%s] " % (x, entries[1][1][x])
	hashid = str(entries[0])
	data = "%s : %s \n" % (hashid, articles)
	countdb.write(data)

countdb.close()

articledb = open(os.path.dirname(os.path.abspath(__file__)) + '/articlecounts.txt', 'w')

for articleid in articlecounts:
	count = articlecounts[articleid]
	articledb.write("%s : %s \n" % (articleid, count))

articledb.close()

print "doccount: %s" % doccount

