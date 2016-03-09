from XML_parser.XMLparser import parse
from TFIDF_indexer.TFIDFindexer import index
from TFIDF_searcher.TFIDFsearcher import search
import time

starttime = time.time()
parsedCorpus = parse(0)
print

indexes = index(parsedCorpus)
TFIDFindex = indexes[0]
ARTICLEindex = indexes[1]
print

search(TFIDFindex, ARTICLEindex)
print

print "Total time elapsed: %s seconds" % round((time.time() - starttime), 3)