import math

class Corpus(object):

    def __init__(self, name):
        self.name = name
        self.list_of_documents = []
        self.total_words = 0
        self.tfidf_dic = {}

    # Calculate total number of words in corpus
    def calculate_total_words(self):
        total = 0
        for doc in self.list_of_documents:
            total += sum(doc.dictionary.values())
        self.total_words = total
        return total

    # Create a subset of corpus documents containing the word
    def subset_corpus(self, word):
        new_name = self.name + word
        subset = Corpus(new_name)
        for doc in self.list_of_documents:
            if doc.dictionary.__contains__(word):
                subset.list_of_documents.append(doc)
        return subset

    # Counts the number of documents wherein a specific word appears
    def number_of_documents_containing(self, word):
        total = 0
        for doc in self.list_of_documents:
            if doc.dictionary.__contains__(word):
                total += 1
        return total

    # Counts the number of times a word appears within corpus
    def number_of_occurences(self, word):
        total = 0
        for doc in self.list_of_documents:
            if doc.dictionary.__contains__(word):
                total += doc.dictionary[word]
        return total

    # Prints the stats of specific word within corpus
    def print_word_stats(self, word):
        print word, "appears in", \
            self.number_of_documents_containing(word), "documents and a total of", \
            self.number_of_occurences(word), "times"

    # Prints stats of corpus
    def print_stats(self):
        print self.name, "contains", len(self.list_of_documents), \
            "documents and", self.calculate_total_words(), "words"

    # Returns a list of all words in corpus
    def all_words(self):
        all = {}
        for doc in self.list_of_documents:
            all.update(doc.dictionary)
        return all

    # Returns a list of tf-idf terms from full corpus based on a single word input
    def calculate_tfidf(self, input):
        # get idf variables
        total_number_of_documents = len(self.list_of_documents)

        new_corpus = self.subset_corpus(input)
        total_number_of_words_in_document = new_corpus.number_of_occurences(input)

        for doc in new_corpus.list_of_documents:
            for word in doc.dictionary:
                number_of_documents_containing_word = self.number_of_documents_containing(word)
                number_of_word_occurences = doc.dictionary[word]

                # Calculate tf, idf, and tf-idf
                tf = float(number_of_word_occurences) / float(total_number_of_words_in_document)
                idf = math.log(float(total_number_of_documents) / float(number_of_documents_containing_word))
                tf_idf = tf * idf

                shortened_tf_idf = float("{0:.4f}".format(tf_idf))

                if new_corpus.tfidf_dic.__contains__(word):
                    new_corpus.tfidf_dic[word] = sum([tf_idf, new_corpus.tfidf_dic[word]]) / 2
                else:
                    new_corpus.tfidf_dic[word] = tf_idf

        return new_corpus.tfidf_dic
