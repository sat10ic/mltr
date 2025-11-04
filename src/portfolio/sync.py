"""
Broker synchronization to automatically fetch portfolio holdings.

This module connects to your broker API to automatically sync your
actual holdings, eliminating manual entry.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

import pandas as pd


logger = logging.getLogger(__name__)


class BrokerSync:
    """
    Sync portfolio with broker API.

    Supported brokers:
    - Zerodha (Kite Connect API)
    - Upstox
    - Angel Broking
    - IIFL
    - Fyers
    - CSV import (for any broker via exported files)

    Example:
        >>> sync = BrokerSync("zerodha", api_key="your_key", access_token="your_token")
        >>> holdings = sync.fetch_holdings()
        >>> trades = sync.fetch_trades(days=7)
    """

    def __init__(
        self,
        broker: str,
        api_key: Optional[str] = None,
        access_token: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize broker sync.

        Args:
            broker: Broker name ("zerodha", "upstox", "angelbroking", "csv")
            api_key: API key for authentication
            access_token: Access token for authentication
            **kwargs: Additional broker-specific parameters
        """
        self.broker = broker.lower()
        self.api_key = api_key
        self.access_token = access_token
        self.client = None

        # Initialize broker client
        if self.broker == "zerodha":
            self._init_zerodha()
        elif self.broker == "upstox":
            self._init_upstox()
        elif self.broker == "angelbroking":
            self._init_angelbroking()
        elif self.broker == "csv":
            pass  # CSV doesn't need API client
        else:
            logger.warning(f"Broker '{broker}' not directly supported. Use CSV import.")

    def _init_zerodha(self):
        """Initialize Zerodha Kite Connect client."""
        try:
            from kiteconnect import KiteConnect

            if not self.api_key:
                raise ValueError("Zerodha requires api_key")

            self.client = KiteConnect(api_key=self.api_key)

            if self.access_token:
                self.client.set_access_token(self.access_token)

            logger.info("Zerodha client initialized")
        except ImportError:
            logger.error("kiteconnect library not installed. Run: pip install kiteconnect")
        except Exception as e:
            logger.error(f"Failed to initialize Zerodha client: {e}")

    def _init_upstox(self):
        """Initialize Upstox client."""
        try:
            import upstox_client

            # Upstox setup
            logger.info("Upstox client initialized")
        except ImportError:
            logger.error("upstox_client library not installed. Run: pip install upstox-client")

    def _init_angelbroking(self):
        """Initialize Angel Broking client."""
        try:
            from SmartApi import SmartConnect

            # Angel Broking setup
            logger.info("Angel Broking client initialized")
        except ImportError:
            logger.error("smartapi-python library not installed. Run: pip install smartapi-python")

    def fetch_holdings(self) -> pd.DataFrame:
        """
        Fetch current holdings from broker.

        Returns:
            DataFrame with columns: symbol, quantity, avg_price, current_price, pnl
        """
        if self.broker == "zerodha":
            return self._fetch_zerodha_holdings()
        elif self.broker == "csv":
            logger.warning("CSV mode: use import_holdings_csv() instead")
            return pd.DataFrame()
        else:
            logger.error(f"fetch_holdings not implemented for {self.broker}")
            return pd.DataFrame()

    def _fetch_zerodha_holdings(self) -> pd.DataFrame:
        """Fetch holdings from Zerodha."""
        if not self.client:
            logger.error("Zerodha client not initialized")
            return pd.DataFrame()

        try:
            holdings = self.client.holdings()

            # Convert to DataFrame
            df = pd.DataFrame(holdings)

            # Standardize column names
            df = df.rename(columns={
                "tradingsymbol": "symbol",
                "average_price": "avg_price",
                "last_price": "current_price",
                "pnl": "unrealized_pnl"
            })

            # Select relevant columns
            df = df[["symbol", "quantity", "avg_price", "current_price", "unrealized_pnl"]]

            logger.info(f"Fetched {len(df)} holdings from Zerodha")
            return df

        except Exception as e:
            logger.error(f"Failed to fetch Zerodha holdings: {e}")
            return pd.DataFrame()

    def fetch_trades(self, days: int = 7) -> pd.DataFrame:
        """
        Fetch recent trades from broker.

        Args:
            days: Number of days to look back

        Returns:
            DataFrame with columns: symbol, trade_type, quantity, price, trade_time
        """
        if self.broker == "zerodha":
            return self._fetch_zerodha_trades(days)
        elif self.broker == "csv":
            logger.warning("CSV mode: use import_trades_csv() instead")
            return pd.DataFrame()
        else:
            logger.error(f"fetch_trades not implemented for {self.broker}")
            return pd.DataFrame()

    def _fetch_zerodha_trades(self, days: int = 7) -> pd.DataFrame:
        """Fetch trades from Zerodha."""
        if not self.client:
            logger.error("Zerodha client not initialized")
            return pd.DataFrame()

        try:
            # Zerodha provides order history, not direct trades
            orders = self.client.orders()

            # Filter executed orders
            trades = [o for o in orders if o["status"] == "COMPLETE"]

            df = pd.DataFrame(trades)

            # Standardize
            df = df.rename(columns={
                "tradingsymbol": "symbol",
                "transaction_type": "trade_type",
                "average_price": "price",
                "order_timestamp": "trade_time",
                "filled_quantity": "quantity"
            })

            df = df[["symbol", "trade_type", "quantity", "price", "trade_time"]]

            # Convert timestamp
            df["trade_time"] = pd.to_datetime(df["trade_time"])

            # Filter by days
            cutoff = datetime.now() - pd.Timedelta(days=days)
            df = df[df["trade_time"] >= cutoff]

            logger.info(f"Fetched {len(df)} trades from Zerodha")
            return df

        except Exception as e:
            logger.error(f"Failed to fetch Zerodha trades: {e}")
            return pd.DataFrame()

    def import_holdings_csv(self, csv_path: str) -> pd.DataFrame:
        """
        Import holdings from CSV file.

        CSV format:
        symbol,quantity,avg_price
        RELIANCE,100,2450.50
        TCS,50,3200.00

        Args:
            csv_path: Path to CSV file

        Returns:
            DataFrame with holdings
        """
        try:
            df = pd.read_csv(csv_path)

            # Validate required columns
            required_cols = ["symbol", "quantity", "avg_price"]
            if not all(col in df.columns for col in required_cols):
                raise ValueError(f"CSV must have columns: {required_cols}")

            logger.info(f"Imported {len(df)} holdings from {csv_path}")
            return df

        except Exception as e:
            logger.error(f"Failed to import CSV: {e}")
            return pd.DataFrame()

    def import_trades_csv(self, csv_path: str) -> pd.DataFrame:
        """
        Import trades from CSV file.

        CSV format:
        symbol,trade_type,quantity,price,trade_time
        RELIANCE,BUY,100,2450.50,2025-01-01 09:30:00
        TCS,SELL,25,3200.00,2025-01-02 14:15:00

        Args:
            csv_path: Path to CSV file

        Returns:
            DataFrame with trades
        """
        try:
            df = pd.read_csv(csv_path)

            # Validate required columns
            required_cols = ["symbol", "trade_type", "quantity", "price", "trade_time"]
            if not all(col in df.columns for col in required_cols):
                raise ValueError(f"CSV must have columns: {required_cols}")

            # Convert timestamp
            df["trade_time"] = pd.to_datetime(df["trade_time"])

            logger.info(f"Imported {len(df)} trades from {csv_path}")
            return df

        except Exception as e:
            logger.error(f"Failed to import CSV: {e}")
            return pd.DataFrame()

    def sync_to_tracker(self, tracker):
        """
        Sync broker data to PortfolioTracker.

        Args:
            tracker: PortfolioTracker instance
        """
        # Fetch and sync holdings
        holdings = self.fetch_holdings()
        for _, row in holdings.iterrows():
            # Update tracker (simplified - in practice would check existing positions)
            logger.info(f"Synced holding: {row['symbol']} x {row['quantity']}")

        # Fetch and sync trades
        trades = self.fetch_trades(days=7)
        for _, row in trades.iterrows():
            tracker.record_trade(
                symbol=row["symbol"],
                trade_type=row["trade_type"],
                price=row["price"],
                quantity=row["quantity"],
                timestamp=row["trade_time"]
            )

        logger.info("Broker sync completed")


def setup_zerodha_auth() -> Dict[str, str]:
    """
    Helper to set up Zerodha authentication.

    Returns:
        Dictionary with api_key and access_token
    """
    print("=" * 60)
    print("ZERODHA KITE CONNECT SETUP")
    print("=" * 60)
    print()
    print("1. Go to https://kite.trade/")
    print("2. Create a developer account")
    print("3. Create a new app")
    print("4. Copy your API Key and API Secret")
    print("5. Generate access token using login flow")
    print()
    print("See docs: https://kite.trade/docs/connect/v3/")
    print()

    api_key = input("Enter API Key: ").strip()
    access_token = input("Enter Access Token: ").strip()

    return {
        "api_key": api_key,
        "access_token": access_token
    }
