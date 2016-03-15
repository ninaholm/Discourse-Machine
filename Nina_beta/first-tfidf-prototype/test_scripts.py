import codecs
import operator
from Document import *
from Corpus import *
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')

corpses = []
base_folder = "book_data/"

def create_new_document(content):
    doc = Document("doc")
    doc.dictionary = doc.count_words(content)
    return doc

def import_file(file_content):
    all_docs = []
    counter = 0
    content = []
    for line in file_content:
        counter += 1
        content.append(str(line))
        if counter%1000==0:
            print "Size of content is", len(content)
            print "Number of docs is", len(all_docs)
            all_docs.append(create_new_document(content))
            del content[:]
    return all_docs

# Returns the maximum X terms of a list
def get_top_terms(dict, number_of_terms):
    sorted_tf_idf_list = sorted(dict.items(),
                            key=operator.itemgetter(1), reverse=True)
    return sorted_tf_idf_list[0:number_of_terms]


print os.listdir(".")

# Read text files from the base folder
for file in os.listdir(base_folder):
    print "Now grabbing contents from file", file
    cor = Corpus(file)
    f = codecs.open(base_folder + file, encoding="utf-8")
    cor.list_of_documents = import_file(f)
    print "Number of documents is", len(cor.list_of_documents)
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



