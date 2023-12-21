GET_SERVICE_WORKER_STATUS = """
SELECT * FROM service_worker_status;
"""

GET_ZNO = """
SELECT * FROM zno
ORDER BY id
OFFSET :n ROWS
"""

INCREMENT_COMPLETED_TRANSACTION_COUNT = """
UPDATE service_worker_status
SET completed_transaction_count = completed_transaction_count + 1
"""

SET_SERVICE_WORKER_STATUS_DONE = """
UPDATE service_worker_status
SET is_done = TRUE
"""

GET_COMPLETED_TX_COUNT = """
SELECT completed_transaction_count FROM service_worker_status
"""

NOTHING_IS_MORE_CONSTANT_THAN_TEMPORARY = """
DO $$

DECLARE
    -- person aggregation
    _raw_location_info_id BIGINT;
    _person_location_info_id BIGINT;
    _learning_profile_id BIGINT;
    _ei_location_info_id BIGINT;
    _ei_id BIGINT;
    _person_id BIGINT;

    -- p_ti_tr aggregation (same vars for all)
    _location_info_id BIGINT;
    _test_institution_id BIGINT;
    _test_result_id BIGINT;

BEGIN
    -- raw location info (person)
    INSERT INTO location_info
        (region_name, area_name, territory_name)
    VALUES
        (:regname, :areaname, :tername)
    RETURNING location_info_id
    INTO _raw_location_info_id;

    -- aggregating person location info
    INSERT INTO person_location_info
        (person_location_type, location_info_id)
    VALUES
        (:tertypename, _raw_location_info_id)
    RETURNING person_location_info.person_location_info_id
    INTO _person_location_info_id;

    -- learning profile
    IF (:classprofilename IS NOT NULL) THEN
        INSERT INTO learning_profile
            (learning_profile_name, learning_profile_language)
        VALUES
            (:classprofilename, :classlangname)
        RETURNING learning_profile.learning_profile_id
        INTO _learning_profile_id;
    ELSE
        _learning_profile_id := NULL;
    END IF;

    -- aggregating educational institution
    if (:eoname IS NOT NULL) THEN
        -- location info
        INSERT INTO location_info
            (region_name, area_name, territory_name)
        VALUES
            (:eoregname, :eoareaname, :eotertypename)
        RETURNING location_info_id
        INTO _ei_location_info_id;
        -- institution
        INSERT INTO educational_institution
            (educational_institution_name,
             educational_institution_parent,
             educational_institution_type,
             location_info_id)
        VALUES
            (:eoname,
             :eoparent,
             :eotypename,
             _ei_location_info_id)
        RETURNING educational_institution_id
        INTO _ei_id;
    ELSE
        _ei_id := NULL;
    END IF;

    -- aggregating person
    INSERT INTO person
        (person_out_id,
         birth, registration_status, sex_type,
         learning_profile_id, educational_institution_id, person_location_info_id)
    VALUES
        (:out_id,
         :birth, :regtypename, :sextypename,
         _learning_profile_id, _ei_id, _person_location_info_id)
    RETURNING person_id
    INTO _person_id;

    -- aggregating ukr
    IF (:ukr_test IS NOT NULL) THEN
        -- location info
        INSERT INTO location_info
            (region_name, area_name, territory_name)
        VALUES
            (:ukr_pt_reg_name, :ukr_pt_area_name, :ukr_pt_ter_name)
        RETURNING location_info_id
        INTO _location_info_id;
        -- test institution
        INSERT INTO test_institution
            (test_institution_name, location_info_id)
        VALUES
            (:ukr_pt_name, _location_info_id)
        RETURNING test_institution_id
        INTO _test_institution_id;
        -- test result
        INSERT INTO test_result
            (subject_name,
             test_status, test_language,
             dpa_level, ball_100, ball_12, ball, adapt_scale,
             year_of_attempt)
        VALUES
            (:ukr_test,
             :ukr_test_status, NULL,
             NULL, :ukr_ball100, :ukr_ball12, :ukr_ball, :ukr_adapt_scale,
             :year_of_attempt)
        RETURNING test_result_id
        INTO _test_result_id;
        -- p_ti_tr
        INSERT INTO p_ti_tr
            (person_id, test_institution_id, test_result_id)
        VALUES
            (_person_id, _test_institution_id, _test_result_id);
    END IF;

    -- aggregating history
    IF (:hist_test IS NOT NULL) THEN
        -- location info
        INSERT INTO location_info
            (region_name, area_name, territory_name)
        VALUES
            (:hist_pt_reg_name, :hist_pt_area_name, :hist_pt_ter_name)
        RETURNING location_info_id
        INTO _location_info_id;
        -- test institution
        INSERT INTO test_institution
            (test_institution_name, location_info_id)
        VALUES
            (:hist_pt_name, _location_info_id)
        RETURNING test_institution_id
        INTO _test_institution_id;
        -- test result
        INSERT INTO test_result
            (subject_name,
             test_status, test_language,
             dpa_level, ball_100, ball_12, ball, adapt_scale,
             year_of_attempt)
        VALUES
            (:hist_test,
             :hist_test_status, :hist_lang,
             NULL, :hist_ball100, :hist_ball12, :hist_ball, NULL,
             :year_of_attempt)
        RETURNING test_result_id
        INTO _test_result_id;
        -- p_ti_tr
        INSERT INTO p_ti_tr
            (person_id, test_institution_id, test_result_id)
        VALUES
            (_person_id, _test_institution_id, _test_result_id);
    END IF;

    -- aggregating math
    IF (:math_test IS NOT NULL) THEN
        -- location info
        INSERT INTO location_info
            (region_name, area_name, territory_name)
        VALUES
            (:math_pt_reg_name, :math_pt_area_name, :math_pt_ter_name)
        RETURNING location_info_id
        INTO _location_info_id;
        -- test institution
        INSERT INTO test_institution
            (test_institution_name, location_info_id)
        VALUES
            (:math_pt_name, _location_info_id)
        RETURNING test_institution_id
        INTO _test_institution_id;
        -- test result
        INSERT INTO test_result
            (subject_name,
             test_status, test_language,
             dpa_level, ball_100, ball_12, ball, adapt_scale,
             year_of_attempt)
        VALUES
            (:math_test,
             :math_test_status, :math_lang,
             NULL, :math_ball100, :math_ball12, :math_ball, NULL,
             :year_of_attempt)
        RETURNING test_result_id
        INTO _test_result_id;
        -- p_ti_tr
        INSERT INTO p_ti_tr
            (person_id, test_institution_id, test_result_id)
        VALUES
            (_person_id, _test_institution_id, _test_result_id);
    END IF;

    -- aggregating physics
    IF (:phys_test IS NOT NULL) THEN
        -- location info
        INSERT INTO location_info
            (region_name, area_name, territory_name)
        VALUES
            (:phys_pt_reg_name, :phys_pt_area_name, :phys_pt_ter_name)
        RETURNING location_info_id
        INTO _location_info_id;
        -- test institution
        INSERT INTO test_institution
            (test_institution_name, location_info_id)
        VALUES
            (:phys_pt_name, _location_info_id)
        RETURNING test_institution_id
        INTO _test_institution_id;
        -- test result
        INSERT INTO test_result
            (subject_name,
             test_status, test_language,
             dpa_level, ball_100, ball_12, ball, adapt_scale,
             year_of_attempt)
        VALUES
            (:phys_test,
             :phys_test_status, :phys_lang,
             NULL, :phys_ball100, :phys_ball12, :phys_ball, NULL,
             :year_of_attempt)
        RETURNING test_result_id
        INTO _test_result_id;
        -- p_ti_tr
        INSERT INTO p_ti_tr
            (person_id, test_institution_id, test_result_id)
        VALUES
            (_person_id, _test_institution_id, _test_result_id);
    END IF;

    -- aggregating chemistry
    IF (:chem_test IS NOT NULL) THEN
        -- location info
        INSERT INTO location_info
            (region_name, area_name, territory_name)
        VALUES
            (:chem_pt_reg_name, :chem_pt_area_name, :chem_pt_ter_name)
        RETURNING location_info_id
        INTO _location_info_id;
        -- test institution
        INSERT INTO test_institution
            (test_institution_name, location_info_id)
        VALUES
            (:chem_pt_name, _location_info_id)
        RETURNING test_institution_id
        INTO _test_institution_id;
        -- test result
        INSERT INTO test_result
            (subject_name,
             test_status, test_language,
             dpa_level, ball_100, ball_12, ball, adapt_scale,
             year_of_attempt)
        VALUES
            (:chem_test,
             :chem_test_status, :chem_lang,
             NULL, :chem_ball100, :chem_ball12, :chem_ball, NULL,
             :year_of_attempt)
        RETURNING test_result_id
        INTO _test_result_id;
        -- p_ti_tr
        INSERT INTO p_ti_tr
            (person_id, test_institution_id, test_result_id)
        VALUES
            (_person_id, _test_institution_id, _test_result_id);
    END IF;

    -- aggregating biology
    IF (:bio_test IS NOT NULL) THEN
        -- location info
        INSERT INTO location_info
            (region_name, area_name, territory_name)
        VALUES
            (:bio_pt_reg_name, :bio_pt_area_name, :bio_pt_ter_name)
        RETURNING location_info_id
        INTO _location_info_id;
        -- test institution
        INSERT INTO test_institution
            (test_institution_name, location_info_id)
        VALUES
            (:bio_pt_name, _location_info_id)
        RETURNING test_institution_id
        INTO _test_institution_id;
        -- test result
        INSERT INTO test_result
            (subject_name,
             test_status, test_language,
             dpa_level, ball_100, ball_12, ball, adapt_scale,
             year_of_attempt)
        VALUES
            (:bio_test,
             :bio_test_status, :bio_lang,
             NULL, :bio_ball100, :bio_ball12, :bio_ball, NULL,
             :year_of_attempt)
        RETURNING test_result_id
        INTO _test_result_id;
        -- p_ti_tr
        INSERT INTO p_ti_tr
            (person_id, test_institution_id, test_result_id)
        VALUES
            (_person_id, _test_institution_id, _test_result_id);
    END IF;

    -- aggregating geography
    IF (:geo_test IS NOT NULL) THEN
        -- location info
        INSERT INTO location_info
            (region_name, area_name, territory_name)
        VALUES
            (:geo_pt_reg_name, :geo_pt_area_name, :geo_pt_ter_name)
        RETURNING location_info_id
        INTO _location_info_id;
        -- test institution
        INSERT INTO test_institution
            (test_institution_name, location_info_id)
        VALUES
            (:geo_pt_name, _location_info_id)
        RETURNING test_institution_id
        INTO _test_institution_id;
        -- test result
        INSERT INTO test_result
            (subject_name,
             test_status, test_language,
             dpa_level, ball_100, ball_12, ball, adapt_scale,
             year_of_attempt)
        VALUES
            (:geo_test,
             :geo_test_status, :geo_lang,
             NULL, :geo_ball100, :geo_ball12, :geo_ball, NULL,
             :year_of_attempt)
        RETURNING test_result_id
        INTO _test_result_id;
        -- p_ti_tr
        INSERT INTO p_ti_tr
            (person_id, test_institution_id, test_result_id)
        VALUES
            (_person_id, _test_institution_id, _test_result_id);
    END IF;

    -- aggregating english
    IF (:eng_test IS NOT NULL) THEN
        -- location info
        INSERT INTO location_info
            (region_name, area_name, territory_name)
        VALUES
            (:eng_pt_reg_name, :eng_pt_area_name, :eng_pt_ter_name)
        RETURNING location_info_id
        INTO _location_info_id;
        -- test institution
        INSERT INTO test_institution
            (test_institution_name, location_info_id)
        VALUES
            (:eng_pt_name, _location_info_id)
        RETURNING test_institution_id
        INTO _test_institution_id;
        -- test result
        INSERT INTO test_result
            (subject_name,
             test_status, test_language,
             dpa_level, ball_100, ball_12, ball, adapt_scale,
             year_of_attempt)
        VALUES
            (:eng_test,
             :eng_test_status, NULL,
             :eng_dpa_level, :geo_ball100, :geo_ball12, :geo_ball, NULL,
             :year_of_attempt)
        RETURNING test_result_id
        INTO _test_result_id;
        -- p_ti_tr
        INSERT INTO p_ti_tr
            (person_id, test_institution_id, test_result_id)
        VALUES
            (_person_id, _test_institution_id, _test_result_id);
    END IF;

    -- aggregating french
    IF (:fra_test IS NOT NULL) THEN
        -- location info
        INSERT INTO location_info
            (region_name, area_name, territory_name)
        VALUES
            (:fra_pt_reg_name, :fra_pt_area_name, :fra_pt_ter_name)
        RETURNING location_info_id
        INTO _location_info_id;
        -- test institution
        INSERT INTO test_institution
            (test_institution_name, location_info_id)
        VALUES
            (:fra_pt_name, _location_info_id)
        RETURNING test_institution_id
        INTO _test_institution_id;
        -- test result
        INSERT INTO test_result
            (subject_name,
             test_status, test_language,
             dpa_level, ball_100, ball_12, ball, adapt_scale,
             year_of_attempt)
        VALUES
            (:fra_test,
             :fra_test_status, NULL,
             :fra_dpa_level, :fra_ball100, :fra_ball12, :fra_ball, NULL,
             :year_of_attempt)
        RETURNING test_result_id
        INTO _test_result_id;
        -- p_ti_tr
        INSERT INTO p_ti_tr
            (person_id, test_institution_id, test_result_id)
        VALUES
            (_person_id, _test_institution_id, _test_result_id);
    END IF;

    -- aggregating deu
    IF (:deu_test IS NOT NULL) THEN
        -- location info
        INSERT INTO location_info
            (region_name, area_name, territory_name)
        VALUES
            (:deu_pt_reg_name, :deu_pt_area_name, :deu_pt_ter_name)
        RETURNING location_info_id
        INTO _location_info_id;
        -- test institution
        INSERT INTO test_institution
            (test_institution_name, location_info_id)
        VALUES
            (:deu_pt_name, _location_info_id)
        RETURNING test_institution_id
        INTO _test_institution_id;
        -- test result
        INSERT INTO test_result
            (subject_name,
             test_status, test_language,
             dpa_level, ball_100, ball_12, ball, adapt_scale,
             year_of_attempt)
        VALUES
            (:deu_test,
             :deu_test_status, NULL,
             :deu_dpa_level, :deu_ball100, :deu_ball12, :deu_ball, NULL,
             :year_of_attempt)
        RETURNING test_result_id
        INTO _test_result_id;
        -- p_ti_tr
        INSERT INTO p_ti_tr
            (person_id, test_institution_id, test_result_id)
        VALUES
            (_person_id, _test_institution_id, _test_result_id);
    END IF;

    -- aggregating spanish
    IF (:spa_test IS NOT NULL) THEN
        -- location info
        INSERT INTO location_info
            (region_name, area_name, territory_name)
        VALUES
            (:spa_pt_reg_name, :spa_pt_area_name, :spa_pt_ter_name)
        RETURNING location_info_id
        INTO _location_info_id;
        -- test institution
        INSERT INTO test_institution
            (test_institution_name, location_info_id)
        VALUES
            (:spa_pt_name, _location_info_id)
        RETURNING test_institution_id
        INTO _test_institution_id;
        -- test result
        INSERT INTO test_result
            (subject_name,
             test_status, test_language,
             dpa_level, ball_100, ball_12, ball, adapt_scale,
             year_of_attempt)
        VALUES
            (:spa_test,
             :spa_test_status, NULL,
             :spa_dpa_level, :spa_ball100, :spa_ball12, :spa_ball, NULL,
             :year_of_attempt)
        RETURNING test_result_id
        INTO _test_result_id;
        -- p_ti_tr
        INSERT INTO p_ti_tr
            (person_id, test_institution_id, test_result_id)
        VALUES
            (_person_id, _test_institution_id, _test_result_id);
    END IF;

END;

$$ LANGUAGE plpgsql;
"""
