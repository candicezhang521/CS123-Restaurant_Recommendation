from mrjob.job import MRJob
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity
import ast
import re
import numpy as np
import sys


'''
This MRJob finds the similar restaurants among all the pair 
of restaunrants that the most similar users have respctively been to.
'''
class MRSimilarRest(MRJob):

    def configure_options(self):
        super(MRSimilarRest, self).configure_options()
        self.add_file_option('--database', default = "yelp_test.db")

    def mapper_init(self):
        self.db = sqlite3.connect(self.options.database)
        self.c = self.db.cursor()

    def mapper(self, _, line):
        num, id1, id2, res1, res2, cos= line.split(',')
        command1 = "SELECT vector FROM restaurant_vector WHERE business_id = ?"
        command2 = "SELECT vector FROM restaurant_vector WHERE business_id = ?"
        self.c.execute(command1, [res1])
        result1 = self.c.fetchall()
        result1 = ast.literal_eval(result1[0][0])
        self.c.execute(command2, [res2])
        result2 = self.c.fetchall()
        result2 = ast.literal_eval(result2[0][0])
        yield [id1, id2, float(cos)], [res1, res2, result1[0], result2[0]]

    def combiner(self, the_id, value_list):
        for vector in value_list:
            similarity_score = cosine_similarity(vector[2], vector[3])
            similarity_score = similarity_score.tolist()
            yield the_id, [(vector[0], vector[1]), similarity_score]

    def reducer_init(self):
        self.result = []

    def reducer(self, the_id, value_list):
        for st in value_list:
            if float(st[1][0][0]) >= 1 - the_id[2]:
                self.result.append(st)
        yield the_id, self.result
        self.result = []


if __name__ == '__main__':
    MRSimilarRest.run()