# VortiqX – OWASP Top 10 Vulnerability Scanner

VortiqX is a hackathon project that scans banking web applications for OWASP Top 10 vulnerabilities using the OWASP ZAP engine.

## Features
- Real vulnerability scanning via ZAP API
- Simple frontend UI (HTML/CSS/JS)
- Flask backend that triggers scans and shows results

## How to Run Locally

### 1. Start ZAP in Docker
```bash
docker run -u zap -p 8090:8090 -i owasp/zap2docker-stable \
zap.sh -daemon -host 0.0.0.0 -port 8090 -config api.disablekey=true
```

### 2. Start Flask Backend
```bash
cd backend/
pip install -r requirements.txt
python app.py
```

### 3. Open the Frontend
Just open `frontend/index.html` in a browser.

## Team
Team Vortiq | Hackathon 2025