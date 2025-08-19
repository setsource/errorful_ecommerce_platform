# services/user-service/app.py
from flask import Flask, jsonify, request
import logging
import time
import random

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated database connection issues
CONNECTION_POOL_SIZE = 20
active_connections = 0

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'user-service'})

@app.route('/users/<user_id>')
def get_user(user_id):
    global active_connections
    
    # Simulate connection pool exhaustion
    if active_connections >= CONNECTION_POOL_SIZE:
        logger.error(f"Connection pool exhausted: {active_connections}/{CONNECTION_POOL_SIZE}")
        return jsonify({'error': 'Database unavailable'}), 503
    
    active_connections += 1
    
    # Simulate slow database queries
    time.sleep(random.uniform(0.1, 2.0))
    
    # Random failure for incident simulation
    if random.random() < 0.15:
        logger.error(f"Database timeout for user {user_id}")
        return jsonify({'error': 'Query timeout'}), 500
    
    active_connections -= 1
    return jsonify({'user_id': user_id, 'name': f'User {user_id}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

