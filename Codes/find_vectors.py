from mrjob.job import MRJob
import re

base_vector = []
length = 0
WORD_RE = re.compile(r"[\w']+")


def txt_to_list(txt):
    f = open(txt, "r" )
    a = []
    for line in f:
        a.append(line)
    string_to_re = a[0][5:]
    words_lst = re.findall('\"*([0-9a-zA-Z\_]+)\"',string_to_re)
    f.close()
    return words_lst, len(words_lst)

'''
This MRJob finds all the words occured in every single user's all reviews
and fits in the base vector created by find_base_vector.py.
'''
class MRWordFreqCount(MRJob):

    def mapper(self, _, line):
        the_id, review = line.split(',')
        # sqlite3 automatically adds double quotes for the review string,
        # thus we use review[1:-1] to get rid of them
        yield the_id, review.lower().split()

    def combiner_init(self):
        self.temp = [0] * length

    def combiner(self, the_id, word_list):
        for word in word_list:
            for word2 in word:
                self.temp[base_vector.index(word2)] += 1
        yield the_id, self.temp
        self.temp = [0] * length

    def reducer(self, the_id, word_list):
        yield the_id, list(word_list)


if __name__ == '__main__':
    base_vector, length = txt_to_list("base_vector.txt")
    MRWordFreqCount.run()