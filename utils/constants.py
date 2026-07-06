"""
Constants for CyberMCP.
"""

DEFAULT_TIMEOUT = 10.0
USER_AGENT = "CyberMCP-Security-Assistant/1.0"

HTTP_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

RDAP_BOOTSTRAP_URL = "https://rdap.org/domain/"

EXPECTED_SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy"
]
