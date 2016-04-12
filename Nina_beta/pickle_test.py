import csv
import pickle
import time
import random



def load_data(filename):
	with open(filename) as file:
		data = pickle.load(file)
	return data


def pickle_dump_data(data):
	times = []
	for i in range(1,100):
		starttime = time.time()
		with open("temp", "w") as file:
			pickle.dump(data, file)
		times.append(time.time() - starttime)

	return sum(times) / len(times)

def pickle_load_data(filename):
	times = []
	for i in range(1,100):
		starttime = time.time()
		with open(filename) as file:
			data = pickle.load(file)
		for article in data:
			for i in range(1,4):
				data[article][i] = data[article][i].split(" ")
		times.append(time.time() - starttime)
	return sum(times) / len(times)
	

original_filename = "original_test_indland.in"
data = load_data(original_filename)

# random_keys = random.sample(data, 50)
# data = { key:value for key,value in data.items() if key in random_keys }
print ">>TEST:", len(data), "articles"


print ">>TEST: Articles are strings."
with open("temp", "w") as file:
	pickle.dump(data, file)
average_load = pickle_load_data("temp")
average_dump = pickle_dump_data(data)
print ">>TEST: The average pickle load took", average_load, "seconds"
print ">>TEST: The average pickle dump took", average_dump, "seconds"


print ">>TEST: Articles are lists."
for article in data:
	data[article][4] = data[article][4].split(" ")
with open("temp", "w") as file:
	pickle.dump(data, file)
average_load = pickle_load_data("temp")
average_dump = pickle_dump_data(data)
print ">>TEST: The average pickle load took", average_load, "seconds"
print ">>TEST: The average pickle dump took", average_dump, "seconds"









