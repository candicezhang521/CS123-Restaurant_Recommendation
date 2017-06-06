import numpy as np
import pandas as pd
import sqlite3

conn = sqlite3.connect('yelp_test.db')
c = conn.cursor()

similar_users = pd.read_table('similar_users.txt', sep='\t', header=None)
restaurant_pairs = pd.DataFrame()

for i in range(len(similar_users)):
	user1 = similar_users.iloc[i, 0]
	user2 = similar_users.iloc[i, 1][2: 24]
	score = similar_users.iloc[i, 1][27: -1]
	query = "SELECT a.user_id, b.user_id, a.business_id, b.business_id FROM (SELECT user_id, business_id FROM yelp_reviews WHERE user_id = ?) AS a CROSS JOIN (SELECT user_id, business_id FROM yelp_reviews WHERE user_id = ?) AS b WHERE a.business_id != b.business_id;"
	c.execute(query, (user1, user2))
	result = c.fetchall()
	df_result = pd.DataFrame.from_records(result)
	df_result['similarity'] = score
	restaurant_pairs = restaurant_pairs.append(df_result)

restaurant_pairs[[0, 1, 2, 3, 'similarity']].to_csv('restaurant_pairs.csv', header=None)

conn.close()