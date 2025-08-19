#!/usr/bin/env python3
"""
E-commerce Platform Runner - Simulation helps execute and generate the various failure scenarios
This file generates realistic errors and issues for postmortem analysis
"""

import sys
import time
import random
import logging
import json
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import requests
import psutil

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

# Create timestamp for filenames
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Log filenames with timestamp
app_log_file = f"logs/application_{timestamp}.log"
error_log_file = f"logs/error_{timestamp}.log"
access_log_file = f"logs/access_{timestamp}.log"

# Custom filter to separate error logs from application logs
class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR

class AppFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR

# Configure separate loggers
def setup_logging():
    # Main application logger (INFO and WARNING only)
    app_logger = logging.getLogger("EcommerceRunner")
    app_logger.setLevel(logging.INFO)
    
    # Application log handler (INFO and WARNING)
    app_handler = logging.FileHandler(app_log_file)
    app_handler.setLevel(logging.INFO)
    app_handler.addFilter(AppFilter())
    app_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    app_handler.setFormatter(app_formatter)
    
    # Error log handler (ERROR and CRITICAL only)
    error_handler = logging.FileHandler(error_log_file)
    error_handler.setLevel(logging.ERROR)
    error_handler.addFilter(ErrorFilter())
    error_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    error_handler.setFormatter(error_formatter)
    
    # Console handler (all levels)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to logger
    app_logger.addHandler(app_handler)
    app_logger.addHandler(error_handler)
    app_logger.addHandler(console_handler)
    
    return app_logger

# Setup logging
logger = setup_logging()

class EcommercePlatform:
    def __init__(self):
        self.services = {
            'user-service': {'port': 8001, 'status': 'running', 'cpu_usage': 0},
            'product-service': {'port': 8002, 'status': 'running', 'cpu_usage': 0},
            'order-service': {'port': 8003, 'status': 'running', 'cpu_usage': 0},
            'payment-service': {'port': 8004, 'status': 'running', 'cpu_usage': 0}
        }
        self.database_connection_pool = 20
        self.redis_connections = 100
        self.incident_scenarios = [
            'database_connection_leak',
            'memory_leak',
            'configuration_error',
            'third_party_api_failure',
            'high_cpu_usage',
            'disk_space_issue',
            'network_timeout',
            'authentication_failure'
        ]
        
    def simulate_incident(self):
        """Randomly trigger different types of incidents"""
        scenario = random.choice(self.incident_scenarios)
        logger.info(f"🚨 INCIDENT TRIGGERED: {scenario}")
        
        if scenario == 'database_connection_leak':
            self._database_connection_leak()
        elif scenario == 'memory_leak':
            self._memory_leak()
        elif scenario == 'configuration_error':
            self._configuration_error()
        elif scenario == 'third_party_api_failure':
            self._third_party_api_failure()
        elif scenario == 'high_cpu_usage':
            self._high_cpu_usage()
        elif scenario == 'disk_space_issue':
            self._disk_space_issue()
        elif scenario == 'network_timeout':
            self._network_timeout()
        elif scenario == 'authentication_failure':
            self._authentication_failure()
    
    def _database_connection_leak(self):
        logger.error("DATABASE CONNECTION POOL EXHAUSTED")
        logger.error("Connection pool size exceeded: 50/20 connections active")
        logger.error("service=order-service error=connection_timeout duration=30s")
        logger.error("Multiple queries stuck in WAITING state")
        logger.critical("Database performance degraded - query timeout increased to 45s")
        self.services['order-service']['status'] = 'degraded'
        
    def _memory_leak(self):
        logger.error("MEMORY USAGE CRITICAL")
        logger.error("service=product-service memory_usage=95% heap_size=1.8GB/2GB")
        logger.error("Garbage collection frequency increased significantly")
        logger.error("OutOfMemoryError: Java heap space in product catalog service")
        logger.critical("Service restart required - memory leak detected in image processing")
        self.services['product-service']['status'] = 'critical'
        
    def _configuration_error(self):
        logger.error("CONFIGURATION MISMATCH DETECTED")
        logger.error("service=payment-service config=redis_timeout value=null expected=5000ms")
        logger.error("Redis connection failed: NoneType object has no attribute 'decode'")
        logger.error("Payment processing halted - cache unavailable")
        logger.critical("Configuration rollback required for payment-service")
        self.services['payment-service']['status'] = 'down'
        
    def _third_party_api_failure(self):
        logger.error("EXTERNAL API FAILURE")
        logger.error("api=stripe-payments status=503 error=service_unavailable")
        logger.error("Payment gateway timeout after 30s - retrying with exponential backoff")
        logger.error("Order completion rate dropped to 23%")
        logger.critical("Fallback payment processor not configured")
        
    def _high_cpu_usage(self):
        logger.error("HIGH CPU UTILIZATION ALERT")
        logger.error("service=user-service cpu_usage=89% threads=156 load_avg=4.2")
        logger.error("Authentication requests queuing - average response time 12s")
        logger.error("Login success rate dropped to 67%")
        logger.critical("Auto-scaling threshold reached - no available instances")
        self.services['user-service']['cpu_usage'] = 89
        
    def _disk_space_issue(self):
        logger.error("DISK SPACE CRITICAL")
        logger.error("disk_usage=96% available=2.3GB path=/var/logs/")
        logger.error("Log rotation failed - disk write errors detected")
        logger.error("Application logging disabled to prevent system crash")
        logger.critical("Manual intervention required - disk cleanup needed")
        
    def _network_timeout(self):
        logger.error("NETWORK CONNECTIVITY ISSUES")
        logger.error("service=order-service target=inventory-api timeout=30s retries=3")
        logger.error("Inventory check failed - stock verification unavailable")
        logger.error("Order processing delayed - customer notifications sent")
        logger.critical("Network latency increased to 2.3s average")
        
    def _authentication_failure(self):
        logger.error("AUTHENTICATION SERVICE FAILURE")
        logger.error("service=user-service auth_provider=oauth2 error=invalid_token")
        logger.error("JWT token validation failed - signature mismatch")
        logger.error("User session termination rate: 94%")
        logger.critical("Security breach potential - immediate investigation required")

    def generate_access_logs(self):
        """Generate realistic access log entries"""
        # Create separate access logger
        access_logger = logging.getLogger('access')
        access_logger.setLevel(logging.INFO)
        
        # Remove any existing handlers to avoid duplicates
        access_logger.handlers.clear()
        
        # Create access log handler
        access_handler = logging.FileHandler(access_log_file)
        access_handler.setFormatter(logging.Formatter('%(message)s'))
        access_logger.addHandler(access_handler)
        access_logger.propagate = False  # Prevent propagation to parent logger
        
        # Simulate HTTP requests to different services
        endpoints = [
            ('/users/123', 'GET', 8001),
            ('/users/456', 'GET', 8001),
            ('/products', 'GET', 8002),
            ('/products/search', 'GET', 8002),
            ('/orders', 'POST', 8003),
            ('/orders/789', 'GET', 8003),
            ('/payments', 'POST', 8004),
            ('/health', 'GET', random.choice([8001, 8002, 8003, 8004]))
        ]
        
        user_agents = [
            'curl/7.68.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'PostmanRuntime/7.28.4',
            'monitoring/1.0',
            'python-requests/2.28.2'
        ]
        
        for _ in range(random.randint(10, 25)):
            endpoint, method, port = random.choice(endpoints)
            user_agent = random.choice(user_agents)
            
            # Determine status code based on service health
            service_name = f"{list(self.services.keys())[port-8001]}"
            service_status = self.services[service_name]['status']
            
            if service_status == 'running':
                status_code = random.choices([200, 201, 400, 404], weights=[85, 5, 7, 3])[0]
            elif service_status == 'degraded':
                status_code = random.choices([200, 500, 502, 503], weights=[60, 20, 10, 10])[0]
            elif service_status == 'critical':
                status_code = random.choices([500, 502, 503, 504], weights=[40, 20, 30, 10])[0]
            else:  # down
                status_code = random.choices([502, 503, 504], weights=[30, 50, 20])[0]
            
            response_size = random.randint(45, 2048)
            timestamp = datetime.now().strftime('%d/%b/%Y:%H:%M:%S +0000')
            
            access_entry = f'127.0.0.1 - - [{timestamp}] "{method} {endpoint} HTTP/1.1" {status_code} {response_size} "-" "{user_agent}"'
            access_logger.info(access_entry)

    def generate_metrics(self):
        """Generate realistic metrics for monitoring"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'services': {},
            'system': {
                'cpu_usage': random.randint(15, 95),
                'memory_usage': random.randint(30, 88),
                'disk_usage': random.randint(45, 97),
                'network_latency': random.uniform(0.1, 3.2)
            }
        }
        
        for service, config in self.services.items():
            metrics['services'][service] = {
                'status': config['status'],
                'response_time': random.uniform(0.1, 5.0),
                'error_rate': random.uniform(0, 15.5) if config['status'] != 'running' else random.uniform(0, 2.1),
                'throughput': random.randint(50, 1200),
                'cpu_usage': config.get('cpu_usage', random.randint(10, 45))
            }
        
        logger.info(f"METRICS: {json.dumps(metrics, indent=2)}")
        return metrics

    def health_check(self):
        """Perform health checks on all services"""
        logger.info("=== HEALTH CHECK STARTED ===")
        
        for service, config in self.services.items():
            status = config['status']
            port = config['port']
            
            if status == 'running':
                logger.info(f"✅ {service} (port {port}): HEALTHY")
            elif status == 'degraded':
                logger.warning(f"⚠️  {service} (port {port}): DEGRADED - Performance issues detected")
            elif status == 'critical':
                logger.error(f"🔥 {service} (port {port}): CRITICAL - Immediate attention required")
            elif status == 'down':
                logger.critical(f"❌ {service} (port {port}): DOWN - Service unavailable")
        
        logger.info("=== HEALTH CHECK COMPLETED ===")

    def run_load_test(self):
        """Simulate load testing that triggers issues"""
        logger.info("🔄 Starting load test simulation...")
        
        # Simulate concurrent requests
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for i in range(10):
                future = executor.submit(self._simulate_request, f"request_{i}")
                futures.append(future)
            
            # Wait for completion and potentially trigger errors
            for future in futures:
                try:
                    future.result(timeout=2)
                except Exception as e:
                    logger.error(f"Load test request failed: {str(e)}")
        
        logger.info("Load test completed")

    def _simulate_request(self, request_id):
        """Simulate individual service requests"""
        # Random delay to simulate processing
        time.sleep(random.uniform(0.1, 1.5))
        
        # Random chance of failure during load test
        if random.random() < 0.3:
            service = random.choice(list(self.services.keys()))
            logger.error(f"Request {request_id} failed on {service}: Connection timeout")
            raise Exception(f"Service {service} unavailable")
        
        logger.info(f"Request {request_id} completed successfully")

def main():
    """Main execution function that generates various scenarios for postmortem analysis"""
    print("🚀 Starting E-commerce Platform Simulation")
    print("=" * 60)
    
    platform = EcommercePlatform()
    
    try:
        # Initial health check
        platform.health_check()
        time.sleep(2)
        
        # Generate baseline metrics
        logger.info("📊 Generating baseline metrics...")
        platform.generate_metrics()
        
        # Generate initial access logs
        logger.info("🌐 Generating access logs...")
        platform.generate_access_logs()
        time.sleep(2)
        
        # Simulate normal operations for a few seconds
        logger.info("✅ Platform running normally...")
        time.sleep(3)
        
        # Start load testing
        platform.run_load_test()
        time.sleep(2)
        
        # Trigger multiple incidents (this is what creates issues for analysis)
        logger.info("🎯 Simulating incident scenarios...")
        for i in range(random.randint(2, 4)):
            platform.simulate_incident()
            time.sleep(random.uniform(1, 3))
            platform.generate_metrics()
            # Generate access logs after each incident
            platform.generate_access_logs()
        
        # Final health check after incidents
        time.sleep(2)
        platform.health_check()
        
        # Generate final metrics
        final_metrics = platform.generate_metrics()
        
        print("\n" + "=" * 60)
        print("🏁 Simulation completed!")
        print("📝 Check logs/ directory for detailed incident logs")
        print("🔍 Run your postmortem automation platform on these logs")
        print("=" * 60)
        
    except KeyboardInterrupt:
        logger.info("🛑 Platform simulation interrupted by user")
        print("\nSimulation stopped by user")
    except Exception as e:
        logger.critical(f"💥 FATAL ERROR: {str(e)}")
        print(f"\nFatal error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()