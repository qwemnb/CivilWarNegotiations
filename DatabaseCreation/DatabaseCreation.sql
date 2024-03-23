CREATE TABLE IF NOT EXISTS heather.files (id  int NOT NULL AUTO_INCREMENT, file_name varchar(255), PRIMARY KEY (id));

CREATE TABLE IF NOT EXISTS heather.raw_data (id int NOT NULL AUTO_INCREMENT, file_id int NOT NULL, question_id int NOT NULL, answer text, PRIMARY KEY (id), FOREIGN KEY (file_id) REFERENCES  heather.files(id), FOREIGN KEY (question_id) REFERENCES heather.questions(id));

CREATE TABLE IF NOT EXISTS heather.questions (id int NOT NULL AUTO_INCREMENT, question_text text NOT NULL, question_hash varchar(256) NOT NULL, question_display_text text NOT NULL, PRIMARY KEY(id), UNIQUE(question_hash));

CREATE TABLE IF NOT EXISTS heather.split_rebel_groups_by_year (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), rebel_aims text,  line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) );

CREATE TABLE IF NOT EXISTS heather.split_govt_changes_by_year (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

#CREATE TABLE IF NOT EXISTS heather.split_ceasefire_declared

CREATE TABLE IF NOT EXISTS heather.split_offer_inducements (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), answer_month int, line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) );

CREATE TABLE IF NOT EXISTS heather.split_offer_inducements (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), answer_month int, line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) );

CREATE TABLE IF NOT EXISTS heather.split_negotiations_suggested (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), answer_month int, line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_negotiations_refused (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), answer_month int, refused_to_negotiate varchar(3), line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_content_of_negotiations (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), answer_month int, line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_end_without_signing (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), answer_month int, who_did_not_sign varchar(12), line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_agreement_signed (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), answer_month int, agreement_signed varchar(3), line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_agreement_end_fighting (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), answer_month int, end_fighting varchar(3), line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_reached_not_signed (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), answer_month int, not_signed varchar(3), line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_unsigned_end_fighting (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), answer_month int, unsigned_end_fighting varchar(3), line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_outside_offer_mediation (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), answer_month int, mediation_offered varchar(3), line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_mediation_occur (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_year varchar(8), answer_month int, did_mediation_occur varchar(3), line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_un_involved (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_start_year varchar(8),  answer_end_year varchar(8), un_involved varchar(3), line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_igo_involved (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_start_year varchar(8),  answer_end_year varchar(8), igo_involved varchar(3), line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_third_party_intervene (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, group_type varchar(12), did_third_party_intervene varchar(3), answer_start_year varchar(8),  answer_end_year varchar(8), intervention_type text, line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_govt_receive_aid (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_start_year varchar(8),  answer_end_year varchar(8), govt_receive_aid varchar(3), line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

CREATE TABLE IF NOT EXISTS heather.split_rebels_receive_aid (id int NOT NULL AUTO_INCREMENT, raw_data_id int NOT NULL, file_id int NOT NULL, question_id int NOT NULL, answer_start_year varchar(8),  answer_end_year varchar(8), rebels_receive_aid varchar(3), line_data text, PRIMARY KEY (id), FOREIGN KEY (question_id) REFERENCES  heather.questions(id) ); 

#CREATE TABLE IF NOT EXIST heather.split_did_conflict_recur