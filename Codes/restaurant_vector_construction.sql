-- Import calculated single business vector
CREATE TABLE restaurant_vector
(business_id TEXT,
 vector TEXT);

.separator "\t"
.import restaurant_vectors.txt restaurant_vector