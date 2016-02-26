import os

path = os.getcwd()

xmlpath = path + "/XML parser/xmlparser.py"

xmlpath = xmlpath.replace(" ", "*")

print "running: %s \n" % xmlpath
os.system("python " + xmlpath)

tfidfindexerpath = (path + "/TF-IDF indexer/tediffern.py").replace(" ", "*")
print "running: %s \n" % tfidfindexerpath
os.system("python " + tfidfindexerpath)

tfidfsearchpath = (path + "/TF-IDF searcher/search.py").replace(" ", "*")
print "running: %s \n" % tfidfsearchpath
os.system("python " + tfidfsearchpath)
