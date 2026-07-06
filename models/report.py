"""
Pydantic models for Website Audit Reports.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

from .responses import (
    RDAPResponse, DNSResponse, SSLResponse, HeaderResponse,
    CookieResponse, FingerprintResponse, RobotsResponse, SecurityTxtResponse
)

class WebsiteAuditReport(BaseModel):
    domain: str
    audit_date: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    status: str = "COMPLETED"
    
    rdap: Optional[RDAPResponse] = None
    dns: Optional[DNSResponse] = None
    ssl: Optional[SSLResponse] = None
    headers: Optional[HeaderResponse] = None
    cookies: Optional[CookieResponse] = None
    fingerprint: Optional[FingerprintResponse] = None
    robots_txt: Optional[RobotsResponse] = None
    security_txt: Optional[SecurityTxtResponse] = None
    
    summary: Dict[str, Any] = Field(default_factory=dict)
