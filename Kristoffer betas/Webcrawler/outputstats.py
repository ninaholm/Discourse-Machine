import os
import re
import operator


a_dir = os.getcwd() + "/output/httpinformationdk/"

paths = [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]

docs = {}
years = {}
doccount = 0

for path in paths:
	folder = a_dir + path
	for filename in os.listdir(folder):
		doccount += 1
		name = ""
		year = ""
		month = ""
		timecount  = 0
		for letter in filename:
			if letter.isdigit():
				if timecount >= 4:
					month += str(letter)
				if timecount < 4:
					year += str(letter)
				if timecount > 5:
					break
				timecount += 1
			if name == "mofo":
				break
			if timecount == 0:
				name += letter
			if timecount > 5:
				break
		# print "name: %s, %s/%s" % (name, month, year)
		if name in docs:
			docs[name] += 1
		else:
			docs[name] = 1

		if year in years:
			years[year] += 1
		else:
			years[year] = 1

print ">>> # of documents: \t %s" % doccount 
print ">>> # of categories: \t %s \n" % len(docs)

sorted_docs = sorted(docs.items(), key=operator.itemgetter(1), reverse=True)
sorted_years = sorted(years.items(), key=operator.itemgetter(0), reverse=True)

for x in sorted_docs:
	category = x[0]
	catcount = docs[category]

	if catcount == 0:
		continue
	else:
		percentage = round(((float(catcount) / doccount) * 100),1)

	if len(category) >= 9:
		print ">>> %s: \t %s (%s%%)" % (category, catcount, percentage)
	else:
		print ">>> %s: \t\t %s (%s%%)" % (category, catcount, percentage)