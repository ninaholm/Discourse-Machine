import os

path = os.getcwd()

# XML parser initialized and run
xmlpath = path + "/XML parser/xmlparser.py"

xmlpath = xmlpath.replace(" ", "*")

os.system("python " + xmlpath)

# Add new subfolder and scripts