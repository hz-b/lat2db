from typing import Optional

from pydantic import BaseModel


class MachineUpdate(BaseModel):
    name: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "MLS",
            }
        }
