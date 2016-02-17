import os

print("xml print test")

path = os.path.dirname(__file__)

test = open(path + "/test1.txt", 'w')

test.close()