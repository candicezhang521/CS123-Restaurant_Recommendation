import pandas as pd

column_names = ['business_id','review']
restaurant_review_df = pd.read_csv('restaurant_reviews.csv', header=None,\
					   names=column_names)
restaurant_review_df['review'] = restaurant_review_df.review.str.replace(',',' ')
restaurant_review_df.to_csv('restaurant_reviews_nocommas.csv', header=False,
	index=False, sep=',', encoding='utf-8')