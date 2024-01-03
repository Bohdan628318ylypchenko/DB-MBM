from fastapi import APIRouter, Depends
from src.db import get_db, DB, queries
from src.utils.error_handler import raise_exception
from .models import EducationalInstitution, LearningProfile, LocationInfo, Person, PersonGlimpse, PersonLocationInfo, TestResult
from loguru import logger


person_router = APIRouter()


@person_router.get("/person/glimpse")
def glimpse_person_by_out_id(
    person_out_id: str,
    db: DB =  Depends(get_db)
) -> PersonGlimpse:
    try:
        row = db.fetch_one(
            query=queries.GLIMPSE_PERSON_BY_OUT_ID,
            values={
                "person_out_id": person_out_id
            }
        )
        return PersonGlimpse.model_validate(row)
    except Exception as error:
        logger.error(error)
        raise_exception(exception=error)


@person_router.get("/person/glimpse/{person_id}")
def glimpse_person_by__id(
    person_id: str,
    db: DB =  Depends(get_db)
) -> PersonGlimpse:
    try:
        row = db.fetch_one(
            query=queries.GLIMPSE_PERSON_BY_ID,
            values={
                "person_id": person_id
            }
        )
        return PersonGlimpse.model_validate(row)
    except Exception as error:
        logger.error(error)
        raise_exception(exception=error)


@person_router.get("/person")
def get_by_out_id(
    person_out_id: str,
    db: DB =  Depends(get_db)
) -> Person:
    try:
        row = db.fetch_one(
            query=queries.GET_PERSON_BY_OUT_ID,
            values={
                "person_out_id": person_out_id
            }
        )
        return Person(
            person_id=row["person_id"],
            person_out_id=row["person_out_id"],
            birth=row["birth"],
            registration_status=row["registration_status"],
            sex_type=row["sex_type"],
            learning_profile=LearningProfile(
                learning_profile_id=row["learning_profile_id"],
                learning_profile_name=row["learning_profile_name"],
                learning_profile_language=row["learning_profile_language"]
            ),
            educational_institution=EducationalInstitution(
                educational_institution_id=row["educational_institution_id"],
                educational_institution_name=row["educational_institution_name"],
                educational_institution_parent=row["educational_institution_parent"],
                educational_institution_type=row["educational_institution_type"],
                location_info=LocationInfo(
                    location_info_id=row["edi_li_location_info_id"],
                    region_name=row["edi_li_region_name"],
                    area_name=row["edi_li_area_name"],
                    territory_name=row["edi_li_territory_name"]
                )
            ),
            person_location_info=PersonLocationInfo(
                person_location_info_id=row["person_location_info_id"],
                person_location_type=row["person_location_type"],
                location_info=LocationInfo(
                    location_info_id=row["pli_li_location_info_id"],
                    region_name=row["pli_li_region_name"],
                    area_name=row["pli_li_area_name"],
                    territory_name=row["pli_li_territory_name"]
                )
            )
        )
    except Exception as error:
        logger.error(error)
        raise_exception(exception=error)


@person_router.get("/person/tests")
def get_test_results_by_out_id(
    person_out_id: str,
    db: DB =  Depends(get_db)
) -> list[TestResult]:
    try:
        rows = db.fetch_all(
            query=queries.GET_TEST_RESULTS_BY_OUT_ID,
            values={
                "person_out_id": person_out_id
            }
        )
        return [TestResult.model_validate(row) for row in rows] # type: ignore
    except Exception as error:
        logger.error(error)
        raise_exception(exception=error)
