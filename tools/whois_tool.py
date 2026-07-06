import logging
from typing import Dict, Any
from services.rdap_service import get_rdap_data, parse_rdap_response
from models.responses import RDAPResponse
from utils.validator import sanitize_domain

logger = logging.getLogger(__name__)

async def whois_lookup(domain: str) -> Dict[str, Any]:
    """
    Lookup WHOIS/RDAP information of a domain.
    """
    try:
        clean_domain = sanitize_domain(domain)
        raw_data = await get_rdap_data(clean_domain)
        parsed = parse_rdap_response(raw_data)
        
        response = RDAPResponse(
            success=True,
            target=clean_domain,
            registrar=parsed["registrar"],
            creation_date=parsed["creation_date"],
            expiration_date=parsed["expiration_date"],
            name_servers=parsed["name_servers"],
            status=parsed["status"],
            raw_data=raw_data
        )
        return response.model_dump()
        
    except ValueError as e:
        return RDAPResponse(success=False, target=domain, error=str(e)).model_dump()
    except Exception as e:
        logger.error(f"RDAP Error for {domain}: {str(e)}")
        return RDAPResponse(success=False, target=domain, error="Failed to fetch RDAP data").model_dump()