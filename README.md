# Market Data API Observability Platform

A real-time observability platform that monitors and analyzes requests to the YFinance API. Built with FastAPI, Prometheus for metrics collection and querying, and Grafana dashboards for visualization. Each service runs in its own Docker container for easy deployment and scaling using [Docker Compose](https://docs.docker.com/compose/).

## Features
- Real-time and historical stock data via YFinance
- Prometheus metrics for monitoring API performance
- FastAPI backend with built-in API docs
- Grafana dashboards for data visualization
- Containerized architecture with Docker

## Current Implementation and Local Setup Instructions

### API Setup
Run FastAPI locally:
1. `cd backend/`
2. `uvicorn src.main:app --reload`
3. API runs at http://localhost:8000

### Working Endpoints
You can install jq first to pretty print format the JSON output:
```bash
brew install jq  # on macOS
```

Use uppercase tickers (AAPL not aapl) for all endpoints:

1. **Health Check**
```bash
curl http://localhost:8000/ | jq '.'
```

2. **Stock Price**
```bash
curl http://localhost:8000/stock/AAPL/price | jq '.'
```

3. **Historical Data**
```bash
# Default 1-month data
curl http://localhost:8000/stock/AAPL/historical | jq '.'

# Custom period and interval
curl "http://localhost:8000/stock/AAPL/historical?interval=1wk&period=1y" | jq '.'
```

4. **Company Info**
```bash
curl http://localhost:8000/stock/AAPL/info | jq '.'
```

5. **Dividends**
```bash
curl http://localhost:8000/stock/AAPL/dividends | jq '.'
```

6. **Earnings Data**
```bash
curl http://localhost:8000/stock/AAPL/earnings | jq '.'
```

### Testing Endpoints
First, let's test some requests:
```bash
curl http://localhost:8000/stock/AAPL/price | jq '.' && echo -e "\n" && curl http://localhost:8000/stock/MSFT/price | jq '.' && echo -e "\n" && curl http://localhost:8000/stock/GOOGL/historical | jq '.'
```

Response from endpoints:

<img width="650" alt="endpoints_responses" src="https://github.com/user-attachments/assets/25248dff-d54d-4484-beba-5a05f59c3a0a" />

Shows the price data for AAPL and MSFT, and historical data for GOOGL (with customizable time intervals).

### Metrics Implementation
FastAPI exposes these Prometheus metrics at `[/metrics](https://github.com/shahjacobb/Market-Data-API-Observability-Platform/blob/main/backend/src/metrics.py)`:
- Request counts by endpoint
- Request latency measurements
- Stock symbol request frequency
- Stock price fetch latency
- Successful vs failed YFinance calls
- Number of unique symbols requested

### Docker & Prometheus Setup
Okay, so testing the FastAPI service can be done by just running `uvicorn`, but in order to test Prometheus and start querying, it needs a Docker container running. Here's how to get both services running together using Docker Compose:

1. Start Docker Desktop
2. Run the services:
```bash
docker-compose up -d
```

You should see something like this (Docker images being built and containers running):
<img width="703" alt="docker_container_startup_logs" src="https://github.com/user-attachments/assets/f68ba7b3-87e1-4860-bc22-89c7d6c4a8db" />

The logs show containers building and Prometheus starting to scrape metrics (those 200 OK responses from /metrics endpoint).

Services will be at:
- FastAPI: http://localhost:8000
- Prometheus: http://localhost:9090

### Using Prometheus
With our Docker containers running, you can now query the metrics in Prometheus. Here's what we're tracking:

#### 1. API Traffic Patterns
Check requests across endpoints:
```promql
# Total requests by endpoint
market_data_requests_total
```

Total requests by endpoint:
<img width="1454" alt="market_request_data_prom" src="https://github.com/user-attachments/assets/60d22cb5-e07e-4109-8c53-b5864029cd00" />

The graph breaks down API usage - you can see the mix of price lookups, historical data pulls, and info requests.

#### 2. Stock Symbol Analytics
See which stocks are being queried:
```promql
# Requests per symbol
stock_symbol_requests_total
```

Request count by symbol:
<img width="1451" alt="ticker_requests_counter_prom" src="https://github.com/user-attachments/assets/603e1e28-0c86-4615-b668-1053b490bfd2" />

Shows request volume per stock symbol over time (AAPL, GOOGL, MSFT).

### Development Status
#### Done
- [x] YFinance API Integration
  - [x] Real-time price endpoint
  - [x] Historical data endpoint
  - [x] Company info endpoint
  - [x] Dividend data endpoint
  - [x] Earnings data endpoint
- [x] docker
  - [x] FastAPI container
  - [x] Prometheus container
  - [x] Docker Compose setup
- [x] prometheus metrics
  - [x] Request counting
  - [x] Latency tracking
  - [x] Error monitoring

#### In Progress
**prometheus stuff**
  - [x] yfinance call success rate
  - [ ] response status tracking
  - [ ] yfinance error response details

**grafana**
- [ ] literally all of grafana

## Requirements
- Python 3.9 or newer
- Docker Desktop (for containerized deployment)

## License
MIT License - do whatever you want with this!
