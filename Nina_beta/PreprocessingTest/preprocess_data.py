#from XML_parser.XMLparser import parse
from Preprocessor.Preprocessor import Preprocessor
import time

data_path = "data/test"


pre = Preprocessor()

pre.create_monster_corpus(data_path)
print

# pre.lemmatise_directory(data_path)
# print






