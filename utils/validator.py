"""
Validators for CyberMCP.
Provides utility functions to validate domains and URLs before processing.
"""

import re
from urllib.parse import urlparse

def is_valid_domain(domain: str) -> bool:
    """
    Validates if a string is a well-formed domain name.
    
    Args:
        domain (str): The domain to validate (e.g., 'example.com')
        
    Returns:
        bool: True if valid, False otherwise.
    """
    if not isinstance(domain, str) or not domain:
        return False
        
    domain = domain.strip().lower()
    
    if domain.startswith(('http://', 'https://')):
        parsed = urlparse(domain)
        domain = parsed.hostname or ""

    domain_regex = re.compile(
        r'^(?:[a-zA-Z0-9]'
        r'(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'
        r'[a-zA-Z]{2,63}$'
    )
    
    return bool(domain_regex.match(domain))

def sanitize_domain(domain: str) -> str:
    """
    Sanitizes and normalizes the domain input.
    Extracts hostname if URL is provided.
    Raises ValueError if invalid.
    """
    domain = domain.strip().lower()
    if domain.startswith(('http://', 'https://')):
        parsed = urlparse(domain)
        domain = parsed.hostname or ""
        
    if not is_valid_domain(domain):
        raise ValueError(f"Invalid domain format: {domain}")
        
    return domain

def sanitize_url(url: str) -> str:
    """
    Ensures a URL is valid and uses http/https scheme.
    """
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = f"https://{url}"
        
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError(f"Invalid URL format: {url}")
        
    return url
