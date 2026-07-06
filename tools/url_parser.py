from urllib.parse import urlparse
from typing import Dict, Any

def url_parse(url: str) -> Dict[str, Any]:
    """
    Parse a URL into its components.
    """
    try:
        parsed = urlparse(url)
        return {
            "success": True,
            "target": url,
            "scheme": parsed.scheme,
            "netloc": parsed.netloc,
            "path": parsed.path,
            "params": parsed.params,
            "query": parsed.query,
            "fragment": parsed.fragment,
            "hostname": parsed.hostname,
            "port": parsed.port
        }
    except Exception as e:
        return {
            "success": False,
            "target": url,
            "error": str(e)
        }
