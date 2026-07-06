import logging
from typing import Dict, Any
from services.http_service import check_security_txt
from models.responses import SecurityTxtResponse
from utils.validator import sanitize_url

logger = logging.getLogger(__name__)

async def securitytxt_check(url: str) -> Dict[str, Any]:
    """
    Check and analyze security.txt for a given URL.
    """
    try:
        clean_url = sanitize_url(url)
        security_data = await check_security_txt(clean_url)
        
        response = SecurityTxtResponse(
            success=True,
            target=clean_url,
            **security_data
        )
        return response.model_dump()
        
    except ValueError as e:
        return SecurityTxtResponse(success=False, target=url, error=str(e)).model_dump()
    except Exception as e:
        logger.error(f"Security.txt Error for {url}: {str(e)}")
        return SecurityTxtResponse(success=False, target=url, error=str(e)).model_dump()
