DO $$

	DECLARE
		-- to iterate though original table
		zno_row RECORD;

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

		FOR zno_row IN
		SELECT * FROM zno
		LOOP
			-- raw location info (person)
			INSERT INTO location_info
				(region_name, area_name, territory_name)
			VALUES
				(zno_row.regname, zno_row.areaname, zno_row.tername)
			RETURNING location_info_id
			INTO _raw_location_info_id;

			-- aggregating person location info
			INSERT INTO person_location_info
				(person_location_type, location_info_id)
			VALUES
				(zno_row.tertypename, _raw_location_info_id)
			RETURNING person_location_info.person_location_info_id
			INTO _person_location_info_id;

			-- learning profile
			IF (zno_row.classprofilename IS NOT NULL) THEN
				INSERT INTO learning_profile
					(learning_profile_name, learning_profile_language)
				VALUES
					(zno_row.classprofilename, zno_row.classlangname)
				RETURNING learning_profile.learning_profile_id
				INTO _learning_profile_id;
			ELSE
				_learning_profile_id := NULL;
			END IF;

			-- aggregating educational institution
			if (zno_row.eoname IS NOT NULL) THEN
				-- location info
				INSERT INTO location_info
					(region_name, area_name, territory_name)
				VALUES
					(zno_row.eoregname, zno_row.eoareaname, zno_row.eotername)
				RETURNING location_info_id
				INTO _ei_location_info_id;
				-- institution
				INSERT INTO educational_institution
					(educational_institution_name,
					 educational_institution_parent,
					 educational_institution_type,
					 location_info_id)
				VALUES
					(zno_row.eoname,
					 zno_row.eoparent,
					 zno_row.eotypename,
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
				(zno_row.outid,
				 zno_row.birth, zno_row.regtypename, zno_row.sextypename,
				 _learning_profile_id, _ei_id, _person_location_info_id)
			RETURNING person_id
			INTO _person_id;

			-- aggregating ukr
			IF (zno_row.ukrtest IS NOT NULL) THEN
				-- location info
				INSERT INTO location_info
					(region_name, area_name, territory_name)
				VALUES
					(zno_row.ukrptregname, zno_row.ukrptareaname, zno_row.ukrpttername)
				RETURNING location_info_id
				INTO _location_info_id;
				-- test institution
				INSERT INTO test_institution
					(test_institution_name, location_info_id)
				VALUES
					(zno_row.ukrptname, _location_info_id)
				RETURNING test_institution_id
				INTO _test_institution_id;
				-- test result
				INSERT INTO test_result
					(subject_name,
					 test_status, test_language,
					 dpa_level, ball_100, ball_12, ball, adapt_scale,
					 year_of_attempt)
				VALUES
					(zno_row.ukrtest,
					 zno_row.ukrteststatus, NULL,
					 NULL, zno_row.ukrball100, zno_row.ukrball12, zno_row.ukrball, zno_row.ukradaptscale,
					 zno_row.yearofattempt)
				RETURNING test_result_id
				INTO _test_result_id;
				-- p_ti_tr
				INSERT INTO p_ti_tr
					(person_id, test_institution_id, test_result_id)
				VALUES
					(_person_id, _test_institution_id, _test_result_id);
			END IF;

			-- aggregating history
			IF (zno_row.histtest IS NOT NULL) THEN
				-- location info
				INSERT INTO location_info
					(region_name, area_name, territory_name)
				VALUES
					(zno_row.histptregname, zno_row.histptareaname, zno_row.histpttername)
				RETURNING location_info_id
				INTO _location_info_id;
				-- test institution
				INSERT INTO test_institution
					(test_institution_name, location_info_id)
				VALUES
					(zno_row.histptname, _location_info_id)
				RETURNING test_institution_id
				INTO _test_institution_id;
				-- test result
				INSERT INTO test_result
					(subject_name,
					 test_status, test_language,
					 dpa_level, ball_100, ball_12, ball, adapt_scale,
					 year_of_attempt)
				VALUES
					(zno_row.histtest,
					 zno_row.histteststatus, zno_row.histlang,
					 NULL, zno_row.histball100, zno_row.histball12, zno_row.histball, NULL,
					 zno_row.yearofattempt)
				RETURNING test_result_id
				INTO _test_result_id;
				-- p_ti_tr
				INSERT INTO p_ti_tr
					(person_id, test_institution_id, test_result_id)
				VALUES
					(_person_id, _test_institution_id, _test_result_id);
			END IF;

			-- aggregating math
			IF (zno_row.mathtest IS NOT NULL) THEN
				-- location info
				INSERT INTO location_info
					(region_name, area_name, territory_name)
				VALUES
					(zno_row.mathptregname, zno_row.mathptareaname, zno_row.mathpttername)
				RETURNING location_info_id
				INTO _location_info_id;
				-- test institution
				INSERT INTO test_institution
					(test_institution_name, location_info_id)
				VALUES
					(zno_row.mathptname, _location_info_id)
				RETURNING test_institution_id
				INTO _test_institution_id;
				-- test result
				INSERT INTO test_result
					(subject_name,
					 test_status, test_language,
					 dpa_level, ball_100, ball_12, ball, adapt_scale,
					 year_of_attempt)
				VALUES
					(zno_row.mathtest,
					 zno_row.mathteststatus, zno_row.mathlang,
					 NULL, zno_row.mathball100, zno_row.mathball12, zno_row.mathball, NULL,
					 zno_row.yearofattempt)
				RETURNING test_result_id
				INTO _test_result_id;
				-- p_ti_tr
				INSERT INTO p_ti_tr
					(person_id, test_institution_id, test_result_id)
				VALUES
					(_person_id, _test_institution_id, _test_result_id);
			END IF;

			-- aggregating physics
			IF (zno_row.phystest IS NOT NULL) THEN
				-- location info
				INSERT INTO location_info
					(region_name, area_name, territory_name)
				VALUES
					(zno_row.physptregname, zno_row.physptareaname, zno_row.physpttername)
				RETURNING location_info_id
				INTO _location_info_id;
				-- test institution
				INSERT INTO test_institution
					(test_institution_name, location_info_id)
				VALUES
					(zno_row.physptname, _location_info_id)
				RETURNING test_institution_id
				INTO _test_institution_id;
				-- test result
				INSERT INTO test_result
					(subject_name,
					 test_status, test_language,
					 dpa_level, ball_100, ball_12, ball, adapt_scale,
					 year_of_attempt)
				VALUES
					(zno_row.phystest,
					 zno_row.physteststatus, zno_row.physlang,
					 NULL, zno_row.physball100, zno_row.physball12, zno_row.physball, NULL,
					 zno_row.yearofattempt)
				RETURNING test_result_id
				INTO _test_result_id;
				-- p_ti_tr
				INSERT INTO p_ti_tr
					(person_id, test_institution_id, test_result_id)
				VALUES
					(_person_id, _test_institution_id, _test_result_id);
			END IF;

			-- aggregating chemistry
			IF (zno_row.chemtest IS NOT NULL) THEN
				-- location info
				INSERT INTO location_info
					(region_name, area_name, territory_name)
				VALUES
					(zno_row.chemptregname, zno_row.chemptareaname, zno_row.chempttername)
				RETURNING location_info_id
				INTO _location_info_id;
				-- test institution
				INSERT INTO test_institution
					(test_institution_name, location_info_id)
				VALUES
					(zno_row.chemptname, _location_info_id)
				RETURNING test_institution_id
				INTO _test_institution_id;
				-- test result
				INSERT INTO test_result
					(subject_name,
					 test_status, test_language,
					 dpa_level, ball_100, ball_12, ball, adapt_scale,
					 year_of_attempt)
				VALUES
					(zno_row.chemtest,
					 zno_row.chemteststatus, zno_row.chemlang,
					 NULL, zno_row.chemball100, zno_row.chemball12, zno_row.chemball, NULL,
					 zno_row.yearofattempt)
				RETURNING test_result_id
				INTO _test_result_id;
				-- p_ti_tr
				INSERT INTO p_ti_tr
					(person_id, test_institution_id, test_result_id)
				VALUES
					(_person_id, _test_institution_id, _test_result_id);
			END IF;

			-- aggregating biology
			IF (zno_row.biotest IS NOT NULL) THEN
				-- location info
				INSERT INTO location_info
					(region_name, area_name, territory_name)
				VALUES
					(zno_row.bioptregname, zno_row.bioptareaname, zno_row.biopttername)
				RETURNING location_info_id
				INTO _location_info_id;
				-- test institution
				INSERT INTO test_institution
					(test_institution_name, location_info_id)
				VALUES
					(zno_row.bioptname, _location_info_id)
				RETURNING test_institution_id
				INTO _test_institution_id;
				-- test result
				INSERT INTO test_result
					(subject_name,
					 test_status, test_language,
					 dpa_level, ball_100, ball_12, ball, adapt_scale,
					 year_of_attempt)
				VALUES
					(zno_row.biotest,
					 zno_row.bioteststatus, zno_row.biolang,
					 NULL, zno_row.bioball100, zno_row.bioball12, zno_row.bioball, NULL,
					 zno_row.yearofattempt)
				RETURNING test_result_id
				INTO _test_result_id;
				-- p_ti_tr
				INSERT INTO p_ti_tr
					(person_id, test_institution_id, test_result_id)
				VALUES
					(_person_id, _test_institution_id, _test_result_id);
			END IF;

			-- aggregating geography
			IF (zno_row.geotest IS NOT NULL) THEN
				-- location info
				INSERT INTO location_info
					(region_name, area_name, territory_name)
				VALUES
					(zno_row.geoptregname, zno_row.geoptareaname, zno_row.geopttername)
				RETURNING location_info_id
				INTO _location_info_id;
				-- test institution
				INSERT INTO test_institution
					(test_institution_name, location_info_id)
				VALUES
					(zno_row.geoptname, _location_info_id)
				RETURNING test_institution_id
				INTO _test_institution_id;
				-- test result
				INSERT INTO test_result
					(subject_name,
					 test_status, test_language,
					 dpa_level, ball_100, ball_12, ball, adapt_scale,
					 year_of_attempt)
				VALUES
					(zno_row.geotest,
					 zno_row.geoteststatus, zno_row.geolang,
					 NULL, zno_row.geoball100, zno_row.geoball12, zno_row.geoball, NULL,
					 zno_row.yearofattempt)
				RETURNING test_result_id
				INTO _test_result_id;
				-- p_ti_tr
				INSERT INTO p_ti_tr
					(person_id, test_institution_id, test_result_id)
				VALUES
					(_person_id, _test_institution_id, _test_result_id);
			END IF;

			-- aggregating english
			IF (zno_row.engtest IS NOT NULL) THEN
				-- location info
				INSERT INTO location_info
					(region_name, area_name, territory_name)
				VALUES
					(zno_row.engptregname, zno_row.engptareaname, zno_row.engpttername)
				RETURNING location_info_id
				INTO _location_info_id;
				-- test institution
				INSERT INTO test_institution
					(test_institution_name, location_info_id)
				VALUES
					(zno_row.engptname, _location_info_id)
				RETURNING test_institution_id
				INTO _test_institution_id;
				-- test result
				INSERT INTO test_result
					(subject_name,
					 test_status, test_language,
					 dpa_level, ball_100, ball_12, ball, adapt_scale,
					 year_of_attempt)
				VALUES
					(zno_row.engtest,
					 zno_row.engteststatus, NULL,
					 zno_row.engdpalevel, zno_row.geoball100, zno_row.geoball12, zno_row.geoball, NULL,
					 zno_row.yearofattempt)
				RETURNING test_result_id
				INTO _test_result_id;
				-- p_ti_tr
				INSERT INTO p_ti_tr
					(person_id, test_institution_id, test_result_id)
				VALUES
					(_person_id, _test_institution_id, _test_result_id);
			END IF;

			-- aggregating french
			IF (zno_row.fratest IS NOT NULL) THEN
				-- location info
				INSERT INTO location_info
					(region_name, area_name, territory_name)
				VALUES
					(zno_row.fraptregname, zno_row.fraptareaname, zno_row.frapttername)
				RETURNING location_info_id
				INTO _location_info_id;
				-- test institution
				INSERT INTO test_institution
					(test_institution_name, location_info_id)
				VALUES
					(zno_row.fraptname, _location_info_id)
				RETURNING test_institution_id
				INTO _test_institution_id;
				-- test result
				INSERT INTO test_result
					(subject_name,
					 test_status, test_language,
					 dpa_level, ball_100, ball_12, ball, adapt_scale,
					 year_of_attempt)
				VALUES
					(zno_row.fratest,
					 zno_row.frateststatus, NULL,
					 zno_row.fradpalevel, zno_row.fraball100, zno_row.fraball12, zno_row.fraball, NULL,
					 zno_row.yearofattempt)
				RETURNING test_result_id
				INTO _test_result_id;
				-- p_ti_tr
				INSERT INTO p_ti_tr
					(person_id, test_institution_id, test_result_id)
				VALUES
					(_person_id, _test_institution_id, _test_result_id);
			END IF;

			-- aggregating deu
			IF (zno_row.deutest IS NOT NULL) THEN
				-- location info
				INSERT INTO location_info
					(region_name, area_name, territory_name)
				VALUES
					(zno_row.deuptregname, zno_row.deuptareaname, zno_row.deupttername)
				RETURNING location_info_id
				INTO _location_info_id;
				-- test institution
				INSERT INTO test_institution
					(test_institution_name, location_info_id)
				VALUES
					(zno_row.deuptname, _location_info_id)
				RETURNING test_institution_id
				INTO _test_institution_id;
				-- test result
				INSERT INTO test_result
					(subject_name,
					 test_status, test_language,
					 dpa_level, ball_100, ball_12, ball, adapt_scale,
					 year_of_attempt)
				VALUES
					(zno_row.deutest,
					 zno_row.deuteststatus, NULL,
					 zno_row.deudpalevel, zno_row.deuball100, zno_row.deuball12, zno_row.deuball, NULL,
					 zno_row.yearofattempt)
				RETURNING test_result_id
				INTO _test_result_id;
				-- p_ti_tr
				INSERT INTO p_ti_tr
					(person_id, test_institution_id, test_result_id)
				VALUES
					(_person_id, _test_institution_id, _test_result_id);
			END IF;

			-- aggregating spanish
			IF (zno_row.spatest IS NOT NULL) THEN
				-- location info
				INSERT INTO location_info
					(region_name, area_name, territory_name)
				VALUES
					(zno_row.spaptregname, zno_row.spaptareaname, zno_row.spapttername)
				RETURNING location_info_id
				INTO _location_info_id;
				-- test institution
				INSERT INTO test_institution
					(test_institution_name, location_info_id)
				VALUES
					(zno_row.spaptname, _location_info_id)
				RETURNING test_institution_id
				INTO _test_institution_id;
				-- test result
				INSERT INTO test_result
					(subject_name,
					 test_status, test_language,
					 dpa_level, ball_100, ball_12, ball, adapt_scale,
					 year_of_attempt)
				VALUES
					(zno_row.spatest,
					 zno_row.spateststatus, NULL,
					 zno_row.spadpalevel, zno_row.spaball100, zno_row.spaball12, zno_row.spaball, NULL,
					 zno_row.yearofattempt)
				RETURNING test_result_id
				INTO _test_result_id;
				-- p_ti_tr
				INSERT INTO p_ti_tr
					(person_id, test_institution_id, test_result_id)
				VALUES
					(_person_id, _test_institution_id, _test_result_id);
			END IF;

		END LOOP;

	END;

$$ LANGUAGE plpgsql;
