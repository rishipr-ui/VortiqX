import logging
import validators
from flask import render_template, request, flash, redirect, url_for
from app import app
from vulnerability_scanner import VulnerabilityScanner

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    """Main page with URL input form"""
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_url():
    """Handle URL scanning request"""
    try:
        target_url = request.form.get('url', '').strip()
        
        if not target_url:
            flash('Please enter a URL to scan', 'error')
            return redirect(url_for('index'))
        
        # Add protocol if missing
        if not target_url.startswith(('http://', 'https://')):
            target_url = 'https://' + target_url
        
        # Validate URL
        if not validators.url(target_url):
            flash('Please enter a valid URL', 'error')
            return redirect(url_for('index'))
        
        # Initialize vulnerability scanner
        scanner = VulnerabilityScanner()
        
        # Perform scan
        logger.info(f"Starting scan for URL: {target_url}")
        scan_results = scanner.scan_url(target_url)
        
        if scan_results is None:
            flash('Failed to complete the security scan. Please try again.', 'error')
            return redirect(url_for('index'))
        
        # Categorize results by risk level
        categorized_results = {
            'High': [],
            'Medium': [],
            'Low': [],
            'Informational': []
        }
        
        for alert in scan_results:
            risk_level = alert.get('risk', 'Informational')
            if risk_level not in categorized_results:
                categorized_results[risk_level] = []
            categorized_results[risk_level].append(alert)
        
        logger.info(f"Scan completed for {target_url}. Found {len(scan_results)} alerts.")
        
        return render_template('results.html', 
                             url=target_url, 
                             results=categorized_results,
                             total_alerts=len(scan_results))
    
    except Exception as e:
        logger.error(f"Error during scan: {str(e)}")
        flash('An error occurred during the scan. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/about')
def about():
    """About page with information about the vulnerability scanner"""
    return render_template('about.html')

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return render_template('500.html'), 500
