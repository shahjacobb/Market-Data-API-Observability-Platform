from fastapi import FastAPI, HTTPException, Query
from typing import Optional
import yfinance as yf
from datetime import datetime
from .routes import options

app = FastAPI(title="Market Data API")

# Include only options router
app.include_router(options.router)

# Core endpoints
@app.get("/")
async def health_check():
    """health check endpoint to verify api is running"""
    return {"status": "online", "timestamp": datetime.now().isoformat()}

@app.get("/stock/{ticker}/price")
async def get_current_price(ticker: str):
    """get latest stock price and volume data for a single ticker"""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d')
        if not data.empty:
            return {
                "ticker": ticker,
                "current_price": float(data['Close'].iloc[-1]),
                "volume": int(data['Volume'].iloc[-1]),
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stock/{ticker}/historical")
async def get_historical_data(
    ticker: str,
    interval: str = Query(default='1d', description="Data interval (1d, 1wk, 1mo)"),
    period: str = Query(default='1mo', description="Historical period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")
):
    """get historical price data with customizable intervals and time periods"""
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period=period, interval=interval)
        
        if history.empty:
            raise HTTPException(status_code=404, detail=f"No data found for ticker {ticker}")
            
        return {
            "ticker": ticker,
            "interval": interval,
            "period": period,
            "data_points": len(history),
            "history": history.to_dict(orient='index')
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stock/{ticker}/info")
async def get_company_info(ticker: str):
    """Get company profile and information"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Return only essential company information
        essential_info = {
            "ticker": ticker,
            "company_info": {
                "longName": info.get("longName"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "website": info.get("website"),
                "marketCap": info.get("marketCap"),
                "employees": info.get("fullTimeEmployees"),
                "country": info.get("country"),
                "city": info.get("city"),
                "summary": info.get("longBusinessSummary"),
                "currency": info.get("currency"),
                "exchange": info.get("exchange")
            }
        }
        return essential_info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stock/{ticker}/dividends")
async def get_dividend_data(ticker: str):
    """Get dividend history"""
    try:
        stock = yf.Ticker(ticker)
        dividends = stock.dividends
        return {
            "ticker": ticker,
            "dividend_history": dividends.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stock/{ticker}/earnings")
async def get_earnings_data(
    ticker: str,
    frequency: str = Query(default='yearly', description="Data frequency (yearly or quarterly)")
):
    """Get company earnings data"""
    try:
        stock = yf.Ticker(ticker)
        earnings = stock.get_earnings(freq=frequency)
        return {
            "ticker": ticker,
            "frequency": frequency,
            "earnings_data": earnings.to_dict() if not earnings.empty else {}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/stocks/batch")
async def get_multiple_stocks(
    tickers: str = Query(..., description="Comma-separated list of tickers (e.g., AAPL,MSFT,GOOGL)")
):
    """Get current price for multiple stocks"""
    try:
        ticker_list = tickers.split(',')
        stocks = yf.Tickers(' '.join(ticker_list))
        
        results = {}
        for ticker in ticker_list:
            try:
                data = stocks.tickers[ticker].history(period='1d')
                if not data.empty:
                    results[ticker] = {
                        "current_price": data['Close'].iloc[-1],
                        "volume": data['Volume'].iloc[-1]
                    }
            except:
                results[ticker] = {"error": "Failed to fetch data"}
                
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
