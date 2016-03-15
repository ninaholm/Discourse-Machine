import codecs
import operator
from Document import *
from Corpus import *
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

urls = ["http://information.dk", "http://politiken.dk", "http://www.b.dk", "http://www.bt.dk"]
corpses = []
base_folder = "output/"

def import_file(file_content):
    doc = Document(file_content.readline())
    all = file_content.readline()
    for line in file_content:
        temp = line.rsplit(" ")
        if len(temp)==2:
            doc.dictionary[temp[0]] = int(temp[1].strip())
    return doc

# Returns the maximum X terms of a list
def get_top_terms(dict, number_of_terms):
    sorted_tf_idf_list = sorted(dict.items(),
                            key=operator.itemgetter(1), reverse=True)
    return sorted_tf_idf_list[0:number_of_terms]


# Read text files from the relevant folders
for folder in os.listdir(base_folder):
    print "Now grabbing contents from folder", folder
    cor = Corpus(folder)
    folder_name = base_folder + folder + "/"

    for file in os.listdir(folder_name):
        f = codecs.open(folder_name + file, encoding="utf-8")
        cor.list_of_documents.append(import_file(f))
        f.close()

    corpses.append(cor)

# Print stats for all corpuses
for corpse in corpses:
    corpse.print_stats()

while True:
    input = raw_input("Enter word: ")

    count = 0
    for corpse in corpses:
        tfidf_list = corpse.calculate_tfidf(input)
        if tfidf_list:
            top = get_top_terms(tfidf_list, 5)
            print corpse.name.upper(), ":"
            corpse.print_word_stats(input)
            for term in top:
                print "       ", str(term[0])
            print ""
            count += 1
    if count==0:
        print "Sorry, the data set does not contain this word."



