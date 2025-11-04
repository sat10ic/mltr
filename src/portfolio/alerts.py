"""
Emergency alert system for portfolio protection.

This module monitors your holdings for dangerous situations and sends
immediate alerts when action is needed.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd


logger = logging.getLogger(__name__)


class EmergencyAlertSystem:
    """
    Monitor portfolio for emergency situations.

    Alerts you when:
    - A stock you hold is falling rapidly (>5% intraday)
    - Multiple positions hit stop-losses
    - Portfolio drawdown exceeds threshold
    - Unusual volume or price action

    Example:
        >>> alerts = EmergencyAlertSystem()
        >>>
        >>> # Check a position for emergency
        >>> alert = alerts.check_position("RELIANCE", current_price=2300, avg_price=2500)
        >>> if alert:
        ...     print(f"ALERT: {alert['message']}")
        ALERT: RELIANCE down 8.0% from your average price!
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize emergency alert system.

        Args:
            config: Alert configuration with thresholds
        """
        self.config = config or self._default_config()
        self.alerts: List[Dict] = []

    def _default_config(self) -> Dict:
        """Default alert thresholds."""
        return {
            "intraday_drop_pct": 5.0,  # Alert if stock drops >5% today
            "position_loss_pct": 10.0,  # Alert if position down >10%
            "portfolio_drawdown_pct": 15.0,  # Alert if portfolio down >15%
            "stop_loss_pct": 7.0,  # Default stop-loss level
            "volume_spike_multiplier": 3.0,  # Alert if volume >3x average
            "circuit_limit_buffer_pct": 2.0,  # Alert if approaching circuit limit
        }

    def check_position(
        self,
        symbol: str,
        current_price: float,
        avg_price: float,
        quantity: int,
        day_open: Optional[float] = None,
        day_high: Optional[float] = None,
        day_low: Optional[float] = None,
        volume: Optional[int] = None,
        avg_volume: Optional[int] = None
    ) -> Optional[Dict]:
        """
        Check a single position for emergency conditions.

        Args:
            symbol: Stock symbol
            current_price: Current market price
            avg_price: Your average purchase price
            quantity: Number of shares held
            day_open: Today's opening price
            day_high: Today's high
            day_low: Today's low
            volume: Current volume
            avg_volume: 20-day average volume

        Returns:
            Alert dictionary if emergency detected, None otherwise
        """
        alerts = []

        # Check position loss
        position_pnl_pct = ((current_price - avg_price) / avg_price) * 100
        if position_pnl_pct < -self.config["position_loss_pct"]:
            alerts.append({
                "type": "POSITION_LOSS",
                "severity": "HIGH",
                "symbol": symbol,
                "message": f"{symbol} down {abs(position_pnl_pct):.1f}% from your average price!",
                "current_price": current_price,
                "avg_price": avg_price,
                "pnl_pct": position_pnl_pct,
                "action": f"Consider reviewing stop-loss. Current loss: ₹{abs((current_price - avg_price) * quantity):,.0f}"
            })

        # Check intraday drop
        if day_open:
            intraday_pct = ((current_price - day_open) / day_open) * 100
            if intraday_pct < -self.config["intraday_drop_pct"]:
                alerts.append({
                    "type": "INTRADAY_DROP",
                    "severity": "CRITICAL",
                    "symbol": symbol,
                    "message": f"{symbol} falling rapidly: {abs(intraday_pct):.1f}% down today!",
                    "current_price": current_price,
                    "day_open": day_open,
                    "intraday_pct": intraday_pct,
                    "action": "Consider emergency exit or tightening stop-loss"
                })

        # Check if approaching stop-loss
        stop_loss_price = avg_price * (1 - self.config["stop_loss_pct"] / 100)
        if current_price <= stop_loss_price:
            alerts.append({
                "type": "STOP_LOSS_HIT",
                "severity": "CRITICAL",
                "symbol": symbol,
                "message": f"{symbol} hit stop-loss level!",
                "current_price": current_price,
                "stop_loss_price": stop_loss_price,
                "action": "EXIT POSITION IMMEDIATELY"
            })

        # Check volume spike (may indicate panic selling or news)
        if volume and avg_volume and volume > avg_volume * self.config["volume_spike_multiplier"]:
            alerts.append({
                "type": "VOLUME_SPIKE",
                "severity": "MEDIUM",
                "symbol": symbol,
                "message": f"{symbol} volume spike: {volume / avg_volume:.1f}x normal",
                "volume": volume,
                "avg_volume": avg_volume,
                "action": "Check news and fundamentals. May indicate significant event."
            })

        # Check if approaching lower circuit limit (relevant for Indian markets)
        if day_open:
            lower_circuit = day_open * 0.80  # 20% lower circuit (varies by stock)
            buffer_price = lower_circuit * (1 + self.config["circuit_limit_buffer_pct"] / 100)
            if current_price <= buffer_price:
                alerts.append({
                    "type": "CIRCUIT_LIMIT",
                    "severity": "CRITICAL",
                    "symbol": symbol,
                    "message": f"{symbol} approaching lower circuit limit!",
                    "current_price": current_price,
                    "lower_circuit": lower_circuit,
                    "action": "EXIT MAY BE DIFFICULT. Circuit limit freeze possible."
                })

        if alerts:
            # Return the most severe alert
            severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
            most_severe = min(alerts, key=lambda x: severity_order[x["severity"]])

            # Log and store
            logger.warning(f"EMERGENCY ALERT: {most_severe['message']}")
            self.alerts.append({**most_severe, "timestamp": datetime.now()})

            return most_severe

        return None

    def check_portfolio(self, positions: pd.DataFrame, market_data: pd.DataFrame) -> List[Dict]:
        """
        Check entire portfolio for emergencies.

        Args:
            positions: DataFrame with columns: symbol, quantity, avg_price
            market_data: DataFrame with current market data

        Returns:
            List of alerts
        """
        alerts = []

        # Join positions with market data
        portfolio = positions.merge(
            market_data,
            on="symbol",
            how="left"
        )

        # Check each position
        for _, row in portfolio.iterrows():
            alert = self.check_position(
                symbol=row["symbol"],
                current_price=row.get("close", row.get("current_price")),
                avg_price=row["avg_price"],
                quantity=row["quantity"],
                day_open=row.get("open"),
                day_high=row.get("high"),
                day_low=row.get("low"),
                volume=row.get("volume"),
                avg_volume=row.get("avg_volume")
            )

            if alert:
                alerts.append(alert)

        # Check portfolio-level metrics
        portfolio_alerts = self._check_portfolio_level(portfolio)
        alerts.extend(portfolio_alerts)

        return alerts

    def _check_portfolio_level(self, portfolio: pd.DataFrame) -> List[Dict]:
        """Check portfolio-level risk metrics."""
        alerts = []

        # Calculate portfolio P&L
        portfolio["market_value"] = portfolio["quantity"] * portfolio.get("close", portfolio.get("current_price", 0))
        portfolio["cost_basis"] = portfolio["quantity"] * portfolio["avg_price"]

        total_market_value = portfolio["market_value"].sum()
        total_cost = portfolio["cost_basis"].sum()

        if total_cost > 0:
            portfolio_pnl_pct = ((total_market_value - total_cost) / total_cost) * 100

            if portfolio_pnl_pct < -self.config["portfolio_drawdown_pct"]:
                alerts.append({
                    "type": "PORTFOLIO_DRAWDOWN",
                    "severity": "HIGH",
                    "symbol": "PORTFOLIO",
                    "message": f"Portfolio down {abs(portfolio_pnl_pct):.1f}%!",
                    "current_value": total_market_value,
                    "cost_basis": total_cost,
                    "pnl_pct": portfolio_pnl_pct,
                    "action": "Review risk management. Consider reducing exposure."
                })

        # Check concentration risk
        if len(portfolio) > 0:
            max_position_pct = (portfolio["market_value"].max() / total_market_value) * 100
            if max_position_pct > 30:  # Single position >30% of portfolio
                largest_symbol = portfolio.loc[portfolio["market_value"].idxmax(), "symbol"]
                alerts.append({
                    "type": "CONCENTRATION_RISK",
                    "severity": "MEDIUM",
                    "symbol": largest_symbol,
                    "message": f"{largest_symbol} is {max_position_pct:.1f}% of portfolio",
                    "position_pct": max_position_pct,
                    "action": "Consider diversifying. High concentration risk."
                })

        # Check number of losing positions
        losing_positions = (portfolio["market_value"] < portfolio["cost_basis"]).sum()
        if losing_positions >= len(portfolio) * 0.7:  # >70% positions in loss
            alerts.append({
                "type": "MULTIPLE_LOSSES",
                "severity": "HIGH",
                "symbol": "PORTFOLIO",
                "message": f"{losing_positions}/{len(portfolio)} positions in loss",
                "losing_count": losing_positions,
                "total_count": len(portfolio),
                "action": "Review market conditions and strategy. May be in downtrend."
            })

        return alerts

    def get_recent_alerts(self, hours: int = 24) -> List[Dict]:
        """Get alerts from recent time period."""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [a for a in self.alerts if a["timestamp"] >= cutoff]

    def clear_alerts(self):
        """Clear all stored alerts."""
        self.alerts = []
        logger.info("Cleared all alerts")

    def format_alert_message(self, alert: Dict) -> str:
        """
        Format alert for display or notification.

        Args:
            alert: Alert dictionary

        Returns:
            Formatted message string
        """
        severity_emoji = {
            "CRITICAL": "🚨",
            "HIGH": "⚠️",
            "MEDIUM": "⚡",
            "LOW": "ℹ️"
        }

        emoji = severity_emoji.get(alert["severity"], "📊")

        message = f"{emoji} **{alert['severity']}** - {alert['type']}\n"
        message += f"**{alert['symbol']}**: {alert['message']}\n"
        message += f"**Action**: {alert['action']}\n"

        if "current_price" in alert:
            message += f"Current Price: ₹{alert['current_price']:.2f}\n"

        if "pnl_pct" in alert:
            pnl_emoji = "📉" if alert["pnl_pct"] < 0 else "📈"
            message += f"{pnl_emoji} P&L: {alert['pnl_pct']:.2f}%\n"

        return message
