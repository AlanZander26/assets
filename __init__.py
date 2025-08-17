# assets/__init__.py
"""
Assets package.

Provides core abstract base classes (ABCs) for assets and concrete 
implementations for different financial instruments (stocks, currencies, futures, options, etc.).

The public API allows direct access to common asset types without 
navigating into submodules.
"""

# Core abstract base classes
from assets.core import Asset, Underlying, Derivative

# Concrete asset types
from assets.instruments import Stock, Currency, Futures, Option

# Price Providers
from assets import price_providers # import subpackage

# Utilities
from assets.utils.expiration_date import ExpirationDate



__all__ = [
    # ABCs
    "Asset",
    "Underlying",
    "Derivative",

    # Concrete types
    "Stock",
    "Currency",
    "Futures",
    "Option",

    # Price Providers
    "price_providers",

    # Utilities
    "ExpirationDate",
]
