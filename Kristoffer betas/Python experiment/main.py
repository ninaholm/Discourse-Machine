import os

path = os.getcwd()

xmlpath = path + "/XML parser/xmlparser.py"

xmlpath = xmlpath.replace(" ", "*")

print "running: %s" % xmlpath
os.system("python " + xmlpath)

tfidfpath = (path + "/TF-IDF indexer/tediffern.py").replace(" ", "*")

print "running: %s" % tfidfpath
os.system("python " + tfidfpath)