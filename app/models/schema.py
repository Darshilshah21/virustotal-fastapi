# from pydantic import BaseModel
# from datetime import datetime

from pydantic import BaseModel, ConfigDict

class VTRecord(BaseModel):
    identifier: str
    type: str
    data: dict

    model_config = ConfigDict(from_attributes=True)

# class VTRecord(BaseModel):
#     identifier: str
#     type: str
#     data: dict
#     last_fetched: datetime   # ✅ Use datetime, not str

#     class Config:
#         orm_mode = True
#         json_encoders = {
#             datetime: lambda v: v.isoformat()
#         }
