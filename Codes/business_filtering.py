import pandas as pd 
import numpy as np 

business_df = pd.read_csv('yelp_academic_dataset_business.csv',header=0)

del business_df['neighborhood']
del business_df['latitude']
del business_df['longitude']
del business_df['attributes']
del business_df['hours']
del business_df['type']
del business_df['review_count']
del business_df['is_open']
business_df['name'] = business_df.name.str[2:-1] 
business_df['business_id'] = business_df.business_id.str[2:-1] 
business_df['city'] = business_df.city.str[2:-1] 
business_df['categories'] = business_df.categories.str[1:-1]
business_df['address'] = business_df.address.str[2:-1] 
business_df['state'] = business_df.state.str[2:-1] 
business_df['postal_code'] = business_df.postal_code.str[2:-1] 

business_df = business_df.dropna(axis=0, how='any')

restaurants_df=business_df[business_df.categories.str.contains('Restaurants')]


restaurants_df.to_csv('cs123_restaurants.csv', sep = ',', encoding = 'utf-8')
