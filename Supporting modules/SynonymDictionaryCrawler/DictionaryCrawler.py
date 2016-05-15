import urllib
from bs4 import BeautifulSoup
import re
import heapq
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


base_url1 = "http://www.synonymordbog.dk/index.php?q="
base_url2 = "&menu=menu_search&title_menu=S%F8gning"
words_to_grab = []
words_searched = []

# Grab contents of webpage
def parse_webpage(url):
	html_doc = urllib.urlopen(url, 'ISO-8859-1').read()
	soup = BeautifulSoup(html_doc, "html.parser")
	return soup

# grab contents of the Synonymer div
def get_synonyms(doc_soup, base_word):

	syn_soup = doc_soup.find_all('div', attrs={'class': 'pages_page'})
	
	# Ensure that we only grab the list of direct synonyms (where the list header == the word we're looking for)
	for i in range(len(syn_soup)):
		header = syn_soup[i].find('div', attrs={'class': 'tekst_14F2'}).getText()
		if str(header).lower() == str(base_word + " "):
			syn_list = syn_soup[i].find('div', attrs={'class': 'pages_page_description'})
			syns = str(syn_list).lower().replace("<div class=\"pages_page_description\">", "").replace("</div>", "").replace("</br>", "").split("<br>")
	
			return syns
	else:
		return None
	
	
# Encodes word to url-friendly format
def urlify(word):
	return word.decode("utf-8").encode("ISO-8859-1","ignore")


def run(start_term):
	
	print ">>DICTIONARY_CRAWLER: Crawling for term", start_term
	
	website = parse_webpage(base_url1 + urlify(start_term) + base_url2)
	synonyms = get_synonyms(website, start_term)
	if synonyms is not None:
		for syn in synonyms:
			heapq.heappush(words_to_grab, syn)
	
	words_searched.append(start_term)
	
#	sys.exit()

	counter = 0
	
	while words_to_grab:
		print "************* Next iteration ***************"
		next_word = heapq.heappop(words_to_grab)
		print "Now searching......", next_word
		heapq.heappush(words_searched, next_word)
		next_website = base_url1 + urlify(next_word) + base_url2
		website = parse_webpage(next_website)
		
		synonyms = get_synonyms(website, next_word)
		print synonyms
		
		if synonyms is not None:
			for syn in synonyms:
				if syn not in words_searched and syn not in words_to_grab:
					heapq.heappush(words_to_grab, syn)
		
		# Determine the number of iterations
		counter = counter +1
		if counter == 10:
			break

def save_synonyms(words):
	">>DICTIONARY_CRAWLER: Saving synonyms to file"
	with open("dictionary_crawler_results.txt", "w") as file:
		for word in words:
			file.write(word + "\n")

			
			
print ">>DICTIONARY_CRAWLER: Starting the crawl"


def get_synonyms_of_dictionary():
	all_synonyms = []
	terms = []
	import csv
	with open("../Pipeline/data/sentiment_dictionaries/venstre_sentiment_dictionary.csv", "r") as file:
		content = csv.reader(file, delimiter=",")
		for row in content:
			if int(row[1]) is not 0:
				terms.append(row[0])

	for term in terms:
		run(term)
		for word in words_to_grab:
			all_synonyms.append(word)
		words_to_grab = []

	save_synonyms(all_synonyms + words_searched)

def get_synonyms():
	terms = ["god", ]
	terms = ["dårlig", "svindel", "beklage"]




