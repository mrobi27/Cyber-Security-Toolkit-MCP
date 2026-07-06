import httpx
from typing import Dict, Any, List
from utils.constants import RDAP_BOOTSTRAP_URL, DEFAULT_TIMEOUT

async def get_rdap_data(domain: str) -> Dict[str, Any]:
    """
    Fetch RDAP data for a given domain using async httpx.
    """
    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        url = f"{RDAP_BOOTSTRAP_URL}{domain}"
        
        try:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Domain '{domain}' not found in RDAP.")
            raise Exception(f"HTTP error occurred: {e}")
        except httpx.RequestError as e:
            raise Exception(f"Request error occurred: {e}")

def parse_rdap_response(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse the raw RDAP JSON into a structured dictionary for our model.
    """
    parsed = {
        "registrar": None,
        "creation_date": None,
        "expiration_date": None,
        "name_servers": [],
        "status": []
    }
    
    entities = raw_data.get("entities", [])
    for entity in entities:
        roles = entity.get("roles", [])
        if "registrar" in roles:
            vcard = entity.get("vcardArray", [])
            if len(vcard) > 1:
                for item in vcard[1]:
                    if item[0] == "fn":
                        parsed["registrar"] = item[3]
                        break

    events = raw_data.get("events", [])
    for event in events:
        action = event.get("eventAction")
        date = event.get("eventDate")
        if action == "registration":
            parsed["creation_date"] = date
        elif action == "expiration":
            parsed["expiration_date"] = date
            
    nameservers = raw_data.get("nameservers", [])
    for ns in nameservers:
        parsed["name_servers"].append(ns.get("ldhName"))
        
    parsed["status"] = raw_data.get("status", [])
    
    return parsed
