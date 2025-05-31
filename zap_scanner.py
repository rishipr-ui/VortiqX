import os
import time
import logging
from zapv2 import ZAPv2

logger = logging.getLogger(__name__)

class ZAPScanner:
    """OWASP ZAP Scanner integration class"""
    
    def __init__(self):
        # ZAP configuration from environment variables
        self.zap_proxy_host = os.getenv('ZAP_HOST', '127.0.0.1')
        self.zap_proxy_port = int(os.getenv('ZAP_PORT', '8080'))
        self.zap_api_key = os.getenv('ZAP_API_KEY', '')
        self.zap_target_url = os.getenv('ZAP_TARGET_URL', f'http://{self.zap_proxy_host}:{self.zap_proxy_port}')
        
        # Initialize ZAP API client
        try:
            self.zap = ZAPv2(
                proxies={
                    'http': self.zap_target_url,
                    'https': self.zap_target_url
                },
                apikey=self.zap_api_key
            )
        except Exception as e:
            logger.error(f"Failed to initialize ZAP client: {str(e)}")
            self.zap = None
        
        logger.info(f"ZAP Scanner initialized targeting {self.zap_target_url}")
    
    def is_zap_available(self):
        """Check if ZAP is running and accessible"""
        try:
            # Try to get ZAP version to test connectivity
            version = self.zap.core.version
            logger.info(f"ZAP is available. Version: {version}")
            return True
        except Exception as e:
            logger.error(f"ZAP is not available: {str(e)}")
            return False
    
    def scan_url(self, target_url):
        """
        Perform a security scan on the target URL
        
        Args:
            target_url (str): The URL to scan
            
        Returns:
            list: List of security alerts found
        """
        try:
            logger.info(f"Starting security scan for: {target_url}")
            
            # Access the target URL to populate the sites tree
            logger.info("Accessing target URL...")
            self.zap.urlopen(target_url)
            time.sleep(2)  # Give ZAP time to process
            
            # Spider the target
            logger.info("Starting spider scan...")
            scan_id = self.zap.spider.scan(target_url)
            
            # Wait for spider to complete
            while int(self.zap.spider.status(scan_id)) < 100:
                logger.debug(f"Spider progress: {self.zap.spider.status(scan_id)}%")
                time.sleep(1)
            
            logger.info("Spider scan completed")
            
            # Active scan
            logger.info("Starting active scan...")
            scan_id = self.zap.ascan.scan(target_url)
            
            # Wait for active scan to complete
            while int(self.zap.ascan.status(scan_id)) < 100:
                progress = self.zap.ascan.status(scan_id)
                logger.debug(f"Active scan progress: {progress}%")
                time.sleep(2)
            
            logger.info("Active scan completed")
            
            # Get the scan results
            alerts = self.zap.core.alerts(baseurl=target_url)
            
            # Process and clean up the alerts
            processed_alerts = []
            for alert in alerts:
                processed_alert = {
                    'alert': alert.get('alert', 'Unknown Alert'),
                    'risk': alert.get('risk', 'Informational'),
                    'confidence': alert.get('confidence', 'Low'),
                    'description': alert.get('description', 'No description available'),
                    'solution': alert.get('solution', 'No solution provided'),
                    'reference': alert.get('reference', ''),
                    'url': alert.get('url', target_url),
                    'param': alert.get('param', ''),
                    'evidence': alert.get('evidence', ''),
                    'cweid': alert.get('cweid', ''),
                    'wascid': alert.get('wascid', '')
                }
                processed_alerts.append(processed_alert)
            
            logger.info(f"Scan completed. Found {len(processed_alerts)} alerts")
            return processed_alerts
            
        except Exception as e:
            logger.error(f"Error during scan: {str(e)}")
            return None
    
    def get_scan_progress(self, scan_id):
        """Get the progress of an active scan"""
        try:
            return int(self.zap.ascan.status(scan_id))
        except Exception as e:
            logger.error(f"Error getting scan progress: {str(e)}")
            return 0
    
    def stop_scan(self, scan_id):
        """Stop an active scan"""
        try:
            self.zap.ascan.stop(scan_id)
            logger.info(f"Stopped scan with ID: {scan_id}")
            return True
        except Exception as e:
            logger.error(f"Error stopping scan: {str(e)}")
            return False
