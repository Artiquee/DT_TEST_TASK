from pydantic import BaseModel


class SpySchema(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float
    secret_access_key: str = None


class SpySchemaUpdate(BaseModel):
    name: str
    salary: float
    secret_access_key: str


class AllCatsSchema(BaseModel):
    name: str
    years_of_experience: int
    breed: str
    salary: float
