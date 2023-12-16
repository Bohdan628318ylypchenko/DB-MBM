-- location info
DROP TABLE IF EXISTS location_info CASCADE;
CREATE TABLE location_info (
    location_info_id BIGSERIAL NOT NULL,
    region_name VARCHAR(255) NOT NULL,
    area_name VARCHAR(255) NOT NULL,
    territory_name VARCHAR(255) NOT NULL,
    CONSTRAINT location_info_pk PRIMARY KEY (location_info_id)
);

-- person location info
DROP TABLE IF EXISTS person_location_info CASCADE;
CREATE TABLE person_location_info (
    person_location_info_id BIGSERIAL NOT NULL,
    person_location_type VARCHAR(256) NOT NULL,
    location_info_id BIGINT NOT NULL,
    CONSTRAINT person_location_info_pk PRIMARY KEY (person_location_info_id),
    CONSTRAINT location_info_fk FOREIGN KEY (location_info_id) REFERENCES location_info(location_info_id)
);

-- learning profile
DROP TABLE IF EXISTS learning_profile CASCADE;
CREATE TABLE learning_profile (
    learning_profile_id BIGSERIAL NOT NULL,
    learning_profile_name VARCHAR(256) NOT NULL,
    learning_profile_language VARCHAR(256) NOT NULL,
    CONSTRAINT learning_profile_pk PRIMARY KEY (learning_profile_id)
);

-- educational institution
DROP TABLE IF EXISTS educational_institution CASCADE;
CREATE TABLE educational_institution (
    educational_institution_id BIGSERIAL NOT NULL,
    educational_institution_name VARCHAR(256) NOT NULL,
    educational_institution_parent VARCHAR(256) NOT NULL,
    educational_institution_type VARCHAR(256) NOT NULL,
    location_info_id BIGINT NOT NULL,
    CONSTRAINT educational_institution_pk PRIMARY KEY (educational_institution_id),
    CONSTRAINT location_info_fk FOREIGN KEY (location_info_id) REFERENCES location_info(location_info_id)
);

-- person
DROP TABLE IF EXISTS person CASCADE;
CREATE TABLE person (
    person_id BIGSERIAL NOT NULL,
    person_out_id VARCHAR(256) NOT NULL,
    birth SMALLINT NOT NULL,
    registration_status VARCHAR(256) NOT NULL,
    sex_type VARCHAR(256) NOT NULL,
    learning_profile_id BIGINT,
    educational_institution_id BIGINT,
    person_location_info_id BIGINT NOT NULL,
    CONSTRAINT person_pk PRIMARY KEY (person_id),
    CONSTRAINT learning_profile_fk FOREIGN KEY (learning_profile_id) REFERENCES learning_profile(learning_profile_id),
    CONSTRAINT educational_institution_fk FOREIGN KEY (educational_institution_id) REFERENCES educational_institution(educational_institution_id),
    CONSTRAINT person_location_info_fk FOREIGN KEY (person_location_info_id) REFERENCES person_location_info(person_location_info_id)
);

-- test institution
DROP TABLE IF EXISTS test_institution CASCADE;
CREATE TABLE test_institution (
    test_institution_id BIGSERIAL NOT NULL,
    test_institution_name VARCHAR(256) NOT NULL,
    location_info_id BIGINT NOT NULL,
    CONSTRAINT test_institution_pk PRIMARY KEY (test_institution_id),
    CONSTRAINT location_info_fk FOREIGN KEY (location_info_id) REFERENCES location_info(location_info_id)
);

-- test result (according to TPH)
DROP TABLE IF EXISTS test_result CASCADE;
CREATE TABLE test_result (
    test_result_id BIGSERIAL NOT NULL,
    subject_name VARCHAR(28) NOT NULL,
    test_status VARCHAR(256) NOT NULL,
    test_language VARCHAR(256),
    dpa_level VARCHAR(256),
    ball_100 DECIMAL,
    ball_12 SMALLINT,
    ball SMALLINT,
    adapt_scale SMALLINT,
    year_of_attempt SMALLINT NOT NULL,
    CONSTRAINT test_result_pk PRIMARY KEY (test_result_id)
);

DROP TABLE IF EXISTS p_ti_tr CASCADE;
CREATE TABLE p_ti_tr (
    person_id BIGINT NOT NULL,
    test_institution_id BIGINT NOT NULL,
    test_result_id BIGINT NOT NULL,
    CONSTRAINT person_fk FOREIGN KEY (person_id) REFERENCES person(person_id),
    CONSTRAINT test_institution_fk FOREIGN KEY (test_institution_id) REFERENCES test_institution(test_institution_id),
    CONSTRAINT test_result_fk FOREIGN KEY (test_result_id) REFERENCES test_result(test_result_id)
);
