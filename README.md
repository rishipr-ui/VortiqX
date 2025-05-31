# VortiqX - Security Vulnerability Scanner

A Flask-based vulnerability testing website with AI-powered analysis and clean black and white interface for comprehensive URL security scanning.

## Features

- **Comprehensive Security Scanning**: SSL/TLS analysis, HTTP headers check, common vulnerabilities detection
- **AI-Powered Analysis**: OpenAI integration for intelligent vulnerability assessment
- **Clean Interface**: Modern black and white design with responsive layout
- **Real-time Scanning**: Live vulnerability detection and reporting
- **Detailed Reports**: Risk categorization and actionable recommendations

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd vortiqx
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export OPENAI_API_KEY="your_openai_api_key"
export SESSION_SECRET="your_session_secret"
```

4. Run the application:
```bash
python main.py
```

## Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for AI-powered vulnerability analysis
- `SESSION_SECRET`: Flask session secret key
- `ZAP_API_KEY`: (Optional) OWASP ZAP API key if using ZAP integration
- `ZAP_HOST`: (Optional) ZAP host address
- `ZAP_PORT`: (Optional) ZAP port number

## Usage

1. Navigate to the VortiqX homepage
2. Enter a URL you want to scan for vulnerabilities
3. Click "Start Security Scan"
4. Review the comprehensive security report

## Project Structure

```
vortiqx/
├── templates/          # HTML templates
├── static/            # CSS, JS, and assets
├── app.py            # Flask application setup
├── main.py           # Application entry point
├── routes.py         # URL routes and handlers
├── vulnerability_scanner.py    # Core scanning logic
├── ai_vulnerability_analyzer.py # AI-powered analysis
├── zap_scanner.py    # OWASP ZAP integration (optional)
└── requirements.txt  # Python dependencies
```

## Security Checks

VortiqX performs the following security assessments:

- SSL/TLS certificate validation
- Security headers analysis
- Directory traversal testing
- XSS protection verification
- Common vulnerability detection
- AI-powered content analysis
- Information disclosure checks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Disclaimer

VortiqX is for educational and authorized testing purposes only. Only scan websites you own or have explicit permission to test.