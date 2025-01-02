"""
metrics collection module using prometheus. tracks api requests, latency, and errors.
prometheus works by exposing these metrics at an endpoint that it periodically scrapes
"""

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from functools import wraps

# core metrics for monitoring - each metric is either a counter (goes up)
# or histogram (tracks distribution of values like response times)

# basic request tracking - increments by 1 for each endpoint hit
REQUEST_COUNT = Counter(
    'market_data_requests_total',
    'Total number of requests by endpoint',
    ['endpoint']  # labels let us break down metrics by different dimensions
)

# latency tracking - stores request times in buckets to see performance distribution
REQUEST_LATENCY = Histogram(
    'market_data_request_latency_seconds',
    'Request latency in seconds',
    ['endpoint']
)

# monitor external api usage - similar to request latency but for external calls
YFINANCE_CALLS = Histogram(
    'yfinance_api_duration_seconds',
    'YFinance API call duration in seconds',
    ['operation']  # different types of yfinance operations we're timing
)

# track popular symbols - helps understand what stocks users care about
SYMBOL_REQUESTS = Counter(
    'stock_symbol_requests_total',
    'Number of requests by stock symbol',
    ['symbol']  # break down by stock ticker
)

# error tracking - groups errors by type to spot patterns
ERROR_COUNT = Counter(
    'market_data_errors_total',
    'Total number of errors by type',
    ['error_type']  # python exception names
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    """middleware that handles request metrics and error tracking.
    sits between fastapi and our routes to measure all requests automatically"""
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # grab endpoint path for labeling metrics
        endpoint = request.url.path
        REQUEST_COUNT.labels(endpoint=endpoint).inc()
        
        try:
            response = await call_next(request)
            # calculate time taken in seconds
            duration = time.time() - start_time
            REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)
            return response
        except Exception as e:
            # track what kind of error occurred
            ERROR_COUNT.labels(error_type=type(e).__name__).inc()
            raise

def track_symbol_request(symbol: str):
    """logs requests for specific stock symbols. called manually when
    handling stock-specific endpoints"""
    SYMBOL_REQUESTS.labels(symbol=symbol).inc()

def track_yfinance_operation(operation_name: str):
    """decorator that times yfinance api calls. wraps async functions to measure
    how long external api operations take"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # use context manager to time the operation
            with YFINANCE_CALLS.labels(operation=operation_name).time():
                return await func(*args, **kwargs)
        return wrapper
    return decorator

async def metrics_endpoint():
    """endpoint that prometheus scrapes for metrics. prometheus hits this
    endpoint on a schedule to collect all the metrics we've recorded"""
    return Response(
        generate_latest(),  # prometheus client formats all metrics for scraping
        media_type=CONTENT_TYPE_LATEST
    ) 