import json
from jinja2 import Environment, BaseLoader
from models.report import WebsiteAuditReport

REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberMCP Audit Report - {{ report.domain }}</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 1000px; margin: 0 auto; padding: 20px; }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h2 { color: #2980b9; margin-top: 30px; }
        .card { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 15px; margin-bottom: 20px; }
        .success { color: #27ae60; font-weight: bold; }
        .error { color: #e74c3c; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 15px; }
        th, td { border: 1px solid #dee2e6; padding: 8px; text-align: left; }
        th { background-color: #e9ecef; }
        pre { background: #2d3436; color: #f1f2f6; padding: 10px; border-radius: 5px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>Security Audit Report: {{ report.domain }}</h1>
    <p><strong>Date:</strong> {{ report.audit_date }}</p>
    <p><strong>Status:</strong> <span class="{% if report.status == 'COMPLETED' %}success{% else %}error{% endif %}">{{ report.status }}</span></p>

    {% if report.rdap %}
    <div class="card">
        <h2>RDAP / WHOIS Information</h2>
        {% if report.rdap.success %}
            <p><strong>Registrar:</strong> {{ report.rdap.registrar }}</p>
            <p><strong>Creation Date:</strong> {{ report.rdap.creation_date }}</p>
            <p><strong>Expiration Date:</strong> {{ report.rdap.expiration_date }}</p>
            <p><strong>Name Servers:</strong> {{ report.rdap.name_servers | join(', ') }}</p>
        {% else %}
            <p class="error">{{ report.rdap.error }}</p>
        {% endif %}
    </div>
    {% endif %}

    {% if report.ssl %}
    <div class="card">
        <h2>SSL Certificate</h2>
        {% if report.ssl.success %}
            <p><strong>Issuer:</strong> {{ report.ssl.issuer }}</p>
            <p><strong>Valid:</strong> <span class="{% if report.ssl.is_valid %}success{% else %}error{% endif %}">{{ report.ssl.is_valid }}</span></p>
            <p><strong>Expires In:</strong> {{ report.ssl.days_until_expiration }} days</p>
        {% else %}
            <p class="error">{{ report.ssl.error }}</p>
        {% endif %}
    </div>
    {% endif %}

    {% if report.headers %}
    <div class="card">
        <h2>Security Headers</h2>
        {% if report.headers.success %}
            <p><strong>Score:</strong> {{ report.headers.security_score }}/100</p>
            {% if report.headers.missing_security_headers %}
                <p class="error">Missing Headers:</p>
                <ul>
                    {% for h in report.headers.missing_security_headers %}
                        <li>{{ h }}</li>
                    {% endfor %}
                </ul>
            {% else %}
                <p class="success">All expected security headers are present.</p>
            {% endif %}
        {% else %}
            <p class="error">{{ report.headers.error }}</p>
        {% endif %}
    </div>
    {% endif %}

    {% if report.fingerprint %}
    <div class="card">
        <h2>Technology Fingerprint</h2>
        {% if report.fingerprint.success %}
            <p><strong>Server:</strong> {{ report.fingerprint.server or 'Unknown' }}</p>
            <p><strong>Technologies:</strong></p>
            <ul>
                {% for tech in report.fingerprint.technologies %}
                    <li>{{ tech }}</li>
                {% endfor %}
            </ul>
        {% else %}
            <p class="error">{{ report.fingerprint.error }}</p>
        {% endif %}
    </div>
    {% endif %}

</body>
</html>
"""

def generate_html_report(report: WebsiteAuditReport) -> str:
    """Generates an HTML report from a WebsiteAuditReport object."""
    template = Environment(loader=BaseLoader()).from_string(REPORT_TEMPLATE)
    return template.render(report=report)

def generate_json_report(report: WebsiteAuditReport) -> str:
    """Generates a JSON report from a WebsiteAuditReport object."""
    return report.model_dump_json(indent=4)
