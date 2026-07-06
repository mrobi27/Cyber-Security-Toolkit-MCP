import httpx
from typing import Dict, Any, List
from utils.constants import HTTP_HEADERS, DEFAULT_TIMEOUT, EXPECTED_SECURITY_HEADERS

async def _fetch_url(url: str) -> httpx.Response:
    """Helper to fetch URL with consistent settings."""
    async with httpx.AsyncClient(verify=False, timeout=DEFAULT_TIMEOUT) as client:
        response = await client.get(url, headers=HTTP_HEADERS, follow_redirects=True)
        return response

async def analyze_headers(url: str) -> Dict[str, Any]:
    """
    Analyze HTTP Security Headers.
    """
    try:
        response = await _fetch_url(url)
        headers = {k.lower(): v for k, v in response.headers.items()}
        
        missing = []
        score = 100
        penalty_per_missing = 100 // len(EXPECTED_SECURITY_HEADERS)
        
        for expected in EXPECTED_SECURITY_HEADERS:
            if expected.lower() not in headers:
                missing.append(expected)
                score -= penalty_per_missing
                
        return {
            "headers": dict(response.headers),
            "missing_security_headers": missing,
            "security_score": max(0, score)
        }
    except Exception as e:
        raise Exception(f"Failed to analyze headers: {str(e)}")

async def analyze_cookies(url: str) -> Dict[str, Any]:
    """
    Analyze Cookie security (Secure, HttpOnly, SameSite).
    """
    try:
        response = await _fetch_url(url)
        cookies = []
        insecure = []
        
        for name, cookie in response.cookies.items():
            pass
            
        set_cookies = response.headers.get_list('set-cookie')
        for cookie_str in set_cookies:
            parts = cookie_str.split(';')
            name_val = parts[0].split('=', 1)
            if len(name_val) != 2:
                continue
                
            name = name_val[0].strip()
            attrs = [p.strip().lower() for p in parts[1:]]
            
            is_secure = "secure" in attrs
            is_httponly = "httponly" in attrs
            
            samesite = "None"
            for attr in attrs:
                if attr.startswith("samesite="):
                    samesite = attr.split("=")[1].strip()
                    break
                    
            cookies.append({
                "name": name,
                "secure": is_secure,
                "httponly": is_httponly,
                "samesite": samesite
            })
            
            if not is_secure or not is_httponly:
                insecure.append(name)
                
        return {
            "cookies": cookies,
            "insecure_cookies": insecure
        }
    except Exception as e:
        raise Exception(f"Failed to analyze cookies: {str(e)}")

async def check_robots_txt(url: str) -> Dict[str, Any]:
    """
    Fetch and analyze robots.txt.
    """
    try:
        robots_url = f"{url.rstrip('/')}/robots.txt"
        response = await _fetch_url(robots_url)
        
        if response.status_code != 200:
            return {"exists": False, "content": None, "disallowed_paths": [], "sitemaps": []}
            
        content = response.text
        disallowed = []
        sitemaps = []
        
        for line in content.splitlines():
            line = line.strip()
            if line.lower().startswith('disallow:'):
                path = line.split(':', 1)[1].strip()
                if path:
                    disallowed.append(path)
            elif line.lower().startswith('sitemap:'):
                path = line.split(':', 1)[1].strip()
                if path:
                    sitemaps.append(path)
                    
        return {
            "exists": True,
            "content": content,
            "disallowed_paths": disallowed,
            "sitemaps": sitemaps
        }
    except Exception as e:
        raise Exception(f"Failed to check robots.txt: {str(e)}")

async def check_security_txt(url: str) -> Dict[str, Any]:
    """
    Fetch and analyze security.txt.
    """
    try:
        paths = ["/.well-known/security.txt", "/security.txt"]
        
        for path in paths:
            check_url = f"{url.rstrip('/')}{path}"
            response = await _fetch_url(check_url)
            
            if response.status_code == 200 and "Contact:" in response.text:
                content = response.text
                contacts = []
                encryption = []
                
                for line in content.splitlines():
                    line = line.strip()
                    if line.startswith('Contact:'):
                        contacts.append(line.split(':', 1)[1].strip())
                    elif line.startswith('Encryption:'):
                        encryption.append(line.split(':', 1)[1].strip())
                        
                return {
                    "exists": True,
                    "content": content,
                    "contacts": contacts,
                    "encryption": encryption
                }
                
        return {"exists": False, "content": None, "contacts": [], "encryption": []}
    except Exception as e:
        raise Exception(f"Failed to check security.txt: {str(e)}")
