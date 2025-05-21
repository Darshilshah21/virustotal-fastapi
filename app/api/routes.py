# app/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.tables import VirusTotalRecord
from app.services.virustotal import fetch_from_api
from app.utils.cache import get_from_cache, set_in_cache, invalidate_cache

router = APIRouter()

@router.get("/lookup/{identifier}")
def lookup_data(identifier: str, db: Session = Depends(get_db)):
    # ✅ Step 1: Check cache
    cached = get_from_cache(identifier)
    if cached:
        return {"source": "cache", "identifier": identifier, "data": cached}

    # ✅ Step 2: Check DB
    entry = db.query(VirusTotalRecord).filter(VirusTotalRecord.identifier == identifier).first()
    if entry:
        set_in_cache(identifier, entry.data)  # ✅ Step 3: Add to cache
        return {"source": "db", "identifier": identifier, "data": entry.data}

    raise HTTPException(status_code=404, detail="Identifier not found")

@router.get("/refresh/{identifier}")
def refresh_data(identifier: str, db: Session = Depends(get_db)):
    if not identifier:
        raise HTTPException(status_code=400, detail="Invalid identifier")

    # ✅ Step 1: Fetch new data from VirusTotal
    new_data = fetch_from_api(identifier)
    if not new_data:
        raise HTTPException(status_code=500, detail="Failed to fetch data from VirusTotal")

    # ✅ Step 2: Update DB
    entry = db.query(VirusTotalRecord).filter_by(identifier=identifier).first()
    if entry:
        entry.data = new_data
    else:
        entry = VirusTotalRecord(identifier=identifier, data=new_data)
        db.add(entry)
    db.commit()

    # ✅ Step 3: Update cache
    invalidate_cache(identifier)
    set_in_cache(identifier, new_data)

    return {"message": "Refreshed from VirusTotal", "identifier": identifier}
