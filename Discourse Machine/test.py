
import pickle




d = {3:"Fish", 45:"Neeat"}

with open("temp", "w") as file:
	pickle.dump(d, file)

with open("temp", "r") as file:
	t = pickle.load(file)
	print t
	for key in t:
		print key
