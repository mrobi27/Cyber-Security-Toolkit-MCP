import logging
import json
import os
from typing import Dict, Any
from services.report_service import generate_html_report, generate_json_report
from models.report import WebsiteAuditReport

logger = logging.getLogger(__name__)

def generate_report(audit_data: Dict[str, Any], format: str = "html", output_path: str = "./report") -> str:
    """
    Generate a final report from the website audit data.
    format: "html" or "json"
    output_path: Base filename for the report.
    """
    try:
        report = WebsiteAuditReport(**audit_data)
        
        if format.lower() == "html":
            content = generate_html_report(report)
            filename = f"{output_path}.html"
        elif format.lower() == "json":
            content = generate_json_report(report)
            filename = f"{output_path}.json"
        else:
            raise ValueError(f"Unsupported format: {format}")
            
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"Report generated successfully: {os.path.abspath(filename)}"
        
    except Exception as e:
        logger.error(f"Report Generation Error: {str(e)}")
        return f"Failed to generate report: {str(e)}"
