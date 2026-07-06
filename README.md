<div align="center">

# 🛡️ CyberMCP

### AI-Powered Cyber Security Assistant built with Model Context Protocol (MCP)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastMCP](https://img.shields.io/badge/FastMCP-Latest-blue)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success)](#)

*A production-ready MCP Server that brings cybersecurity analysis tools directly to AI assistants such as Claude Desktop.*

</div>

---

## ✨ Overview

CyberMCP is an **AI-powered Cyber Security Assistant** built on the **Model Context Protocol (MCP)**.

Instead of manually checking DNS, SSL certificates, HTTP headers, cookies, or security configurations, AI assistants can invoke CyberMCP tools and receive structured security analysis automatically.

CyberMCP follows a **Clean Architecture** approach with modular services, asynchronous networking, and defensive security principles.

---

# 🚀 Features

| Feature | Description |
|----------|-------------|
| 🌍 RDAP Lookup | Retrieve domain registration information |
| 🌐 DNS Analyzer | Analyze A, AAAA, MX, TXT, NS records |
| 🔒 SSL Inspector | Inspect SSL/TLS certificates |
| 🛡 Security Headers | Detect missing HTTP security headers |
| 🍪 Cookie Analyzer | Analyze Secure, HttpOnly & SameSite |
| 🧬 Technology Fingerprinting | Detect web technologies |
| 🤖 robots.txt Analyzer | Parse robots.txt |
| 📄 security.txt Checker | Find security contact information |
| 📊 Website Audit | Run all security checks together |
| 📑 Report Generator | Export HTML & JSON reports |

---

# 🏗️ Architecture

```text
                 AI Assistant
             (Claude Desktop)
                     │
                     ▼
              Model Context Protocol
                     │
                     ▼
                CyberMCP Server
                     │
 ┌──────────────┬───────────────┬───────────────┐
 │              │               │               │
 ▼              ▼               ▼               ▼
 RDAP        DNS Analyzer    SSL Checker    Headers
 │
 ▼
 Services
 │
 ▼
 External APIs / DNS / Websites
```

---

# 📂 Project Structure

```text
CyberMCP/

├── mcp_server.py
├── README.md
├── requirements.txt
│
├── tools/
├── services/
├── models/
├── utils/
├── tests/
└── docs/
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CyberMCP.git

cd CyberMCP
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Development Server

```bash
mcp dev mcp_server.py
```

---

# 🔗 Claude Desktop Integration

Edit:

```text
claude_desktop_config.json
```

Example:

```json
{
  "mcpServers": {
    "CyberMCP": {
      "command": "python",
      "args": [
        "/path/to/CyberMCP/mcp_server.py"
      ]
    }
  }
}
```

---

# 💡 Example

Ask Claude:

```text
Analyze the security of openai.com
```

Claude automatically calls:

```text
✔ RDAP Lookup

✔ DNS Analyzer

✔ SSL Inspection

✔ Security Headers

✔ robots.txt

✔ security.txt

✔ Technology Fingerprinting
```

Result:

```text
Security Score : 91/100

SSL           ✔

HSTS          ✔

CSP           ✖

robots.txt    ✔

security.txt  ✔
```

---

# 🛣️ Roadmap

- [x] FastMCP Server
- [x] RDAP Lookup
- [x] DNS Analyzer
- [x] SSL Inspector
- [x] Header Analyzer
- [ ] Cookie Analyzer
- [ ] Website Audit
- [ ] HTML Report
- [ ] PDF Report
- [ ] VirusTotal Integration
- [ ] AbuseIPDB Integration

---

# 🤝 Contributing

Contributions are welcome!

Feel free to open an Issue or submit a Pull Request.

---

<div align="center">

Made with ❤️ using **Python**, **FastMCP**, and **Model Context Protocol**

⭐ If you find this project useful, don't forget to give it a star!

</div>