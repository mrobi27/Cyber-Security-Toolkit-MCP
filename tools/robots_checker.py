import logging
from typing import Dict, Any
from services.http_service import check_robots_txt
from models.responses import RobotsResponse
from utils.validator import sanitize_url

logger = logging.getLogger(__name__)

async def robots_check(url: str) -> Dict[str, Any]:
    """
    Check and analyze robots.txt for a given URL.
    """
    try:
        clean_url = sanitize_url(url)
        robots_data = await check_robots_txt(clean_url)
        
        response = RobotsResponse(
            success=True,
            target=clean_url,
            **robots_data
        )
        return response.model_dump()
        
    except ValueError as e:
        return RobotsResponse(success=False, target=url, error=str(e)).model_dump()
    except Exception as e:
        logger.error(f"Robots.txt Error for {url}: {str(e)}")
        return RobotsResponse(success=False, target=url, error=str(e)).model_dump()
