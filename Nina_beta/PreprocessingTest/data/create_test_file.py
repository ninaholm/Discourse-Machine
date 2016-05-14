import pickle
import random

big_file = "../lemmatiser_output/indland.in"
sample_size = 100

with open(big_file) as file:
	data = pickle.load(file)

random_keys = random.sample(data, sample_size)

output = {}
for key in random_keys:
	output[key] = data[key]

# Save sample
output_file_name = "test" + big_file.replace("/", "_").replace("..", "")
with open(output_file_name, "w") as file:
	pass
	pickle.dump(output, file)

