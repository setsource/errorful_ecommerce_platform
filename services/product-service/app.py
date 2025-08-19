# services/product-service/app.py
from flask import Flask, jsonify
import logging
import gc
import random

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Memory leak simulation
memory_hog = []

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'product-service'})

@app.route('/products')
def get_products():
    global memory_hog
    
    # Simulate memory leak
    for i in range(1000):
        memory_hog.append([0] * 1000)  # Intentional memory leak
    
    # Simulate image processing errors
    if random.random() < 0.2:
        logger.error("OutOfMemoryError: Java heap space in image processing")
        return jsonify({'error': 'Memory exhausted'}), 500
    
    return jsonify({'products': ['Product 1', 'Product 2']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
