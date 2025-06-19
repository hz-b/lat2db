from pydantic import BaseModel


class IntegrationParameters(BaseModel):
    n_slices:  int
    symplectic_order : int