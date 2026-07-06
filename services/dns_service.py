import dns.asyncresolver
import dns.exception
from typing import Dict, List, Any

async def resolve_dns_records(domain: str) -> Dict[str, Any]:
    """
    Asynchronously resolve various DNS records for a domain.
    """
    resolver = dns.asyncresolver.Resolver()
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    
    results = {
        "a_records": [],
        "aaaa_records": [],
        "mx_records": [],
        "txt_records": [],
        "ns_records": []
    }
    
    record_types = {
        'A': 'a_records',
        'AAAA': 'aaaa_records',
        'MX': 'mx_records',
        'TXT': 'txt_records',
        'NS': 'ns_records'
    }
    
    for rtype, key in record_types.items():
        try:
            answers = await resolver.resolve(domain, rtype)
            for rdata in answers:
                if rtype == 'MX':
                    results[key].append({
                        "preference": rdata.preference,
                        "exchange": str(rdata.exchange).rstrip('.')
                    })
                elif rtype == 'TXT':
                    txt_data = b"".join(rdata.strings).decode('utf-8', errors='ignore')
                    results[key].append(txt_data)
                else:
                    results[key].append(str(rdata).rstrip('.'))
        except dns.resolver.NoAnswer:
            pass  
        except dns.resolver.NXDOMAIN:
            raise ValueError(f"Domain '{domain}' does not exist.")
        except dns.exception.Timeout:
            raise Exception(f"Timeout while resolving {rtype} records.")
        except Exception as e:
            pass
            
    return results
