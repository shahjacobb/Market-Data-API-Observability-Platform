# Market Data API Observability Platform

A real-time observability platform that monitors and analyzes requests to the YFinance API. Built with FastAPI, using Prometheus for metrics collection and querying, and Grafana dashboards for visualization. Each service runs in its own Docker container for easy deployment and scaling.

## Features
- Real-time and historical stock data via YFinance
- Prometheus metrics for monitoring API performance
- FastAPI backend with built-in API docs
- Grafana dashboards for data visualization
- Containerized architecture with Docker

## Current Implementation

### API Server Setup
To test the endpoints:
1. `cd backend/`
2. Start the server: `uvicorn src.main:app --reload`
3. The API will be available at `http://localhost:8000`

### Working Endpoints
If you're trying to test these endpoints with curl, download jq to pretty print the JSON responses:
```bash
brew install jq  # on macOS
```

Note: all endpoints are case sensitive - use uppercase tickers (AAPL not aapl)

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
The API includes Prometheus metrics to track performance:
- Request counts by endpoint
- Request latency measurements
- Stock symbol request frequency
- Error tracking by type
- Stock price fetch latency
- Successful vs failed YFinance calls
- Number of unique symbols requested

Access metrics at `/metrics` endpoint for Prometheus scraping.

### Setting Up Prometheus
If the Docker engine isn't running in the app, you won't be able to access Prometheus locally to run queries. Here's what you need to do:

1. Open Docker Desktop and wait for it to start up
2. Fire up the FastAPI server:
```bash
cd backend
uvicorn src.main:app --reload
```
3. Start Prometheus using Docker Compose:
```bash
docker-compose up -d
```

Once everything's running, you can access:
- FastAPI at http://localhost:8000
- Prometheus at http://localhost:9090 (this is where you'll run your queries)

### Testing Metrics Output

First, let's test some requests to our FastAPI server:
```bash
curl http://localhost:8000/stock/AAPL/price | jq '.' && echo -e "\n" && curl http://localhost:8000/stock/MSFT/price | jq '.' && echo -e "\n" && curl http://localhost:8000/stock/GOOGL/historical | jq '.'
```

Then check these queries in Prometheus:
```promql
# Query 1: Total requests by endpoint
market_data_requests_total

# Query 2: Requests by stock symbol
stock_symbol_requests_total
```

Response from endpoints:
<img width="635" alt="endpoints_responses" src="https://github.com/user-attachments/assets/25248dff-d54d-4484-beba-5a05f59c3a0a" />

Shows the price data for AAPL and MSFT, and historical data for GOOGL with customizable time intervals.

Here's the metrics these requests generated:

#### Endpoint Hit Counter
```bash
curl http://localhost:8000/metrics | grep market_data_requests_total
```

<img width="628" alt="endpoints_hits" src="https://github.com/user-attachments/assets/6737eb6f-2e83-48a7-b45c-da063f4a6cec" />

### Prometheus Metrics Visualization

Here's what we're tracking in Prometheus:

#### 1. API Traffic Patterns
Looking at how requests are spread across endpoints:
```promql
# Total requests by endpoint
market_data_requests_total
```

Total requests by endpoint:
<img width="1000" alt="market_data_requests_prom" src="https://github.com/user-attachments/assets/market_data_requests_prom.png" />

The graph breaks down API usage - you can see the mix of price lookups, historical data pulls, and info requests.

#### 2. Stock Symbol Analytics
Tracking which stocks people are looking up:
```promql
# Requests per symbol
stock_symbol_requests_total
```

Request count by symbol:
<img width="1000" alt="symbol_requests_prom" src="https://github.com/user-attachments/assets/symbol_requests_prom.png" />

Shows how many times each stock (AAPL, GOOGL, MSFT) was queried over time.

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


x