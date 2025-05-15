from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import schema, tables
from app.models.database import SessionLocal
from app.services.virustotal import fetch_virustotal_data
from app.utils.cache import get_cache, set_cache
from datetime import datetime
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/lookup/{identifier}", response_model=schema.VTRecord)
def lookup(identifier: str, db: Session = Depends(get_db)):
    # Check cache first
    cached = get_cache(identifier)
    if cached:
        return schema.VTRecord(
            identifier=cached.id,
            type=cached.data_type,
            data=cached.attributes
        )

    # Check DB
    record = db.query(tables.VirusTotalRecord).filter(tables.VirusTotalRecord.id == identifier).first()
    if record:
        set_cache(identifier, record)
        return schema.VTRecord(
            identifier=record.id,
            type=record.data_type,
            data=record.attributes
        )

    # Fetch from API
    data = fetch_virustotal_data(identifier)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")

    new_record = tables.VirusTotalRecord(
        id=data['id'],
        data_type=data['type'],
        attributes=data['attributes'],
        last_fetched=datetime.utcnow()
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    set_cache(identifier, new_record)

    return schema.VTRecord(
        identifier=new_record.id,
        type=new_record.data_type,
        data=new_record.attributes
    )


@router.get("/refresh/{identifier}", response_model=schema.VTRecord)
def refresh(identifier: str, db: Session = Depends(get_db)):
    data = fetch_virustotal_data(identifier)
    if not data:
        raise HTTPException(status_code=404, detail="Unable to refresh data")

    record = db.query(tables.VirusTotalRecord).filter(tables.VirusTotalRecord.id == identifier).first()
    if record:
        record.data_type = data['type']
        record.attributes = data['attributes']
        record.last_fetched = datetime.utcnow()
    else:
        record = tables.VirusTotalRecord(
            id=data['id'],
            data_type=data['type'],
            attributes=data['attributes'],
            last_fetched=datetime.utcnow()
        )
        db.add(record)
    db.commit()
    set_cache(identifier, record)

    return schema.VTRecord(
        identifier=record.id,
        type=record.data_type,
        data=record.attributes
    )
