GLIMPSE_PERSON_BY_ID = """
    SELECT * FROM "person" WHERE person_id = :person_id
"""

GLIMPSE_PERSON_BY_OUT_ID = """
    SELECT * FROM "person" WHERE person_out_id = :person_out_id
"""


# TODO: fix id 
GET_PERSON_BY_OUT_ID = """
    SELECT
        p.person_id,
        p.person_out_id,
        p.birth,
        p.registration_status,
        p.sex_type,
        lp.learning_profile_id,
        lp.learning_profile_name,
        lp.learning_profile_language,
        edi.educational_institution_id,
        edi.educational_institution_name,
        edi.educational_institution_parent,
        edi.educational_institution_type,
        edi_li.location_info_id as edi_li_location_info_id,
        edi_li.region_name as edi_li_region_name,
        edi_li.area_name as edi_li_area_name,
        edi_li.territory_name as edi_li_territory_name,
        pli.person_location_info_id,
        pli.person_location_type,
        pli_li.location_info_id as pli_li_location_info_id,
        pli_li.region_name as pli_li_region_name,
        pli_li.area_name as pli_li_area_name,
        pli_li.territory_name as pli_li_territory_name
    FROM "person" as p
    LEFT JOIN "learning_profile" as lp ON lp.learning_profile_id = p.learning_profile_id
    LEFT JOIN "educational_institution" as edi ON edi.educational_institution_id = p.educational_institution_id
    LEFT JOIN "location_info" as edi_li ON edi_li.location_info_id = edi.location_info_id
    LEFT JOIN "person_location_info" as pli ON pli.person_location_info_id = p.person_location_info_id
    LEFT JOIN "location_info" as pli_li ON pli_li.location_info_id = pli.location_info_id
    WHERE p.person_out_id = :person_out_id
"""

GET_TEST_RESULTS_BY_OUT_ID = """
    SELECT 
        t_r.test_result_id,
        t_r.subject_name,
        t_r.test_status,
        t_r.test_language,
        t_r.dpa_level,
        t_r.ball_100,
        t_r.ball_12,
        t_r.ball,
        t_r.adapt_scale,
        t_r.year_of_attempt
    FROM "person" as p
    LEFT JOIN "p_ti_tr" as p_t ON p_t.person_id = p.person_id
    LEFT JOIN "test_result" as t_r ON t_r.test_result_id = p_t.test_result_id
    WHERE p.person_out_id = :person_out_id
"""

GET_EDUCATIONAL_INSTITUTION = """
    SELECT 
        educational_institution_id,
        educational_institution_name,
        educational_institution_parent,
        educational_institution_type,
        l_i.location_info_id,
        l_i.region_name,
        l_i.area_name,
        l_i.territory_name
    FROM "educational_institution" as e_i
    LEFT JOIN "location_info" as l_i ON l_i.location_info_id = e_i.location_info_id
    WHERE educational_institution_id = :e_i_id
"""

GLIMPSE_EDUCATIONAL_INSTITUTION = """
    SELECT * FROM "educational_institution" WHERE educational_institution_id = :e_i_id
"""

GET_TEST_INSTITUTION = """
    SELECT 
        t_i.test_institution_id,
        t_i.test_institution_name,
        l_i.location_info_id,
        l_i.region_name,
        l_i.area_name,
        l_i.territory_name
    FROM "test_institution" as t_i
    LEFT JOIN "location_info" as l_i ON l_i.location_info_id = t_i.location_info_id
    WHERE t_i.test_institution_id = :t_i_id
"""

GLIMPSE_TEST_INSTITUTION = """
    SELECT * FROM "test_institution" as t_i WHERE t_i.test_institution_id = :t_i_id
"""

GET_TEST_RESULT_BY_ID = """
    SELECT * FROM "test_result" WHERE test_result_id = :test_result_id
"""

UPDATE_TEST_RESULT = """
    UPDATE "test_result"
    SET 
        subject_name=:subject_name,
        test_status=:test_status,
        test_language=:test_language,
        dpa_level=:dpa_level,
        ball_100=:ball_100,
        ball_12=:ball_12,
        ball=:ball,
        adapt_scale=:adapt_scale,
        year_of_attempt=:year_of_attempt
    WHERE test_result_id = :test_result_id
"""
