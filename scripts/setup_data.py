#!/usr/bin/env python3
"""
Initial data setup script for MLTR.
Downloads sample historical data for testing and development.
"""

import argparse
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf
from loguru import logger
from tqdm import tqdm


# NSE to Yahoo Finance suffix mapping
NSE_SUFFIX = ".NS"
BSE_SUFFIX = ".BO"

# Predefined symbol universes
UNIVERSES = {
    "NIFTY50": [
        "RELIANCE", "TCS", "HDFCBANK", "INFY", "HINDUNILVR", "ICICIBANK", "KOTAKBANK",
        "BHARTIARTL", "ITC", "LT", "AXISBANK", "SBIN", "BAJFINANCE", "ASIANPAINT",
        "MARUTI", "HCLTECH", "SUNPHARMA", "TITAN", "WIPRO", "ULTRACEMCO", "NESTLEIND",
        "TECHM", "POWERGRID", "NTPC", "TATASTEEL", "ONGC", "BAJAJFINSV", "M&M",
        "DIVISLAB", "ADANIPORTS", "HEROMOTOCO", "GRASIM", "CIPLA", "DRREDDY",
        "EICHERMOT", "TATACONSUM", "HINDALCO", "BRITANNIA", "COALINDIA", "SHREECEM",
        "UPL", "INDUSINDBK", "JSWSTEEL", "BAJAJ-AUTO", "TATAMOTORS", "APOLLOHOSP",
        "BPCL", "SBILIFE", "HDFCLIFE"
    ],
    "NIFTY100": [],  # Extend as needed
    "NIFTY200": [],
    "NIFTY500": [],
}


def get_symbols(universe: str, custom_symbols: list = None) -> list:
    """Get list of symbols for the specified universe."""
    if custom_symbols:
        return custom_symbols

    if universe.upper() not in UNIVERSES:
        logger.error(f"Unknown universe: {universe}")
        logger.info(f"Available universes: {list(UNIVERSES.keys())}")
        return []

    symbols = UNIVERSES[universe.upper()]
    logger.info(f"Selected {len(symbols)} symbols from {universe}")
    return symbols


def download_symbol_data(
    symbol: str,
    start_date: str,
    end_date: str,
    exchange: str = "NSE"
) -> pd.DataFrame:
    """Download historical data for a single symbol."""
    suffix = NSE_SUFFIX if exchange == "NSE" else BSE_SUFFIX
    ticker = f"{symbol}{suffix}"

    try:
        df = yf.download(ticker, start=start_date, end=end_date, progress=False)

        if df.empty:
            logger.warning(f"No data returned for {symbol}")
            return pd.DataFrame()

        # Flatten column multi-index if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Standardize column names
        df.columns = [col.lower() for col in df.columns]

        # Add symbol column
        df['symbol'] = symbol

        # Reset index to make date a column
        df.reset_index(inplace=True)
        df.rename(columns={'date': 'timestamp'}, inplace=True)

        logger.debug(f"Downloaded {len(df)} rows for {symbol}")
        return df

    except Exception as e:
        logger.error(f"Error downloading {symbol}: {e}")
        return pd.DataFrame()


def save_data(df: pd.DataFrame, output_dir: Path, format: str = "parquet"):
    """Save data to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)

    if format == "parquet":
        output_file = output_dir / "ohlcv_data.parquet"
        df.to_parquet(output_file, index=False)
        logger.info(f"Saved {len(df)} rows to {output_file}")

    elif format == "csv":
        output_file = output_dir / "ohlcv_data.csv"
        df.to_csv(output_file, index=False)
        logger.info(f"Saved {len(df)} rows to {output_file}")

    else:
        logger.error(f"Unsupported format: {format}")


def main():
    parser = argparse.ArgumentParser(description="Download historical market data for MLTR")

    parser.add_argument(
        "--universe",
        type=str,
        default="NIFTY50",
        choices=list(UNIVERSES.keys()),
        help="Symbol universe to download"
    )
    parser.add_argument(
        "--symbols",
        type=str,
        nargs="+",
        help="Custom list of symbols (overrides universe)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=730,
        help="Number of days of historical data (default: 730 = 2 years)"
    )
    parser.add_argument(
        "--start",
        type=str,
        help="Start date (YYYY-MM-DD). Overrides --days"
    )
    parser.add_argument(
        "--end",
        type=str,
        help="End date (YYYY-MM-DD). Default: today"
    )
    parser.add_argument(
        "--exchange",
        type=str,
        default="NSE",
        choices=["NSE", "BSE"],
        help="Stock exchange (default: NSE)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/raw/market",
        help="Output directory"
    )
    parser.add_argument(
        "--format",
        type=str,
        default="parquet",
        choices=["parquet", "csv"],
        help="Output format"
    )

    args = parser.parse_args()

    # Configure logger
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), format="{message}")

    # Calculate date range
    if args.end:
        end_date = args.end
    else:
        end_date = datetime.now().strftime("%Y-%m-%d")

    if args.start:
        start_date = args.start
    else:
        start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")

    logger.info(f"Date range: {start_date} to {end_date}")

    # Get symbols
    symbols = get_symbols(args.universe, args.symbols)

    if not symbols:
        logger.error("No symbols to download. Exiting.")
        return

    # Download data
    logger.info(f"Downloading data for {len(symbols)} symbols...")
    all_data = []

    for symbol in tqdm(symbols, desc="Downloading"):
        df = download_symbol_data(symbol, start_date, end_date, args.exchange)
        if not df.empty:
            all_data.append(df)

    if not all_data:
        logger.error("No data downloaded. Exiting.")
        return

    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    logger.info(f"Total rows downloaded: {len(combined_df)}")

    # Save data
    output_dir = Path(args.output)
    save_data(combined_df, output_dir, args.format)

    # Print summary statistics
    logger.info("\n=== Summary ===")
    logger.info(f"Symbols: {combined_df['symbol'].nunique()}")
    logger.info(f"Date range: {combined_df['timestamp'].min()} to {combined_df['timestamp'].max()}")
    logger.info(f"Total rows: {len(combined_df)}")
    logger.info(f"Output: {output_dir / f'ohlcv_data.{args.format}'}")

    logger.success("\n✓ Data setup complete!")


if __name__ == "__main__":
    main()
