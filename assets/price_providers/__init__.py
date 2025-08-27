# assets/price_providers/__init__.py
"""
Price Providers subpackage.

Provides abstract base classes (ABCs) and concrete implementations
for fetching and updating asset prices from external data sources
(e.g., Yahoo Finance).

Public API
----------
- Base classes:
    PriceProvider

- Example implementations:
    YFinanceStockPriceProvider
    YFinanceCurrencyPriceProvider
"""

# Base ABC
from assets.price_providers.price_provider import PriceProvider

# Example concrete implementations
from assets.price_providers.stock_price_providers.yfinance_stock_price_provider import YFinanceStockPriceProvider
from assets.price_providers.currency_price_providers.yfinance_currency_price_provider import YFinanceCurrencyPriceProvider

__all__ = [
    "PriceProvider",
    "YFinanceStockPriceProvider",
    "YFinanceCurrencyPriceProvider",
]
