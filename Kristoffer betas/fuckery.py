import csv

fil = open("universal_dictionary.csv", 'r')
count = 0
tagcount = 0
annontated = []
positive = []
negative = []

for line in fil:
	if ',+1' in line or ',1' in line:
		positive.append(line)
	if ',-1' in line:
		negative.append(line)
		

	tagcount += 1
fil.close()

positive.sort()
negative.sort()
annontated += positive
annontated += negative

# finished = open("information_manual_sent.csv", "w")

# for x in annontated:
# 	word = x[:x.find(",")]
# 	score = x[x.find(",")+1:x.rfind("1")+1].translate(None, "+")
# 	finished.write("%s,%s\n"%(word, score))


print "total: ", len(annontated)
print "negative: ", len(negative)
print "positive: ", len(positive)