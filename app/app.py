"""
Flask Application with Prometheus Metrics
"""

from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import random
import os

app = Flask(__name__)

# Configuration
SERVICE_NAME = "monitored-app"
VERSION = "1.0.0"

# Custom Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint'],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Number of active HTTP requests',
    ['endpoint']
)

APP_VERSION = Gauge(
    'app_version_info',
    'Application version info',
    ['version']
)

# Business metrics
ITEMS_PROCESSED = Counter(
    'items_processed_total',
    'Total items processed',
    ['status']
)

QUEUE_SIZE = Gauge(
    'queue_size',
    'Current queue size'
)

# Set version metric
APP_VERSION.labels(version=VERSION).set(1)


@app.route("/")
def home():
    """Home endpoint"""
    return jsonify({
        "service": SERVICE_NAME,
        "version": VERSION,
        "status": "running"
    })


@app.route("/health")
def health():
    """Health check"""
    return jsonify({"status": "healthy"})


@app.route("/ready")
def ready():
    """Readiness check"""
    return jsonify({"status": "ready"})


@app.route("/data")
def get_data():
    """Get some data (simulated)"""
    start_time = time.time()

    # Simulate processing
    time.sleep(random.uniform(0.01, 0.05))

    items = [
        {"id": 1, "name": "Item 1", "processed": True},
        {"id": 2, "name": "Item 2", "processed": True},
        {"id": 3, "name": "Item 3", "processed": False},
    ]

    # Track metrics
    REQUEST_COUNT.labels(method='GET', endpoint='/data', status='200').inc()
    REQUEST_LATENCY.labels(method='GET', endpoint='/data').observe(time.time() - start_time)
    ITEMS_PROCESSED.labels(status='success').inc(random.randint(1, 5))

    return jsonify({"items": items, "count": len(items)})


@app.route("/process", methods=["POST"])
def process():
    """Simulate item processing"""
    start_time = time.time()

    # Simulate random processing result
    success = random.random() > 0.1  # 90% success rate

    if success:
        ITEMS_PROCESSED.labels(status='success').inc()
        status_code = 200
    else:
        ITEMS_PROCESSED.labels(status='failure').inc()
        status_code = 500

    REQUEST_COUNT.labels(method='POST', endpoint='/process', status=str(status_code)).inc()
    REQUEST_LATENCY.labels(method='POST', endpoint='/process').observe(time.time() - start_time)

    return jsonify({
        "status": "success" if success else "failure",
        "processed": True
    }), status_code


@app.route("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    # Update queue size metric
    queue_size = random.randint(0, 100)
    QUEUE_SIZE.set(queue_size)

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.before_request
def before_request():
    """Track active requests"""
    endpoint = request.endpoint or 'unknown'
    ACTIVE_REQUESTS.labels(endpoint=endpoint).inc()


@app.after_request
def after_request(response):
    """Track request completion"""
    endpoint = request.endpoint or 'unknown'
    ACTIVE_REQUESTS.labels(endpoint=endpoint).dec()
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
