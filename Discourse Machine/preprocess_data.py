#from XML_parser.XMLparser import parse
from Lemmatiser.Preprocessor import Preprocessor, Lemmatiser
from log.logger import log, createLog, logChoice
import time

data_path = "data/original_data/information"


pre = Preprocessor()

pre.lemmatise_directory(data_path)
print

#postag_directory(data_path)
#print





