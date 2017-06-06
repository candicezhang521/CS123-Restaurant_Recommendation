-- Concat all reviews about a restaurant
.mode csv
.separator ","
.output restaurant_reviews.csv
SELECT business_id, GROUP_CONCAT(review) AS review
FROM yelp_reviews
GROUP BY business_id
ORDER BY business_id;


-- Import the business information
CREATE TABLE restaurant_info
(num INT,
 name TEXT,
 address TEXT,
 business_id TEXT,
 postal_code TEXT,
 is_open INT,
 state TEXT,
 stars TEXT,
 city TEXT,
 categories TEXT);

.separator ","
.import restaurants_data.csv restaurant_info
DELETE FROM restaurant_info WHERE name = 'name';














