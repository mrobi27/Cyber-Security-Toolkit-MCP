import logging
from typing import Dict, Any
from services.dns_service import resolve_dns_records
from models.responses import DNSResponse
from utils.validator import sanitize_domain

logger = logging.getLogger(__name__)

async def dns_lookup(domain: str) -> Dict[str, Any]:
    """
    Lookup DNS records (A, AAAA, MX, TXT, NS) for a domain.
    """
    try:
        clean_domain = sanitize_domain(domain)
        records = await resolve_dns_records(clean_domain)
        
        response = DNSResponse(
            success=True,
            target=clean_domain,
            **records
        )
        return response.model_dump()
        
    except ValueError as e:
        return DNSResponse(success=False, target=domain, error=str(e)).model_dump()
    except Exception as e:
        logger.error(f"DNS Error for {domain}: {str(e)}")
        return DNSResponse(success=False, target=domain, error="Failed to resolve DNS records").model_dump()
