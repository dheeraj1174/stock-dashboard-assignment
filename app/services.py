import yfinance as yf
import pandas as pd


def fetch_stock_data(symbol: str) -> pd.DataFrame:
    """
    Fetch 1 year of daily stock data using yfinance
    """
    df = yf.download(
        symbol,
        period="1y",
        interval="1d",
        group_by="column",
        auto_adjust=False
    )
    df.reset_index(inplace=True)
    return df


def process_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean stock data and compute financial metrics
    """

    if df.empty:
        return df

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] if isinstance(col, tuple) else str(col) for col in df.columns]
    else:
        df.columns = [str(col) for col in df.columns]

    if 'Date' not in df.columns:
        df.reset_index(inplace=True)
        if 'Date' not in df.columns:
            for col in df.columns:
                if 'date' in col.lower():
                    df.rename(columns={col: 'Date'}, inplace=True)
                    break

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.dropna(subset=['Date'], inplace=True)

    for col in ['Open', 'Close']:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(subset=['Open', 'Close'], inplace=True)

    df.sort_values('Date', inplace=True)

    df['Daily_Return'] = (df['Close'] - df['Open']) / df['Open']
    df['MA_7'] = df['Close'].rolling(window=7).mean()
    df['Volatility'] = df['Daily_Return'].rolling(window=7).std()

    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    df['Daily_Return'] = df['Daily_Return'].round(4)
    df['MA_7'] = df['MA_7'].round(2)
    df['Volatility'] = df['Volatility'].round(4)

    df.reset_index(drop=True, inplace=True)

    return df


def stock_summary(df: pd.DataFrame) -> dict:
    """
    Calculate 52-week summary statistics
    """
    if df.empty:
        return {
            "52_week_high": None,
            "52_week_low": None,
            "average_close": None
        }

    return {
        "52_week_high": round(float(df['High'].max()), 2) if 'High' in df.columns else None,
        "52_week_low": round(float(df['Low'].min()), 2) if 'Low' in df.columns else None,
        "average_close": round(float(df['Close'].mean()), 2) if 'Close' in df.columns else None
    }


def compare_stocks(df1: pd.DataFrame, df2: pd.DataFrame) -> dict:
    """
    Compare two stocks based on average daily return
    """
    if df1.empty or df2.empty:
        return {
            "stock_1_avg_return": None,
            "stock_2_avg_return": None,
            "better_performer": None
        }

    avg_return_1 = df1['Daily_Return'].mean()
    avg_return_2 = df2['Daily_Return'].mean()

    return {
        "stock_1_avg_return": round(float(avg_return_1), 4),
        "stock_2_avg_return": round(float(avg_return_2), 4),
        "better_performer": "stock_1" if avg_return_1 > avg_return_2 else "stock_2"
    }
