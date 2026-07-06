import logging
import asyncio
from typing import Dict, Any
from models.report import WebsiteAuditReport
from utils.validator import sanitize_url, sanitize_domain

from tools.whois_tool import whois_lookup
from tools.dns_tool import dns_lookup
from tools.ssl_checker import ssl_check
from tools.header_analyzer import header_check
from tools.cookie_analyzer import cookie_check
from tools.fingerprint import technology_fingerprint
from tools.robots_checker import robots_check
from tools.securitytxt_checker import securitytxt_check

logger = logging.getLogger(__name__)

async def website_audit(domain_or_url: str) -> Dict[str, Any]:
    """
    Perform a full website security audit, running multiple tools concurrently.
    """
    try:
        domain = sanitize_domain(domain_or_url)
        url = sanitize_url(domain_or_url)
        
        report = WebsiteAuditReport(domain=domain)
        
        results = await asyncio.gather(
            whois_lookup(domain),
            dns_lookup(domain),
            ssl_check(domain),
            header_check(url),
            cookie_check(url),
            technology_fingerprint(url),
            robots_check(url),
            securitytxt_check(url),
            return_exceptions=True
        )
        
        (rdap_res, dns_res, ssl_res, header_res, 
         cookie_res, finger_res, robots_res, sectxt_res) = results
         
        if not isinstance(rdap_res, Exception): report.rdap = rdap_res
        if not isinstance(dns_res, Exception): report.dns = dns_res
        if not isinstance(ssl_res, Exception): report.ssl = ssl_res
        if not isinstance(header_res, Exception): report.headers = header_res
        if not isinstance(cookie_res, Exception): report.cookies = cookie_res
        if not isinstance(finger_res, Exception): report.fingerprint = finger_res
        if not isinstance(robots_res, Exception): report.robots_txt = robots_res
        if not isinstance(sectxt_res, Exception): report.security_txt = sectxt_res
        
        issues = 0
        if report.headers and getattr(report.headers, 'missing_security_headers', None):
            issues += len(report.headers.missing_security_headers)
        if report.ssl and not getattr(report.ssl, 'is_valid', True):
            issues += 1
            
        report.summary = {
            "total_issues_found": issues,
            "overall_status": "POOR" if issues > 3 else "FAIR" if issues > 0 else "GOOD"
        }
        
        return report.model_dump()
        
    except Exception as e:
        logger.error(f"Audit Error for {domain_or_url}: {str(e)}")
        return {"error": str(e), "status": "FAILED"}
