from multiprocessing import *
import random
import time

def doStuff(x):
	x.sort()

	for y in range(1000):
		x[y] = random.uniform(0,1000)
		
	x.sort()

	return len(x)

arr = []

for lol in range(100):
	tmp = []
	for y in range(1000):
		tmp.append(random.uniform(0,lol))
	arr.append(tmp)

print len(arr[0])
print len(arr)
for x in range(len(arr)):
	# print "arr x: ",len(arr[x])
	for y in range(9):
		arr[x] += arr[x]
	# print "arr x: ",len(arr[x])
print len(arr[0])
print len(arr)

# cpus = multiprocessing.cpu_count()
result = []

# print "CPU count: ", cpus
print "RUNNING"
starttime = time.time()

# for rofl in arr:
# 	result.append(doStuff(rofl))
p = Pool(4)
result += (p.map(doStuff,arr))


totalTime = round((time.time()-starttime),3)

print "total time: ", totalTime, " s"
print "avg time: ",float(totalTime) / 1000," s"
print len(result)
# # print result