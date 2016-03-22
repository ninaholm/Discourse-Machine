import os
import shutil
import sys
from glob import glob

a_dir = os.getcwd() + "/output/httpinformationdk/"
paths = [name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))]

userinput = raw_input("Are you sure you want to delete everything in output-folder? Y/N \n")

if userinput != "Y":
	sys.exit() 

print "Deleting..."

for path in paths:
	folder = os.getcwd() + "/output/httpinformationdk/" + path
	for the_file in os.listdir(folder):
	    file_path = os.path.join(folder, the_file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
	    except Exception, e:
	        print e