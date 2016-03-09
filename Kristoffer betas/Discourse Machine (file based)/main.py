from XML_parser.XMLparser import parse
from TFIDF_indexer.TFIDFindexer import index
from TFIDF_searcher.TFIDFsearcher import search
import time

starttime = time.time()
parse(0)
print 
index(0)
print
search(0)
print
print "Total time elapsed: %s seconds" % round((time.time() - starttime), 3)