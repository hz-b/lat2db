from typing import Optional

from pydantic import BaseModel


class IntegrationParameters(BaseModel):
    n_steps: Optional[int] = -1
    max_order: Optional[int] = -1
