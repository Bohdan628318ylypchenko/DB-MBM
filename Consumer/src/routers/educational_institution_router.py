from fastapi import APIRouter, Depends
from src.db import get_db, DB, queries
from src.routers.models import GlimpseEducationalInstitution, EducationalInstitution, LocationInfo
from src.utils.error_handler import raise_exception
from loguru import logger


educational_institution_router = APIRouter()


@educational_institution_router.get("/educational_institution/{e_i_id}")
def get_e_i_by_id(
    e_i_id: int,
    db: DB = Depends(get_db)
) -> EducationalInstitution:
    try:
        row = db.fetch_one(
            query=queries.GET_EDUCATIONAL_INSTITUTION,
            values={
                "e_i_id": e_i_id
            }
        )
        return EducationalInstitution(
            educational_institution_id=row["educational_institution_id"],
            educational_institution_name=row["educational_institution_name"],
            educational_institution_parent=row["educational_institution_parent"],
            educational_institution_type=row["educational_institution_type"],
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



@educational_institution_router.get("/educational_institution/{e_i_id}/glimpse")
def glimpse_e_i_by_id(
    e_i_id: int,
    db: DB = Depends(get_db)
) -> GlimpseEducationalInstitution:
    try:
        row = db.fetch_one(
            query=queries.GLIMPSE_EDUCATIONAL_INSTITUTION,
            values={
                "e_i_id": e_i_id
            }
        )
        return GlimpseEducationalInstitution.model_validate(row)
    except Exception as error:
        logger.error(error)
        raise_exception(exception=error)
