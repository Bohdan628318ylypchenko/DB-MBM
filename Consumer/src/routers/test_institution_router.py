from fastapi import APIRouter, Depends
from src.db import get_db, DB, queries
from src.routers.models import LocationInfo, TestInstitution, GlimpseTestInstitution
from src.utils.error_handler import raise_exception
from loguru import logger


test_institution_router = APIRouter()


@test_institution_router.get("/test_institution/{t_i_id}")
def get_t_i_by_id(
    t_i_id: int,
    db: DB = Depends(get_db)
) -> TestInstitution:
    try:
        row = db.fetch_one(
            query=queries.GET_TEST_INSTITUTION,
            values={
                "t_i_id": t_i_id
            }
        )
        return TestInstitution(
            test_institution_id=row["test_institution_id"],
            test_institution_name=row["test_institution_name"],
            location_info=LocationInfo(
                location_info_id=row["location_info_id"],
                region_name=row["region_name"],
                area_name=row["area_name"],
                territory_name=row["territory_name"]
            )
        )
    except Exception as error:
        logger.error(error)
        raise_exception(exception=error)


@test_institution_router.get("/test_institution/{t_i_id}/glimpse")
def glimpse_t_i_id(
    t_i_id: int,
    db: DB = Depends(get_db)
) -> GlimpseTestInstitution:
    try:
        row = db.fetch_one(
            query=queries.GLIMPSE_TEST_INSTITUTION,
            values={
                "t_i_id": t_i_id
            }
        )
        return GlimpseTestInstitution.model_validate(row)
    except Exception as error:
        logger.error(error)
        raise_exception(exception=error)
