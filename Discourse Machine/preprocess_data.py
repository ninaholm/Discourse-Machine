#from XML_parser.XMLparser import parse
from Lemmatiser.Lemmatiser import lemmatise_directory, lemmatise_input_term, postag_directory
from log.logger import log, createLog, logChoice
import time

data_path = "data/original_data/information"

#lemmatise_directory(data_path)
#print

postag_directory(data_path)
print





