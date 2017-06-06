from mrjob.job import MRJob
import re

WORD_RE = re.compile(r"[\w']+")

'''
This MRJob finds all the single word occured in all the reviews
users have provided.
'''

class MRWordFreqCount(MRJob):

    def mapper(self, _, line):
        review, *rest = line.split(',');
        for word in WORD_RE.findall(review):
            yield None, word.lower()

    def combiner(self, _, word):
        yield None, list(set(word))

    def reducer_init(self):
        self.result = set()

    def reducer(self, _, word_list):
        for word in word_list:
            self.result = self.result.union(word)
        yield None, list(self.result)


if __name__ == '__main__':
    MRWordFreqCount.run()