"""Data models for portfolio tracking."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Position:
    """Current portfolio position."""

    symbol: str
    quantity: int
    avg_price: float
    current_price: Optional[float] = None
    last_updated: Optional[datetime] = None

    @property
    def market_value(self) -> float:
        """Current market value of position."""
        if self.current_price:
            return self.quantity * self.current_price
        return 0.0

    @property
    def unrealized_pnl(self) -> float:
        """Unrealized profit/loss."""
        if self.current_price:
            return (self.current_price - self.avg_price) * self.quantity
        return 0.0

    @property
    def pnl_pct(self) -> float:
        """Unrealized P&L percentage."""
        if self.avg_price > 0:
            return ((self.current_price or 0) - self.avg_price) / self.avg_price * 100
        return 0.0


@dataclass
class Trade:
    """Executed trade."""

    symbol: str
    trade_type: str  # BUY or SELL
    quantity: int
    price: float
    trade_time: datetime
    signal_id: Optional[int] = None
    commission: float = 0.0
    notes: str = ""

    @property
    def value(self) -> float:
        """Trade value (quantity * price)."""
        return self.quantity * self.price

    @property
    def total_cost(self) -> float:
        """Total cost including commission."""
        return self.value + self.commission


@dataclass
class Signal:
    """Trading signal from ML system."""

    symbol: str
    signal_type: str  # BUY, SELL, or HOLD
    signal_price: float
    signal_time: datetime
    confidence: float = 0.5
    executed: bool = False
    execution_time: Optional[datetime] = None
    execution_price: Optional[float] = None


@dataclass
class PortfolioState:
    """Overall portfolio state."""

    total_value: float
    num_positions: int
    cash: float
    timestamp: datetime

    @property
    def invested_value(self) -> float:
        """Total invested value (excludes cash)."""
        return self.total_value - self.cash
