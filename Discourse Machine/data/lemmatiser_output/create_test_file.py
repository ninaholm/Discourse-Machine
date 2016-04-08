import pickle
import random

with open("indland.in") as file:
	data = pickle.load(file)

random_keys = random.sample(data, 100)

output = {}
for key in random_keys:
	output[key] = data[key]


with open("test_indland.in", "w") as file:
	pickle.dump(output, file)

