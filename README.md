# Monitoring Stack with Prometheus and Grafana

A complete monitoring solution using Prometheus for metrics collection and Grafana for visualization.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Monitoring Stack Architecture                        │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                        Your Application                            │  │
│  │   ┌─────────────────────────────────────────────────────────────┐ │  │
│  │   │                    Flask App (:8080)                        │ │  │
│  │   │                                                             │ │  │
│  │   │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │ │  │
│  │   │   │  /metrics    │  │  /health     │  │  /data       │    │ │  │
│  │   │   │ Prometheus   │  │  Health      │  │  Business    │    │ │  │
│  │   │   │  Metrics     │  │  Checks      │  │  Endpoints   │    │ │  │
│  │   │   └──────────────┘  └──────────────┘  └──────────────┘    │ │  │
│  │   └─────────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                      │                                    │
│                                      │ Scrapes (:8080/metrics)           │
│                                      ▼                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                        Prometheus (:9090)                          │  │
│  │                                                                   │  │
│  │   • Metrics Collection (every 5s)                                 │  │
│  │   • Alert Rules Evaluation                                        │  │
│  │   • Time Series Storage                                           │  │
│  │   • PromQL Queries                                                 │  │
│  │                                                                   │  │
│  │   ┌─────────────────────────────────────────────────────────────┐ │  │
│  │   │ Alert Rules                                                 │ │  │
│  │   │  • HighErrorRate     (>10% errors)                         │ │  │
│  │   │  • ServiceDown       (up==0)                                │ │  │
│  │   │  • HighLatency       (p95>0.5s)                             │ │  │
│  │   │  • HighQueueSize     (>80 items)                           │ │  │
│  │   └─────────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                      │                                    │
│                                      │ Query                              │
│                                      ▼                                    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                        Grafana (:3000)                            │  │
│  │                                                                   │  │
│  │   ┌─────────────────────────────────────────────────────────────┐ │  │
│  │   │ Dashboards                                                   │ │  │
│  │   │                                                             │ │  │
│  │   │  • Request Rate        • Items Processed                    │ │  │
│  │   │  • Request Latency     • Queue Size                         │ │  │
│  │   │  • Error Rate          • Active Requests                    │ │  │
│  │   │  • Service Status      • P95 Latency                        │ │  │
│  │   └─────────────────────────────────────────────────────────────┘ │  │
│  │                                                                   │  │
│  │   Default Login: admin / admin                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                        cAdvisor (:8081)                            │  │
│  │   Container metrics (CPU, Memory, Network)                         │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Tech Stack

![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-000000?style=for-the-badge&logo=prometheus&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![cAdvisor](https://img.shields.io/badge/cAdvisor-000000?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## Components

### Application (`app/`)
- Flask application with custom Prometheus metrics
- Exposes `/metrics` endpoint for Prometheus scraping
- Includes business metrics: items processed, queue size
- Health and readiness endpoints

### Prometheus (`prometheus/`)
- Metrics collection every 5 seconds
- Alert rules for common failure scenarios
- Time-series data storage
- Remote write capability (for production)

### Grafana (`grafana/`)
- Pre-configured datasource (Prometheus)
- Application monitoring dashboard
- Auto-provisioned dashboards and datasources
- Dark theme UI

### cAdvisor
- Container resource metrics
- CPU, memory, network usage
- Per-container monitoring

## Metrics Exposed

### HTTP Metrics
- `http_requests_total` - Total HTTP requests (counter)
- `http_request_duration_seconds` - Request latency histogram
- `http_requests_active` - Active requests (gauge)

### Business Metrics
- `items_processed_total` - Items processed (counter)
- `queue_size` - Current queue size (gauge)
- `app_version_info` - Application version (gauge)

## How to Run

### Prerequisites
- Docker and Docker Compose

### Start the Stack

```bash
# Navigate to project directory
cd 4-monitoring-stack

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### Access Services

| Service | URL | Default Credentials |
|---------|-----|--------------------|
| Application | http://localhost:8080 | - |
| API Health | http://localhost:8080/health | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin / admin |
| cAdvisor | http://localhost:8081 | - |

### View Metrics

```bash
# Application metrics
curl http://localhost:8080/metrics

# Trigger some traffic
curl http://localhost:8080/data
curl -X POST http://localhost:8080/process
```

### Grafana Dashboard

1. Open http://localhost:3000
2. Login with `admin` / `admin`
3. Navigate to Dashboards → Browse
4. Open "Application Monitoring Dashboard"

## How to Deploy for FREE

### Option 1: Local with Docker (100% Free)
```bash
# Already covered above - completely free
docker-compose up -d
```

### Option 2: Raspberry Pi / Home Lab (Free Forever)
- Install Docker on Raspberry Pi
- Run the same docker-compose
- Access via local IP

### Option 3: Cloud Free Tiers
| Provider | Service | Free Tier |
|----------|---------|-----------|
| Grafana Cloud | Hosted Grafana | 3k hours/month free |
| Prometheus | Managed | $0/vCPU/month |
| AWS | EKS | $0.10/hour after free tier |
| Google Cloud | GKE | $75 credit/month |

### Recommended for Learning
Use the local Docker Compose setup - it's production-like and costs nothing.

## Alert Rules Explained

```yaml
HighErrorRate:    # Alert when error rate > 10%
ServiceDown:      # Alert when service stops responding
HighLatency:      # Alert when p95 latency > 500ms
HighQueueSize:    # Alert when queue backs up
LowProcessingRate: # Alert when throughput drops
```

## Project Structure

```
4-monitoring-stack/
├── docker-compose.yml
├── prometheus.yml              # Root config (for local testing)
├── README.md
├── app/
│   ├── app.py                  # Flask app with Prometheus metrics
│   ├── Dockerfile
│   └── requirements.txt
├── prometheus/
│   ├── prometheus.yml          # Prometheus configuration
│   └── alert.rules.yml         # Alert rules
└── grafana/
    └── provisioning/
        ├── dashboards/
        │   ├── dashboard.yml
        │   └── app-dashboard.json
        └── datasources/
            └── datasource.yml
```

## Troubleshooting

### Prometheus not scraping?
```bash
# Check targets
curl http://localhost:9090/api/v1/targets

# Check metrics are exposed
curl http://localhost:8080/metrics | head -20
```

### Grafana dashboards not showing?
```bash
# Check datasource
curl http://localhost:3000/api/datasources

# Check logs
docker-compose logs grafana
```

### Container metrics missing?
```bash
# cAdvisor needs privileged access
docker-compose up -d cadvisor
```

## License

MIT License - See LICENSE file for details.
