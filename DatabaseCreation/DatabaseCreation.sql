CREATE TABLE IF NOT EXISTS heather.files (id  int NOT NULL AUTO_INCREMENT, file_name varchar(255), PRIMARY KEY (id));

CREATE TABLE IF NOT EXISTS heather.raw_data (id int NOT NULL AUTO_INCREMENT, file_id int NOT NULL, question text NOT NULL, answer text, PRIMARY KEY (id), FOREIGN KEY (file_id) REFERENCES  heather.files(id));

CREATE TABLE IF NOT EXISTS heather.questions (id int NOT NULL AUTO_INCREMENT, question_text text NOT NULL, question_hash varchar(256) NOT NULL, PRIMARY KEY(id), UNIQUE(question_hash));

CREATE TABLE IF NOT EXISTS heather.govt_changes_by_year (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), year_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 
