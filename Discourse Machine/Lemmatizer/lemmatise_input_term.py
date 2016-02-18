
#apt-get install python-pip

#pip install subprocess

def run():
	import subprocess
	import sys

	# Get input term
	input_term = sys.argv[1]

	# Write input term to file
	temp_file = "temp"
	file = open(temp_file, "w")
	file.write(input_term)
	file.close()
	
	# Call the lemmatiser program
	lem_call = "./CST_tools/cstlemma/src/cstlemma -L -f CST_tools/flexrules -i " + temp_file
	lem = subprocess.check_output(lem_call, shell=True)

	# Extract the lemmatised term
	lem = lem.split("\n")
	lem = lem[2].split("\t")
	print "The input term was: \t\t" + input_term
	print "The lemmatised word is: \t" + lem[1]
	return lem[1]

run()
