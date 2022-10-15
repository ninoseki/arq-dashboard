import humps
from pydantic import BaseModel


class APIModel(BaseModel):
    class Config:
        alias_generator = humps.camelize
        allow_population_by_field_name = True
