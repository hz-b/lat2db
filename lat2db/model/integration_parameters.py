from pydantic import BaseModel


class IntegrationParameters(BaseModel):
    steps:  int
    order : int