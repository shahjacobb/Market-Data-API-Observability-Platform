#!/bin/bash

# Popular tech stocks
for i in {1..5}; do
  curl -s http://localhost:8000/stock/AAPL/price | jq '.'
  curl -s http://localhost:8000/stock/MSFT/price | jq '.'
  curl -s http://localhost:8000/stock/GOOGL/price | jq '.'
  sleep 1
done

# Some errors
curl -s http://localhost:8000/stock/INVALID/price | jq '.'
curl -s http://localhost:8000/stock/NOTREAL/price | jq '.'

# Financial stocks
for i in {1..5}; do
  curl -s http://localhost:8000/stock/JPM/price | jq '.'
  curl -s http://localhost:8000/stock/GS/price | jq '.'
  curl -s http://localhost:8000/stock/BAC/price | jq '.'
  sleep 1
done

# Mix of endpoints
for i in {1..5}; do
  curl -s http://localhost:8000/stock/AAPL/historical | jq '.'
  curl -s http://localhost:8000/stock/MSFT/info | jq '.'
  curl -s http://localhost:8000/stock/GOOGL/dividends | jq '.'
  sleep 1
done

# Generate some more errors
curl -s http://localhost:8000/stock/FAKE/historical | jq '.'
curl -s http://localhost:8000/stock/TEST/info | jq '.'