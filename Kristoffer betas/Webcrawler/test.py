import pickle
import os

links_TS = {}
links_S = {}

if os.path.isfile("links_searched.in"):         # Check if there already is a crawl saved.
	print "lol"
	linkfile = open("links_to_search.in", 'rb')
	links_TS = pickle.load(linkfile)
	linkfile.close()

	linkfile = open("links_searched.in", 'rb')
	links_S = pickle.load(linkfile)
	linkfile.close()

print len(links_S)
print len(links_TS)

links = {}

for x in links_TS:
	if not x.startswith("/telegram/"):
		links[x] = True

print len(links)

print len(links_S)

# links_pickle = open('links_TS.in', 'wb')
# pickle.dump(links_S, links_pickle)
# links_pickle.close()

links_pickle = open('links_S.in', 'wb')
pickle.dump(links, links_pickle)
links_pickle.close()