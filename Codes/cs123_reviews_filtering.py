import pandas as pd 
import numpy as np 

cs123_reviews_df = pd.read_csv('yelp_academic_dataset_reviews.csv',header=0)

del cs123_reviews_df['type']
del cs123_reviews_df['funny']
del cs123_reviews_df['cool']
del cs123_reviews_df['useful']
del cs123_reviews_df['review_id']
del cs123_reviews_df['date']

cs123_reviews_df['text'] = cs123_reviews_df.text.str.replace('(b[\'\"]?)*([\'\"])' , '')
cs123_reviews_df['text'] = cs123_reviews_df.text.str.replace('(\W)' , ' ')
cs123_reviews_df['text'] = cs123_reviews_df.text.str.replace('\s(n)\s' , ' ')
cs123_reviews_df['business_id'] = cs123_reviews_df.business_id.str.replace('(b[\'\"]?)*([\'\"])' , '')
cs123_reviews_df['user_id'] = cs123_reviews_df.user_id.str.replace('(b[\'\"]?)*([\'\"])' , '')

cs123_reviews_df.to_csv('cs123_reviews_no_punc.csv', sep = ',', header=False,encoding = 'utf-8')
