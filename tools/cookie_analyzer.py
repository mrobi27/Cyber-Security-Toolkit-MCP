import logging
from typing import Dict, Any
from services.http_service import analyze_cookies
from models.responses import CookieResponse
from utils.validator import sanitize_url

logger = logging.getLogger(__name__)

async def cookie_check(url: str) -> Dict[str, Any]:
    """
    Analyze Cookie security (Secure, HttpOnly, SameSite) for a given URL.
    """
    try:
        clean_url = sanitize_url(url)
        cookie_data = await analyze_cookies(clean_url)
        
        response = CookieResponse(
            success=True,
            target=clean_url,
            **cookie_data
        )
        return response.model_dump()
        
    except ValueError as e:
        return CookieResponse(success=False, target=url, error=str(e)).model_dump()
    except Exception as e:
        logger.error(f"Cookie Analysis Error for {url}: {str(e)}")
        return CookieResponse(success=False, target=url, error=str(e)).model_dump()
