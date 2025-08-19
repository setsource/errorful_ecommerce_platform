# scripts/health_check.py
#!/usr/bin/env python3
import requests
import logging
import sys
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVICES = {
    'user-service': 'http://localhost:8001/health',
    'product-service': 'http://localhost:8002/health', 
    'order-service': 'http://localhost:8003/health',
    'payment-service': 'http://localhost:8004/health'
}

def check_service_health():
    failed_services = []
    
    for service, url in SERVICES.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                logger.info(f"✅ {service}: HEALTHY")
            else:
                logger.error(f"❌ {service}: UNHEALTHY (status: {response.status_code})")
                failed_services.append(service)
        except requests.exceptions.ConnectionError:
            logger.error(f"💥 {service}: CONNECTION FAILED")
            failed_services.append(service)
        except requests.exceptions.Timeout:
            logger.error(f"⏱️  {service}: TIMEOUT")  
            failed_services.append(service)
        except Exception as e:
            logger.error(f"🚫 {service}: ERROR - {str(e)}")
            failed_services.append(service)
    
    if failed_services:
        logger.critical(f"CRITICAL: {len(failed_services)} services are unhealthy: {failed_services}")
        return False
    else:
        logger.info("🎉 All services are healthy!")
        return True

if __name__ == "__main__":
    healthy = check_service_health()
    sys.exit(0 if healthy else 1)

