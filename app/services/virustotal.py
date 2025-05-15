import httpx
from app.config import VT_API_KEY

def fetch_virustotal_data(identifier: str):
    base_url = "https://www.virustotal.com/api/v3/"
    if "." in identifier:
        url = f"{base_url}domains/{identifier}"
    elif len(identifier) == 64:
        url = f"{base_url}files/{identifier}"
    else:
        url = f"{base_url}ip_addresses/{identifier}"

    headers = {"x-apikey": VT_API_KEY}
    response = httpx.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("data")
    return None