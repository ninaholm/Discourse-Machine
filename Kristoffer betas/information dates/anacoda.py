import glob
import os
import pickle
import matplotlib.pyplot as plt
import csv

all_files = glob.glob(os.getcwd() + "/data/monster_output/*.in")

articles = {}
dates = {}

for name in all_files:
	with open(name, "r") as inputfile:
		print "Unpickling:",name
		articles.update(pickle.load(inputfile))

	break
	
print len(articles)

for article in articles:
	date = articles[article][0]
	date = date[:date.rfind("/")] + date[date.find("/")+1:] 
	if len(date) < 3:
		continue
	date = int(date)
	if date < 198000:
		print date
		continue
	if date not in dates:
		dates[date] = 1
	else:
		dates[date] += 1

print len(dates)

with open("dates.csv", "w") as csv:
	for x in dates:
		w = "%s,%s\n"%(x,dates[x])
		csv.write(w)



# plt.bar(dates.keys(), dates.values())
# plt.show()