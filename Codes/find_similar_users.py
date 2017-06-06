from mrjob.job import MRJob
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity
import ast
import re
import numpy as np


'''
This MRJob finds the most similar user for every user.
'''
class MRMostSimilarUser(MRJob):

    def configure_options(self):
        super(MRMostSimilarUser, self).configure_options()
        self.add_file_option('--database', default = "yelp_test.db")

    def mapper_init(self):
        self.db = sqlite3.connect(self.options.database)
        self.c = self.db.cursor()
    def mapper(self, _, line):
        id1,id2 = line.split(',')
        
        command1 = "SELECT vector FROM user_vector WHERE user_id = ?"
        command2 = "SELECT vector FROM user_vector WHERE user_id = ?"
        self.c.execute(command1,[id1])
        result1 = self.c.fetchall()
        result1 = ast.literal_eval(result1[0][0])

        self.c.execute(command2,[id2])
        result2 = self.c.fetchall()
        result2 = ast.literal_eval(result2[0][0])
        yield id1, [id2, result1[0], result2[0]]

    def combiner(self, the_id, value_list):
        for vector in value_list:
            similarity_score = cosine_similarity(vector[1], vector[2])
            similarity_score = similarity_score.tolist()
            yield the_id, [vector[0], similarity_score]

    def reducer_init(self):
        self.result_max = 0
        self.result_id = ""

    def reducer(self, the_id, value_list):
        for st in value_list:
            if st[1][0][0] > self.result_max:
                self.result_max = st[1][0][0]
                self.result_id = st[0]
        yield the_id, [self.result_id, self.result_max]
        self.result_max = 0
        self.result_id = ''


if __name__ == '__main__':
    MRMostSimilarUser.run()