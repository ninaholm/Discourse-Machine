

def save_random_article():
	print ">>TEST: Unpickling data file"
	start_time = time.time()
	with open("../Discourse Machine/data/lemmatiser_output/udland.in") as file:
		data = pickle.load(file)
	print ">>TEST: Unpickled in", time.time() - start_time, "seconds"

	random_article = random.choice(data.keys())
	print ">>TEST: Working on article:", random_article

	with open("rand_article", "w") as file:
		pickle.dump(data[random_article], file)


# Set default coding to uft-8
reload(sys)
sys.setdefaultencoding('utf-8')


def load_data():
	print ">>TEST: Unpickling data file"
	with open("rand_article") as file:
		data = pickle.load(file)

	print ">>TEST: Stringing the article together"
	string = " ".join(data[4])
	string = re.sub('\|.*? ', ' ', string) # resolve lemma ambiguity by taking the first option
	string = string.decode('utf-8')
	text = Text(string)

	return text

	sentences = string.split(".") # Break up article into sentences
	sentence = sentences[3] # Extract test sentence

