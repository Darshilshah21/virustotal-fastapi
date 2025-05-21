from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from app.models.database import Base

class VirusTotalRecord(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, unique=True, index=True)
    data_type = Column(String)
    attributes = Column(Text)
    last_fetched = Column(DateTime, default=datetime.utcnow)
    data = Column(JSON)
