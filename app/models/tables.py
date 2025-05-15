from sqlalchemy import Column, String, DateTime, JSON
from app.models.database import Base

class VirusTotalRecord(Base):
    __tablename__ = "virustotal_records"

    id = Column(String, primary_key=True, index=True)
    data_type = Column(String)
    attributes = Column(JSON)
    last_fetched = Column(DateTime)

    @property
    def identifier(self):
        return self.id

    @property
    def type(self):
        return self.data_type

    @property
    def data(self):
        return self.attributes
