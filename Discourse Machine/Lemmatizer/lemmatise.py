#apt-get install python-pip
#pip install subprocess
import subprocess

input_file = "test_data.txt"
rtf_call = "rtfreader -T -i " + input_file
lem_call = "./CST\ tools/cstlemma/src/cstlemma -L -f flexrules -i " + input_file + '.segments'

subprocess.call(rtf_call, shell=True)
lem_dict = subprocess.check_output(lem_call, shell=True)
print lem_dict


for line in lem_dict:
    pass #This is where we construct the finished, lemmatized file from the CST output. TO BE DONE.

