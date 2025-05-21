

from pydantic import BaseModel, ConfigDict

class VTRecord(BaseModel):
    identifier: str
    type: str
    data: dict

    model_config = ConfigDict(from_attributes=True)

