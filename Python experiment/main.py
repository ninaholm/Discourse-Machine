import os

path = os.getcwd()

xmlpath = path + "/XML parser/xmlparser.py"

xmlpath = xmlpath.replace(" ", "*")

os.system("python " + xmlpath)