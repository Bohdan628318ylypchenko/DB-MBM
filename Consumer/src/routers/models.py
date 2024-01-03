from pydantic import BaseModel


class LocationInfo(BaseModel):
    location_info_id: int
    region_name: str
    area_name: str
    territory_name: str


class EducationalInstitution(BaseModel):
    educational_institution_id: int
    educational_institution_name: str | None
    educational_institution_parent: str | None
    educational_institution_type: str | None
    location_info: LocationInfo | None


class PersonLocationInfo(BaseModel):
    person_location_info_id: int
    person_location_type: str
    location_info: LocationInfo


class LearningProfile(BaseModel):
    learning_profile_id: int
    learning_profile_name: str
    learning_profile_language: str


class Person(BaseModel):
    person_id: int
    person_out_id: str
    birth: int
    registration_status: str
    sex_type: str
    learning_profile: LearningProfile
    educational_institution: EducationalInstitution
    person_location_info: PersonLocationInfo


class PersonGlimpse(BaseModel):
    person_id: int
    person_out_id: str
    birth: int
    registration_status: str
    sex_type: str
    learning_profile_id: int
    educational_institution_id: int
    person_location_info_id: int 


class TestResult(BaseModel):
    test_result_id: int
    subject_name: str | None
    test_status: str | None
    test_language: str | None
    dpa_level: str | None
    ball_100: float | None
    ball_12: float | None
    ball: int | None
    adapt_scale: int | None
    year_of_attempt: int | None


class GlimpseEducationalInstitution(BaseModel):
    educational_institution_id: int | None
    educational_institution_name: str | None
    educational_institution_parent: str | None
    educational_institution_type: str | None
    location_info_id: int | None


class TestInstitution(BaseModel):
    test_institution_id: int 
    test_institution_name: str | None
    location_info: LocationInfo


class GlimpseTestInstitution(BaseModel):
    test_institution_id: int
    test_institution_name: str | None
    location_info_id: int | None


class TestResultDTO(BaseModel):
    subject_name: str | None
    test_status: str | None
    test_language: str | None
    dpa_level: str | None
    ball_100: float | None
    ball_12: float | None
    ball: int | None
    adapt_scale: int | None
    year_of_attempt: int | None
