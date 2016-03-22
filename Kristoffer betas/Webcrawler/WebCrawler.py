#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
import re
import sys
import os
import random
import string
import pickle
import time
from time import gmtime, strftime


linkquarantine = ["?page=", "#kommentarer"]
categories = ["indland", "udland", "mofo", "nyhedsblog", "kultur", "emne", "debat"]
cutoffsentences = ["Du skal være registreret bruger for at kommentere. Log ind eller opret bruger", "Der er ingen kommentarer endnu", "/ritzau/", "Allerede abonnent? Log ind her", "/ritzau/Reuters", "/ritzau/AFP", "/ritzau/NDB"]

class WebCrawler():
    def __init__(self, url, links_to_search, links_searched):
        self.base_url = url
        self.links_to_search = links_to_search
        self.links_searched = links_searched


    def get_links(self, doc_soup):
        # print ">>> get_links to search: %s" %len(self.links_to_search)
        # print ">>> Links searched: %s" %len(self.links_searched)
        for item in doc_soup.findAll('a'):
            if "href=\"/" in str(item):
                link = re.search('href="(.*?)"', str(item))
                link = link.group(1)

                if link not in self.links_searched or link not in self.links_to_search:
                    if any(l in link for l in categories) and not any(l in link for l in linkquarantine): # check to avoid links conaining no_go strings
                        self.links_to_search[link] = True


    def parse_webpage(self, url):
        html_doc = urllib.urlopen(url, 'utf-8').read()
        soup = BeautifulSoup
        s = BeautifulSoup(html_doc)
        return s

    def clean_text(self, soup):
        site = soup.findAll('div')
        empty = [""] * 4
        article = ""
        empty[0] = soup.title.string[:-14]

        for div in site: # Iterates over all div-tages, looking for the article's body
            if 'class="field field-name-field-underrubrik"' in str(div) or 'class="field field-name-field-ritzau-subheader"' in str(div):
                empty[1] = div.getText()
            if 'class="field field-name-field-description"' in str(div):
                empty[2] = div.getText()
            if 'class="field field-name-body"' in str(div):
                article = div.getText() # Overwrites, since we only need the last one found, since the div tags are recursive.

        for line in article.split('\n'):
            # print line
            if any(l in line for l in cutoffsentences):
                break
            empty.append(line)

        return empty


    def cap(self, s, l):
        return s if len(s)<= l else s[0:l]

    def remove_punctuation(self, word, length):
        return self.cap(''.join([i for i in word if i not in string.punctuation]), length)

    def write_doc(self, text, foldername, url):
        for category in categories:
            if category in url:
                subfolder = category
        filename = "output/" + self.remove_punctuation(foldername, 20) + "/" + subfolder + "/" + self.remove_punctuation(url, 20) + ".txt"
        # filename = "output/" + self.remove_punctuation(foldername, 20) + "/" + self.remove_punctuation(url, 20) + ".txt"
        doc = open(filename, "w")
        for line in text:
            # print "line: %s" %line 
            doc.write(line + "\n")
        doc.close()

    def saveLinks(self, links_searched, links_to_search):
        print ">>> PICKLING LINKS"
        links_pickle = open('links_searched.in', 'wb')
        pickle.dump(links_searched, links_pickle)
        links_pickle.close()

        links_pickle = open('links_to_search.in', 'wb')
        pickle.dump(links_to_search, links_pickle)
        links_pickle.close()

    def stats(self):
        stats = []
        totalcount = 0
        for category in categories:
            DIR = os.getcwd() + '/output/httpinformationdk/' + str(category) + "/"
            count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
            totalcount += count
            stats.append((category,count))

        print "\n>>> Totalcount: \t %s \n" % totalcount
        for count in stats:
            if count[1] == 0:
                continue
            percentage = round(((float(count[1]) / totalcount) * 100),1)
            if count[0] == "nyhedsblog":
                print ">>> %s: \t %s (%s%%)" % (count[0], count[1], percentage)
            else:
                print ">>> %s: \t\t %s (%s%%)" % (count[0], count[1], percentage)
        print "\n>>> Links to search: \t %s" %len(self.links_to_search)
        print ">>> Links searched: \t %s" %len(self.links_searched)
        print strftime("\n>>> %H:%M:%S %d-%m-%Y")
        print ">>> Time elapsed: %s seconds.\n" % (time.time() - starttime)


    def run(self):
        # Find links on first run
        self.get_links(self.parse_webpage(self.base_url))
        repeatcheck = []
        repeatcount = 0
        savecount = len(self.links_searched) + 500

        # Calculate and save the word count in the document
        while self.links_to_search:
            # print ">>> Links searched: %s" %len(self.links_searched)

            if len(self.links_searched) % 20 == 0:
                self.stats()

            if len(self.links_searched) >= savecount:
                self.saveLinks(self.links_searched, self.links_to_search)
                savecount += 500


            url = random.choice(self.links_to_search.keys())
            del self.links_to_search[url]

            # url = self.links_to_search.pop() # get next url in line
            print url
            self.links_searched[url] = True # save url as already searched
            soup = self.parse_webpage(self.base_url + url) # get webpage
            self.get_links(soup) # harvest urls to search
            if url.startswith("/emne/"): # 'emne' are frontpages, good for trawling for links, but not content.
                del self.links_searched[url]
                print "emne hit"
                continue

            clean = self.clean_text(soup) # clean webpage content

            if clean == repeatcheck: # Check if we receive the same content +5 times in a row (crawling warning fx.)
                print "repeat"
                repeatcount += 1
                if repeatcount > 5:
                    self.saveLinks(self.links_searched, self.links_to_search)
                    break
            else:
                repeatcount = 0
            repeatcheck = clean

            self.write_doc(clean, self.base_url, url)
            if len(self.links_searched) == 50000:  # Caps the result at X pages, for test purposes
                self.saveLinks(self.links_searched, self.links_to_search)
                break

reload(sys)
sys.setdefaultencoding('utf8')

urls = ["http://information.dk"]

links_TS = {}
links_S = {}

starttime = time.time()

if os.path.isfile("links_searched.in"):         # Check if there already is a crawl saved.
    linkfile = open("links_to_search.in", 'rb')
    links_TS = pickle.load(linkfile)
    linkfile.close()

    linkfile = open("links_searched.in", 'rb')
    links_S = pickle.load(linkfile)
    linkfile.close()

for url in urls:
    print "Now crawling", url
    wc = WebCrawler(url, links_TS, links_S)
    wc.run()

print "Total time elapsed: %s seconds." % (time.time() - starttime)

