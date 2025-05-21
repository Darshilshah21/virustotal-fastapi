import requests
import json
from datetime import datetime
from app.models.tables import VirusTotalRecord

API_KEY = "YOUR_VIRUSTOTAL_API_KEY"
BASE_URL = "https://www.virustotal.com/api/v3/"

def detect_type(identifier: str):
    if "." in identifier and not identifier.replace(".", "").isdigit():
        return "domain"
    elif identifier.replace(".", "").isdigit():
        return "ip"
    else:
        return "file"

def fetch_from_api(identifier: str):
    id_type = detect_type(identifier)
    url = f"{BASE_URL}{id_type}s/{identifier}"
    headers = {"x-apikey": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return id_type, response.json()
    return None, None

def fetch_and_save(identifier: str, db):
    id_type, json_data = fetch_from_api(identifier)
    if not json_data:
        return False

    attributes = json.dumps(json_data.get("data", {}).get("attributes", {}))
    record = db.query(VirusTotalRecord).filter_by(identifier=identifier).first()

    if record:
        record.attributes = attributes
        record.last_fetched = datetime.utcnow()
    else:
        record = VirusTotalRecord(
            identifier=identifier,
            data_type=id_type,
            attributes=attributes,
            last_fetched=datetime.utcnow()
        )
        db.add(record)
    db.commit()
    return True
