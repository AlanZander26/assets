"""
Stock price providers.

This submodule collects implementations of price providers that
fetch stock prices from external data sources (e.g. Yahoo Finance).
"""

from assets.price_providers.stock_price_providers.yfinance_stock_price_provider import YFinanceStockPriceProvider

__all__ = [
    "YFinanceStockPriceProvider",
]
