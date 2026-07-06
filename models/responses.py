"""
Pydantic models for Tool Responses.
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class BaseSecurityResponse(BaseModel):
    success: bool = Field(description="Whether the operation was successful")
    error: Optional[str] = Field(default=None, description="Error message if any")
    target: str = Field(description="The target domain or URL")

class RDAPResponse(BaseSecurityResponse):
    registrar: Optional[str] = None
    creation_date: Optional[str] = None
    expiration_date: Optional[str] = None
    name_servers: List[str] = Field(default_factory=list)
    status: List[str] = Field(default_factory=list)
    raw_data: Dict[str, Any] = Field(default_factory=dict)

class DNSResponse(BaseSecurityResponse):
    a_records: List[str] = Field(default_factory=list)
    aaaa_records: List[str] = Field(default_factory=list)
    mx_records: List[Dict[str, Any]] = Field(default_factory=list)
    txt_records: List[str] = Field(default_factory=list)
    ns_records: List[str] = Field(default_factory=list)

class SSLResponse(BaseSecurityResponse):
    issuer: str = ""
    subject: str = ""
    version: str = ""
    serial_number: str = ""
    not_before: str = ""
    not_after: str = ""
    days_until_expiration: int = 0
    is_valid: bool = False
    san_list: List[str] = Field(default_factory=list)

class HeaderResponse(BaseSecurityResponse):
    headers: Dict[str, str] = Field(default_factory=dict)
    missing_security_headers: List[str] = Field(default_factory=list)
    security_score: int = 0

class CookieResponse(BaseSecurityResponse):
    cookies: List[Dict[str, Any]] = Field(default_factory=list)
    insecure_cookies: List[str] = Field(default_factory=list)

class FingerprintResponse(BaseSecurityResponse):
    server: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    x_powered_by: Optional[str] = None

class RobotsResponse(BaseSecurityResponse):
    exists: bool = False
    content: Optional[str] = None
    disallowed_paths: List[str] = Field(default_factory=list)
    sitemaps: List[str] = Field(default_factory=list)

class SecurityTxtResponse(BaseSecurityResponse):
    exists: bool = False
    content: Optional[str] = None
    contacts: List[str] = Field(default_factory=list)
    encryption: List[str] = Field(default_factory=list)
