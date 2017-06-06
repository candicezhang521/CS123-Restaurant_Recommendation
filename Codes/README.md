# Restaurant Recommendation Project | Logistic Flow

This file aims to describe the logistic flow of this project, giving a general idea of how to use different files.

**1. Data Download**

Please download raw dataset from [Yelp](https://www.yelp.com/dataset_challenge). The dataset is also available on the private [Google Drive]().

A cleaned small subset of the dataset _test_data.csv_ including 500 users is available in the <code>Data</code> section as test dataset and you are welcome to download it and thus skip the Data Cleaning Step.

**2. Data Cleaning**

(1) _json_to_csv.py_: This python script converts all the json files downloaded from Yelp to csv format files.
	Input: yelp_academic_reviews.json
	Output: yelp_academic_reviews.csv
	```
	python3 json_to_csv.py yelp_academic_reviews.json
	```

(2) _-.py_: This python script deals with filtering and standardization of the dataset. It cleans the dataset left with variables of interest, including text_reviews, user_id, business_id, and replaces all punctuations in text_reivews with space for further convenience.
	Input: yelp_academic_reviews.csv
	Output: filtered_reviews.csv
	```
	python3 
	```

(3) _-text_filtering.py_: This python script filtered out the stop words from the text_reviews, for convience of calculating the similarity between users without the influnce of literacy level.
	Input: filtered_reviews.csv
	Output: reviews_nostopwords.csv
	```
	python3
	```

**3. Data Storage**

_database_construction.sql_: This sql srcipt helps store the dataset in a sqlite3 database. It generates two sqlite3 tables and two csv files.
	Input: filtered_reviews.csv / test_data.csv 
	Output: yelp_test.db with table yelp_reviews and table user
			user_reviews.csv
			user_pairs.csv
	```
	sqlite3 yelp_test.db < database_construction.sql
	```

**4. User Data Vectorizaion - Find the most similar pair of users**

(1) _find_base_vector.py_: This python script includes an MRJob that finds all the single word occured in all the reviews.
	Input: filtered_reviews.csv / test_data.csv
	Output: base_vector.txt
	```
	python3 find_base_vector.py test_data.csv > base_vector.txt
	```

(2) _user_reviews_filtering.py_: This python script filters out the comma in user reviews appeared because of the sqlite3 GROUP_CONCAT command.
	Input: user_reviews.csv
	Output: user_reviews_nocommas.csv
	```
	python3 user_reviews_filtering.py
	```

(3) _find_vectors.py_: This python script includes an MRJob that finds all the words occured in every single user's all reviews and create a vector based on the base vector with weights as frequency of occurence of every single word.
	Input: user_reviews_nocommas.csv
	Output: user_vectors.txt
	```
	python3 find_vectors.py user_reviews_nocommas.csv > user_vectors.txt
	```

(4) _user_vector_construction.sql_: This sqlite3 script imports the vector of users into a table.
	Input: user_vectors.txt
	Output: table user_vector in yelp_test.db
	```
	sqlite3 yelp_test.db < user_vector_construction.sql
	```

(5) _find_similar_users.py_: This python script includes an MRJob that compute the cosi similarity between each pair of users and finds the most similar one for each user.
	Input: user_pairs.csv
		   table user_vector in yelp_test.db
	Output: similar_users.txt
	```
	python3 find_similar_users.py user_pairs.csv > similar_users.txt
	```

**5. Restaurant Data Vectorizaion - Find the recommendations for users**

(1) _restaurant_info.sql_: This sqlite3 script concatenates all reviews about every restaurant and imports the restaurant infomation. It generates one csv file and a sqlite3 table.
	Input: restaurant_info.sql
	Output: restaurant_reviews.csv
			table restaurant_info in yelp_test.db
	```
	sqlite3 yelp_test.db < restaurant_info.sql
	```

(2) _restaurant_reviews_filtering.py_: This python script filters out the comma in restaurant reviews appeared because of the sqlite3 GROUP_CONCAT command.
	Input: restaurant_reviews.csv
	Output: restaurant_reviews_nocommas.csv
	```
	python3 restaurant_reviews_filtering.py
	```

(3) _restaurant_pairs.py_: This python script finds all the pairs of restaurants that the most similar user pairs have respectively visited.
	Input: similar_users.txt
		   table yelp_reviews in yelp_test.db
	Output: restaurant_pairs.csv
	```
	python3 restaurant_pairs.py
	```

(4) _find_vectors.py_: This is the same python script used in 4(3). It includes an MRJob that finds all the words occured in every single restaurant's all reviews and create a vector based on the base vector with weights as frequency of occurence of every single word.
	Input: restaurant_reviews_nocommas.csv
	Output: restaurant_vectors.txt
	```
	python3 find_vectors.py restaurant_reviews_nocommas.csv > restaurant_vectors.txt
	```

(5) _restaurant_vector_construction.sql_: This sqlite3 script imports the vector of restaurants into a table.
	Input: restaurant_vectors.txt
	Output: table restaurant_vector in yelp_test.db
	```
	sqlite3 yelp_test.db < restaurant_vector_construction.sql
	```

(6) _find_similar_restaurants.py_: This python script includes an MRJob that computes the cosi similarity between each pair of restaurants and finds the pairs with higher cosi similarity than (1 - cosi similarity of the pair of users).
	Input: restaurant_pairs.csv
		   table restaurant_vector in yelp_test.db
	Output: similar_restaurants.txt
	```
	python3 find_similar_restaurants.py restaurant_pairs.csv > similar_restaurants.txt
	```

(7) _analysis.py_: This python script conducts the success rate of the recommendation system of this project.
	Input: similar_restaurants.txt
	Output: recommendation_results.csv
	```
	python3 analysis.py
	```






