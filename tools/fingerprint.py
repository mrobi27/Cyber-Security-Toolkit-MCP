import logging
from typing import Dict, Any
from services.fingerprint_service import detect_technologies
from models.responses import FingerprintResponse
from utils.validator import sanitize_url

logger = logging.getLogger(__name__)

async def technology_fingerprint(url: str) -> Dict[str, Any]:
    """
    Fingerprint the web application technologies for a given URL.
    """
    try:
        clean_url = sanitize_url(url)
        tech_data = await detect_technologies(clean_url)
        
        response = FingerprintResponse(
            success=True,
            target=clean_url,
            **tech_data
        )
        return response.model_dump()
        
    except ValueError as e:
        return FingerprintResponse(success=False, target=url, error=str(e)).model_dump()
    except Exception as e:
        logger.error(f"Fingerprint Error for {url}: {str(e)}")
        return FingerprintResponse(success=False, target=url, error=str(e)).model_dump()
