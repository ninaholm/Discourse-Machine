from Sentiment_classifier.sentiment_classifier import run_sentiment_classifier
from log.logger import makeLog, createLog, logChoice
from Corpus.corpus import *
import time
import os
import sys
from SyntacticParser.SyntacticParser import SyntacticParser

sentence = "Jeg er en glad studerende"

parser = SyntacticParser()
parser.parse_sentence(sentence)

