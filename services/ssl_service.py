import ssl
import socket
import asyncio
from typing import Dict, Any, List
from datetime import datetime, timezone
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from utils.constants import DEFAULT_TIMEOUT

def _fetch_cert_sync(domain: str, port: int = 443) -> bytes:
    """
    Synchronously fetches the raw SSL certificate from a domain.
    Used within an asyncio executor to prevent blocking.
    """
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    
    with socket.create_connection((domain, port), timeout=DEFAULT_TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=domain) as ssock:
            der_cert = ssock.getpeercert(binary_form=True)
            if der_cert is None:
                raise Exception("No certificate returned from server.")
            return der_cert

async def get_ssl_certificate(domain: str) -> Dict[str, Any]:
    """
    Asynchronously fetch and parse SSL certificate.
    """
    loop = asyncio.get_running_loop()
    
    try:
        der_cert = await loop.run_in_executor(None, _fetch_cert_sync, domain, 443)
        
        cert = x509.load_der_x509_certificate(der_cert, default_backend())
        
        subject_attrs = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
        subject = subject_attrs[0].value if subject_attrs else ""
        
        issuer_attrs = cert.issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
        issuer = issuer_attrs[0].value if issuer_attrs else ""
        
        san_list = []
        try:
            ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
            san_list = ext.value.get_values_for_type(x509.DNSName)
        except x509.ExtensionNotFound:
            pass
            
        not_before = cert.not_valid_before_utc
        not_after = cert.not_valid_after_utc
        
        now = datetime.now(timezone.utc)
        is_valid = not_before <= now <= not_after
        days_until_expiration = (not_after - now).days

        return {
            "issuer": issuer,
            "subject": subject,
            "version": cert.version.name,
            "serial_number": str(cert.serial_number),
            "not_before": not_before.isoformat(),
            "not_after": not_after.isoformat(),
            "days_until_expiration": days_until_expiration,
            "is_valid": is_valid,
            "san_list": san_list
        }
        
    except socket.gaierror:
        raise ValueError(f"Failed to resolve domain: {domain}")
    except socket.timeout:
        raise Exception("Connection timed out while fetching SSL certificate.")
    except Exception as e:
        raise Exception(f"SSL Error: {str(e)}")
