import logging
from typing import Dict, Any
from services.http_service import analyze_headers
from models.responses import HeaderResponse
from utils.validator import sanitize_url

logger = logging.getLogger(__name__)

async def header_check(url: str) -> Dict[str, Any]:
    """
    Analyze HTTP Security Headers for a given URL.
    """
    try:
        clean_url = sanitize_url(url)
        header_data = await analyze_headers(clean_url)
        
        response = HeaderResponse(
            success=True,
            target=clean_url,
            **header_data
        )
        return response.model_dump()
        
    except ValueError as e:
        return HeaderResponse(success=False, target=url, error=str(e)).model_dump()
    except Exception as e:
        logger.error(f"Header Analysis Error for {url}: {str(e)}")
        return HeaderResponse(success=False, target=url, error=str(e)).model_dump()
