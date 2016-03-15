import codecs
import string


class Document(object):

    def cap(self, s, l):
        return s if len(s)<= l else s[0:l]

    def remove_punctuation(self, x):
        return self.cap(''.join([i for i in x if i not in string.punctuation]), 20)

    def __init__(self, name):
        self.name = self.remove_punctuation(name)
        self.dictionary = {}

    def count_words(self, document):
        for line in document:
            line = line.replace("\n", "").lower()
            lst = line.split(" ")
            for word in lst:
                word = self.remove_punctuation(word)
                if word=="":
                    continue
                if word in self.dictionary.keys():
                    self.dictionary[word] += 1
                else:
                    self.dictionary[word] = 1

    def save_word_count(self, folder_name):
        file_name = "output/" + self.remove_punctuation(folder_name) + "/" + self.name + ".txt"
        with codecs.open(file_name, "w", encoding='utf-8') as wordlist:
            wordlist.write(self.name + "\n")
            wordlist.write("Words in dictionary... {0}\n".format(str(len(self.dictionary))))
            for key in self.dictionary:
                string = key + " " + str(self.dictionary[key]) + "\n"
                wordlist.write(string)
