import logging
from mcp.server.fastmcp import FastMCP

from tools.whois_tool import whois_lookup
from tools.dns_tool import dns_lookup
from tools.ssl_checker import ssl_check
from tools.header_analyzer import header_check
from tools.cookie_analyzer import cookie_check
from tools.fingerprint import technology_fingerprint
from tools.robots_checker import robots_check
from tools.securitytxt_checker import securitytxt_check
from tools.url_parser import url_parse
from tools.website_audit import website_audit
from tools.report_generator import generate_report

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("cybermcp")

mcp = FastMCP(
    "CyberMCP",
    dependencies=["httpx", "dnspython", "cryptography", "pydantic", "Jinja2", "beautifulsoup4"]
)

mcp.tool()(whois_lookup)
mcp.tool()(dns_lookup)
mcp.tool()(ssl_check)
mcp.tool()(header_check)
mcp.tool()(cookie_check)
mcp.tool()(technology_fingerprint)
mcp.tool()(robots_check)
mcp.tool()(securitytxt_check)
mcp.tool()(url_parse)
mcp.tool()(website_audit)
mcp.tool()(generate_report)

if __name__ == "__main__":
    logger.info("Starting CyberMCP Server...")
    mcp.run()