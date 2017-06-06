import pandas as pd 

column_names = ['user_id', 'review']
users_review_df = pd.read_csv('user_reviews.csv', header=None, names=column_names)
users_review_df['review'] = users_review_df['review'].str.replace(',', ' ')
users_review_df.to_csv('user_reviews_nocommas.csv', header=False,
    				   index=False,sep=',',encoding='utf-8')