import numpy as np
import pandas as pd
import ast

data = pd.read_table('similar_restaurants.txt', sep='\t', header=None)
recom_result = pd.DataFrame(columns=('user', 'user_sim', 'recom_success', 'recom'))

for i in range(len(data)):
	user = data.iloc[i, 0][2: 24]
	user_sim = data.iloc[i, 0][53: -1]
	if data.iloc[i, 1] == '[]':
		recom_success = False
	else:
		recom_success = True
	recom = ast.literal_eval(data.iloc[i, 1])
	recom_result.loc[i] = [user, user_sim, recom_success, recom]

recom_result['user_sim'] = pd.to_numeric(recom_result['user_sim'])

success_rate = len(recom_result[(recom_result['recom_success'] == True)]) / len(recom_result)

high_sim_success_rate = len(recom_result[(recom_result['recom_success'] == True)
							& (recom_result['user_sim'] >= 0.5)]) / len(recom_result)

low_sim_success_rate = len(recom_result[(recom_result['recom_success'] == True)
						   & (recom_result['user_sim'] < 0.5)]) / len(recom_result)

print('The overall successful rate of the recommendation system is {}; \
the successful rate for the significantly similar users is {}, \
and for the insignificantly similar users is {}.'\
.format(success_rate, high_sim_success_rate, low_sim_success_rate))

recom_result.to_csv('recommendation_results.csv')

