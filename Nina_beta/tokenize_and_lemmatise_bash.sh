#!/bin/bash

#Get the filename from the argument
args=("$@")
INPUT_FILE=${args[0]}

#Navigate to the correct folder
cd '../CST tools/'

#Run the rtfreader
rtfreader -T -i $INPUT_FILE

#Running the cstlemma
TOKENIZED_FILE=$INPUT_FILE'.segments'
./cstlemma -L -f flexrules -i $TOKENIZED_FILE