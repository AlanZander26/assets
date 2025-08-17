"""
Currency price providers.

This submodule collects implementations of price providers that
fetch currency exchange rates from external data sources (e.g. Yahoo Finance).
"""

from assets.price_providers.currency_price_providers.yfinance_currency_price_provider import YFinanceCurrencyPriceProvider

__all__ = [
    "YFinanceCurrencyPriceProvider",
]