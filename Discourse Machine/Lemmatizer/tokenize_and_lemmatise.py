import subprocess


input_file = "test_file.txt"
bash_call = "tokenize_and_lemmatise_bash.sh " + input_file

lemmatized_dict = subprocess.check_output(bash_call, shell=True)
print lemmatized_dict

for line in lemmatized_dict:
    pass #This is where we construct the finished, lemmatized file from the CST output. TO BE DONE.

