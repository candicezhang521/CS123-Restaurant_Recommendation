-- Import the reviews to a table
CREATE TABLE yelp_reviews
(review TEXT,
 stars TEXT,
 user_id TEXT,
 business_id TEXT);

.separator ","
.import test_data.csv yelp_reviews
--.import fresh_yelp_reviews.csv yelp_reviews
DELETE FROM yelp_reviews WHERE review = 'text';


-- Concat all reviews of a user
.mode csv
.separator ","
.output user_reviews.csv
SELECT DISTINCT user_id, GROUP_CONCAT(review) AS review
FROM yelp_reviews
GROUP BY user_id
ORDER BY user_id;


-- Concat all reviews about a restaurant
.mode csv
.separator ","
.output restaurant_reviews.csv
SELECT business_id, GROUP_CONCAT(review) AS review
FROM yelp_reviews
GROUP BY business_id
ORDER BY business_id;


-- Import the user_id to a table to increase the efficiency of cross join
CREATE TABLE user
(user_id TEXT);

INSERT INTO user
SELECT DISTINCT user_id FROM yelp_reviews;


-- Find the user pairs
.mode csv
.separator ","
.output user_pairs.csv
SELECT a.user_id, b.user_id
FROM user a
CROSS JOIN user b
WHERE a.user_id != b.user_id
ORDER BY a.user_id;


-- Import the business information
CREATE TABLE restaurant_info
(num INT,
 name TEXT,
 address TEXT,
 business_id TEXT,
 postal_code TEXT,
 state TEXT,
 stars TEXT,
 city TEXT,
 categories TEXT);

.separator ","
.import cs123_restaurants.csv restaurant_info
DELETE FROM restaurant_info WHERE name = 'name';



