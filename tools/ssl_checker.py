import logging
from typing import Dict, Any
from services.ssl_service import get_ssl_certificate
from models.responses import SSLResponse
from utils.validator import sanitize_domain

logger = logging.getLogger(__name__)

async def ssl_check(domain: str) -> Dict[str, Any]:
    """
    Check and parse SSL/TLS certificate for a domain.
    """
    try:
        clean_domain = sanitize_domain(domain)
        cert_data = await get_ssl_certificate(clean_domain)
        
        response = SSLResponse(
            success=True,
            target=clean_domain,
            **cert_data
        )
        return response.model_dump()
        
    except ValueError as e:
        return SSLResponse(success=False, target=domain, error=str(e)).model_dump()
    except Exception as e:
        logger.error(f"SSL Error for {domain}: {str(e)}")
        return SSLResponse(success=False, target=domain, error=str(e)).model_dump()
