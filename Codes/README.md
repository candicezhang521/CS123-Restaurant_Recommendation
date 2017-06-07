# Restaurant Recommendation Project  |  Logistic Flow

> Please patiently follow the steps below to make sure that you successfully run all the scripts. Feel free to contact Y Cube for any corrections, suggestions, or questions.


## 1. Data Download

Please download the raw datasets <code>yelp_academic_dataset_review.json</code> and <code>yelp_academic_dataset_business.json</code> from [Yelp](https://www.yelp.com/dataset_challenge). The dataset is also available on [Google Drive](https://drive.google.com/drive/folders/0B4ea4c0UtYaYT0hMWnhIY2QzUEU?usp=sharing).

A cleaned small subset of the <code>yelp_academic_dataset_review</code> dataset <code>test_data.csv</code> including 50 users as test dataset and a cleaned version of <code>yelp_academic_dataset_business</code> dataset <code>cs123_restaurants.csv</code> are available in the <code>Data</code> section. You are welcome to download them and thus skip the Data Cleaning Step. However, you may need to make sure that you import the right dataset into the yelp.db in <code>database_construction.sql</code>.


## 2. Data Cleaning

**(1) _json_to_csv.py_:** This python script converts all the json files downloaded from Yelp to csv format files. It is provided by Yelp.
* Input: yelp_academic_reviews.json / yelp_academic_dataset_business.json
* Output: yelp_academic_reviews.csv / yelp_academic_dataset_business.csv
```sh
python3 json_to_csv.py yelp_academic_reviews.json
```

**(2) _cs123_reviews_filtering.py_:** This python script deals with filtering and standardization of the <code>yelp_academic_dataset_review</code> dataset. It cleans the dataset left with variables of interest including text_reviews, user_id, business_id, stars and filters all punctuations and stop words in text_reivews for further convenience.
* Input: yelp_academic_dataset_reviews.csv
* Output: fresh_yelp_reviews.csv
```sh
python3 cs123_reviews_filtering.py
```

**(3) _cs123_business_filtering.py_:** This python script deals with the filtering and standardization of the <code>yelp_academic_dataset_business</code> dataset. It cleans the dataset left with variables of interest including name, business_id, city, categories, address, state, postal_code.
* Input: yelp_academic_dataset_business.csv
* Output: cs123_restaurants.csv
```sh
python3 cs123_business_filtering.py
```


## 3. Data Storage

**(1) _database_construction.sql_:** This sql srcipt helps store the dataset in a sqlite3 database. It generates three sqlite3 tables and three csv files.
* Input: fresh_yelp_reviews.csv / test_data.csv
	 cs123_restaurants.csv
* Output: yelp.db with table yelp_reviews, table user, and table restaurant_info
	  user_reviews.csv
	  restaurant_reviews.csv
	  user_pairs.csv
```sh
sqlite3 yelp.db < database_construction.sql
```

**(2) _user_reviews_filtering.py_:** This python script filters out the comma in user reviews appeared because of the sqlite3 GROUP_CONCAT command.
* Input: user_reviews.csv
* Output: user_reviews_nocommas.csv
```sh
python3 user_reviews_filtering.py
```

**(3) _restaurant_reviews_filtering.py_:** This python script filters out the comma in restaurant reviews appeared because of the sqlite3 GROUP_CONCAT command.
* Input: restaurant_reviews.csv
* Output: restaurant_reviews_nocommas.csv
```sh
python3 restaurant_reviews_filtering.py
```


## 4. User Data Vectorizaion - Find the most similar pair of users

**(1) _find_base_vector.py_:** This python script includes an MRJob that finds all the single word occured in all the reviews.
* Input: fresh_yelp_reviews.csv / test_data.csv
* Output: base_vector.txt
```sh
python3 find_base_vector.py test_data.csv > base_vector.txt
python3 find_base_vector.py fresh_yelp_reviews.csv > base_vector.txt
```

**(2) _find_vectors.py_:** This python script includes an MRJob that finds all the words occured in every single user's all reviews and create a vector based on the base vector with weights as frequency of occurence of every single word.
* Input: user_reviews_nocommas.csv
* Output: user_vectors.txt
```sh
python3 find_vectors.py user_reviews_nocommas.csv > user_vectors.txt
```

**(3) _user_vector_construction.sql_:** This sqlite3 script imports the vector of users into a table.
* Input: user_vectors.txt
* Output: table user_vector in yelp.db
```sh
sqlite3 yelp.db < user_vector_construction.sql
```

**(4) _find_similar_users.py_:** This python script includes an MRJob that compute the cosi similarity between each pair of users and finds the most similar one for each user.
* Input: user_pairs.csv
	 table user_vector in yelp.db
* Output: similar_users.txt
```sh
python3 find_similar_users.py user_pairs.csv > similar_users.txt
```


## 5. Restaurant Data Vectorizaion - Find the recommendations for users

**(1) _restaurant_pairs.py_:** This python script finds all the pairs of restaurants that the most similar user pairs have respectively visited.
* Input: similar_users.txt
	 table yelp_reviews in yelp.db
* Output: restaurant_pairs.csv
```sh
python3 restaurant_pairs.py
```

**(2) _find_vectors.py_:** This is the same python script used in 4(2). It includes an MRJob that finds all the words occured in every single restaurant's all reviews and create a vector based on the base vector with weights as frequency of occurence of every single word.
* Input: restaurant_reviews_nocommas.csv
* Output: restaurant_vectors.txt
```sh
python3 find_vectors.py restaurant_reviews_nocommas.csv > restaurant_vectors.txt
```

**(3) _restaurant_vector_construction.sql_:** This sqlite3 script imports the vector of restaurants into a table.
* Input: restaurant_vectors.txt
* Output: table restaurant_vector in yelp.db
```sh
sqlite3 yelp.db < restaurant_vector_construction.sql
```

**(4) _find_similar_restaurants.py_:** This python script includes an MRJob that computes the cosi similarity between each pair of restaurants and finds the pairs with higher cosi similarity than (1 - cosi similarity of the pair of users).
* Input: restaurant_pairs.csv
	table restaurant_vector in yelp.db
* Output: similar_restaurants.txt
```sh
python3 find_similar_restaurants.py restaurant_pairs.csv > similar_restaurants.txt
```

**(5) _analysis.py_:** This python script shows the recommendation results and computes the success rate of the recommendation system of this project.
* Input: similar_restaurants.txt
* Output: recommendation_results.csv
```sh
python3 analysis.py
```






