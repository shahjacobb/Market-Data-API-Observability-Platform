# Market Data API Observability Platform

A real-time observability platform that monitors and analyzes requests to the YFinance API. Built with FastAPI, using Prometheus for metrics collection and querying, and Grafana dashboards for visualization. Each service runs in its own Docker container for easy deployment and scaling.

## Features
- Real-time and historical stock data via YFinance
- Prometheus metrics for monitoring API performance
- FastAPI backend with built-in API docs
- Grafana dashboards for data visualization
- Containerized architecture with Docker

## Current Implementation

### API Setup
Run FastAPI locally:
1. `cd backend/`
2. `uvicorn src.main:app --reload`
3. API runs at http://localhost:8000

### Working Endpoints
Install jq to format the JSON output:
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

### Metrics Implementation
FastAPI exposes these Prometheus metrics at `/metrics`:
- Request counts by endpoint
- Request latency measurements
- Stock symbol request frequency
- Error tracking by type
- Stock price fetch latency
- Successful vs failed YFinance calls
- Number of unique symbols requested

### Docker & Prometheus Setup
Prometheus needs Docker to scrape metrics. Here's how to get both services running:

1. Start Docker Desktop
2. Run the services:
```bash
docker-compose up -d
```

You should see something like this (services starting up):
<img width="1000" alt="docker_startup_logs" src="https://github.com/user-attachments/assets/docker_startup_logs.png" />

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
<img width="1000" alt="market_data_requests_prom" src="https://github.com/user-attachments/assets/market_data_requests_prom.png" />

The graph breaks down API usage - you can see the mix of price lookups, historical data pulls, and info requests.

#### 2. Stock Symbol Analytics
See which stocks are being queried:
```promql
# Requests per symbol
stock_symbol_requests_total
```

Request count by symbol:
<img width="1000" alt="symbol_requests_prom" src="https://github.com/user-attachments/assets/symbol_requests_prom.png" />

Shows request volume per stock symbol over time (AAPL, GOOGL, MSFT).

### Development Status
#### ✅ Done
- [x] YFinance API Integration
  - [x] Real-time price endpoint
  - [x] Historical data endpoint
  - [x] Company info endpoint
  - [x] Dividend data endpoint
  - [x] Earnings data endpoint
- [x] Prometheus Metrics
  - [x] Request counting
  - [x] Latency tracking
  - [x] Error monitoring
  - [x] YFinance call success rate

#### In Progress
- JSON serialization for complex data types (numpy/pandas)
- Type conversion implementation:
  - Date formatting in historical data
  - Strike prices in options chain
  - Dividend history formatting
  - Earnings data number formatting

#### Planned Features
- Docker containerization
- Grafana dashboard setup
- Additional endpoints:
  - Batch Stock Data (`/stocks/batch`)
  - Options Chain (`/stock/{ticker}/options`)

## Requirements
- Python 3.9 or newer
- Docker Desktop (for containerized deployment)

## License
MIT License - do whatever you want with this!
