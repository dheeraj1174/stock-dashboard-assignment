from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.services import (
    fetch_stock_data,
    process_stock_data,
    stock_summary,
    compare_stocks
)



app = FastAPI(title="Stock Data Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API is running"}


@app.get("/companies")
def list_companies():
    return [
        {"symbol": "INFY.NS", "name": "Infosys"},
        {"symbol": "TCS.NS", "name": "Tata Consultancy Services"},
        {"symbol": "RELIANCE.NS", "name": "Reliance Industries"},
        {"symbol": "HDFCBANK.NS", "name": "HDFC Bank"}
    ]


@app.get("/data/{symbol}")
def get_stock_data(symbol: str):
    df = fetch_stock_data(symbol)
    df = process_stock_data(df)
    return df.tail(30).to_dict(orient="records")


@app.get("/summary/{symbol}")
def get_stock_summary(symbol: str):
    df = fetch_stock_data(symbol)
    df = process_stock_data(df)
    return stock_summary(df)


@app.get("/compare")
def compare(
    symbol1: str = Query(..., description="First stock symbol"),
    symbol2: str = Query(..., description="Second stock symbol")
):
    df1 = process_stock_data(fetch_stock_data(symbol1))
    df2 = process_stock_data(fetch_stock_data(symbol2))
    return compare_stocks(df1, df2)
