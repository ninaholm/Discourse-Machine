# -*- coding: utf-8 -*-

from log.logger import makeLog, createLog, logChoice
from Corpus.corpus import *
from SyntacticParser.SyntacticParser import SyntacticParser
import time
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

sentence = "Jeg var en glad studerende i går"

print sentence
parser = SyntacticParser()
parser.parse_sentence(sentence)

