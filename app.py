from flask import Flask, request, jsonify
import requests
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

ZAP_BASE = 'http://localhost:8090'  # OWASP ZAP must be running here

@app.route('/api/scan', methods=['GET'])
def scan_target():
    target = request.args.get('url')
    if not target:
        return jsonify({'error': 'Missing URL'}), 400

    scan = requests.get(f'{ZAP_BASE}/JSON/ascan/action/scan/', params={'url': target})
    scan_id = scan.json().get('scan')

    while True:
        status = requests.get(f'{ZAP_BASE}/JSON/ascan/view/status/', params={'scanId': scan_id})
        if status.json()['status'] == '100':
            break
        time.sleep(2)

    alerts = requests.get(f'{ZAP_BASE}/JSON/core/view/alerts/', params={'baseurl': target}).json()
    results = [
        {
            'name': alert['alert'],
            'severity': alert['risk'].lower(),
            'description': alert['description'],
            'fix': alert.get('solution', 'No fix provided.')
        }
        for alert in alerts['alerts']
    ]
    return jsonify(results)

if __name__ == '__main__':
    app.run(port=5000)