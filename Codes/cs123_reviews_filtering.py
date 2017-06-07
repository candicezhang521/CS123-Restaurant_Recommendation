import pandas as pd 
import numpy as np 
import nltk
from nltk import *
from nltk.corpus import stopwords
import re
import pandas as pd

cs123_reviews_df = pd.read_csv('yelp_academic_dataset_review.csv',header=0)

del cs123_reviews_df['type']
del cs123_reviews_df['funny']
del cs123_reviews_df['cool']
del cs123_reviews_df['useful']
del cs123_reviews_df['review_id']
del cs123_reviews_df['date']

#delete the start and end weird letter
cs123_reviews_df['text'] = cs123_reviews_df.text.str[2:-1] 
cs123_reviews_df['business_id'] = cs123_reviews_df.business_id.str[2:-1]
cs123_reviews_df['user_id'] = cs123_reviews_df.user_id.str[2:-1]

#replace all punctuations with whitespace
cs123_reviews_df['text'] = cs123_reviews_df.text.str.replace('(\W)' , ' ')

#replace all digits with whitespace
cs123_reviews_df['text'] = cs123_reviews_df.text.str.replace('(\d)' , ' ')

#replace all n's with whitespace
cs123_reviews_df['text'] = cs123_reviews_df.text.str.replace('\s(n)\s' , ' ')

#filter out all the stop words in reviews, such as 'I','The',etc
stops = nltk.corpus.stopwords.words('english')
cs123_reviews_df['text']= cs123_reviews_df.text.str.lower().str.split()
cs123_reviews_df['text'] = cs123_reviews_df['text'].apply(lambda x: [review for review in x if review not in stops])

cs123_reviews_df['text'] = cs123_reviews_df['text'].apply(lambda x: ', '.join(x))
cs123_reviews_df['text'] = cs123_reviews_df.text.str.replace('(\,)' , ' ')

#convert the fresh dataframe to csv
cs123_reviews_df.to_csv('fresh_yelp_reviews.csv', sep = ',', encoding = 'utf-8',index=False)


