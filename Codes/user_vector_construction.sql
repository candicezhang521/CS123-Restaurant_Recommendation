-- Import calculated single user vector
CREATE TABLE user_vector
(user_id TEXT,
 vector TEXT);

.separator "\t"
.import user_vectors.txt user_vector