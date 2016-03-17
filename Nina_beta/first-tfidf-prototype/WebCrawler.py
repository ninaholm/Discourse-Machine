import urllib
import BeautifulSoup
import re
import heapq
from Document import *
import sys


no_go = ["kommentar", "ibyen", "comment", "byliv", "bilnyheder", "biltests"]

class WebCrawler():
    def __init__(self, url):
        self.base_url = url
        self.links_to_search = []
        self.links_searched = []

    def get_links(self, doc_soup):
        for item in doc_soup.findAll('a'):
            if "href=\"/" in str(item):
                link = re.search('href="(.*?)"', str(item))
                link = link.group(1)
                if link not in self.links_searched and link not in self.links_to_search:
                    if not any(l in link for l in no_go): # check to avoid links conaining no_go strings
                        heapq.heappush(self.links_to_search, link)

    def parse_webpage(self, url):
        html_doc = urllib.urlopen(url, 'utf-8').read()
        soup = BeautifulSoup
        s = soup.BeautifulSoup(html_doc)
        return s

    def clean_text(self, soup):
        content = soup.findAll('p')
        empty = []
        for i in content:
            empty.append(i.getText())
        return empty

    def run(self):
        # Find links on first run
        self.get_links(self.parse_webpage(self.base_url))

        # Calculate and save the word count in the document
        while self.links_to_search:
            url = heapq.heappop(self.links_to_search) # get next url in line
            heapq.heappush(self.links_searched, url) # save url as already searched
            soup = self.parse_webpage(self.base_url + url) # get webpage
            self.get_links(soup) # harvest urls to search
            clean = self.clean_text(soup) # clean webpage content
            doc = Document(url)
            doc.count_words(clean) # count number of words on webpage
            doc.save_word_count(self.base_url) # save document
            if len(self.links_searched) == 10000:  # Caps the result at X pages, for test purposes
                break


reload(sys)
sys.setdefaultencoding('utf8')

urls = ["http://information.dk"]

for url in urls:
    print "Now crawling", url
    wc = WebCrawler(url)
    wc.run()


