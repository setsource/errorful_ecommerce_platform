# services/order-service/app.py
from flask import Flask, jsonify, request
import logging
import redis
import json

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Intentional configuration error
try:
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True, socket_timeout=None)  # Bug: timeout=None
except Exception as e:
    logger.error(f"Redis connection failed: {str(e)}")
    redis_client = None

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'order-service'})

@app.route('/orders', methods=['POST'])
def create_order():
    try:
        order_data = request.json
        
        # This will fail due to redis timeout configuration
        if redis_client:
            redis_client.set(f"order_{order_data.get('id')}", json.dumps(order_data))
        
        # Simulate order processing delay
        if random.random() < 0.25:
            logger.error("Order processing timeout - inventory service unreachable")
            return jsonify({'error': 'Inventory check failed'}), 502
        
        return jsonify({'order_id': order_data.get('id'), 'status': 'created'})
    
    except Exception as e:
        logger.error(f"Order creation failed: {str(e)}")
        return jsonify({'error': 'Order processing failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003)

