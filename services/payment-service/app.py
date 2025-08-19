# services/payment-service/app.py
from flask import Flask, jsonify, request
import logging
import requests
import random

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Intentional configuration issue
STRIPE_API_KEY = None  # Missing configuration
PAYMENT_TIMEOUT = 30

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'payment-service'})

@app.route('/payments', methods=['POST'])
def process_payment():
    payment_data = request.json
    
    if not STRIPE_API_KEY:
        logger.error("Payment gateway configuration missing: API key not found")
        return jsonify({'error': 'Configuration error'}), 500
    
    try:
        # Simulate external API call that fails
        if random.random() < 0.3:
            logger.error("Stripe API returned 503: Service temporarily unavailable")
            return jsonify({'error': 'Payment gateway unavailable'}), 503
        
        # Simulate authentication failures
        if random.random() < 0.2:
            logger.error("Payment authentication failed: Invalid merchant credentials")
            return jsonify({'error': 'Authentication failed'}), 401
        
        return jsonify({'payment_id': payment_data.get('id'), 'status': 'processed'})
    
    except Exception as e:
        logger.error(f"Payment processing failed: {str(e)}")
        return jsonify({'error': 'Payment failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8004)