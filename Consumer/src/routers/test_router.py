from fastapi import APIRouter, Depends
from src.db import get_db, DB, queries 
from src.routers.models import TestResult, TestResultDTO
from src.utils.error_handler import raise_exception
from loguru import logger


test_result_router = APIRouter()


@test_result_router.get("/test_result/{test_result_id}")
def get_test_result_by_id(
    test_result_id: int,
    db: DB = Depends(get_db)
) -> TestResult:
    try:
        row = db.fetch_one(
            query=queries.GET_TEST_RESULT_BY_ID,
            values={
                "test_result_id": test_result_id
            }
        )
        return TestResult.model_validate(row)
    except Exception as error:
        logger.error(error)
        raise_exception(exception=error)


@test_result_router.post("/test_result/{test_result_id}")
def update_test_result(
    test_result_id: int,
    test_result_dto: TestResultDTO,
    db: DB = Depends(get_db)
) -> None:
    try:
        db.execute(
            query=queries.UPDATE_TEST_RESULT,
            values={
                "test_result_id": test_result_id,
                **test_result_dto.model_dump()
            }
        )
    except Exception as error:
        logger.error(error)
        raise_exception(exception=error)
