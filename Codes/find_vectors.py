from mrjob.job import MRJob
import re
import sys

base_vector = []
length = 0


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

    def configure_options(self):
        super(MRWordFreqCount, self).configure_options()
        self.add_file_option('--fff', default = "base_vector.txt")

    def mapper(self, _, line):
        the_id, review = line.split(',')
        # sqlite3 automatically adds double quotes for the review string,
        # thus we use review[1:-1] to get rid of them
        yield the_id, review.lower().split()

    def combiner_init(self):
        self.base_vector,self.length=txt_to_list(self.options.fff)
        self.temp = [0] * self.length

    def combiner(self, the_id, word_list):
        w=self.base_vector
        for word in word_list:
            for word2 in word:
                try:
                    self.temp[w.index(word2)] += 1
                except:
                    pass
        yield the_id, self.temp
        self.temp = [0] * self.length

    def reducer(self, the_id, word_list):
        yield the_id, list(word_list)


if __name__ == '__main__':
    MRWordFreqCount.run()