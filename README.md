# assets

A Python package for modeling financial instruments such as **stocks, forex/currencies, futures, and options**, with a flexible design that supports price providers.  

This package is intended as a **foundation** for building higher-level financial applications, such as **tracking performance, computing risk metrics, valuation models, watchlists, and portfolio applications**.

## Features

- Core abstractions for financial assets (base classes for underlying and derivative instruments).
- Concrete implementations:
  - Stocks
  - Currencies (Forex)
  - Futures
  - Options
- Price provider framework with plug-in support for external data sources (e.g. Yahoo Finance).

## Examples

For detailed examples, go to `examples`.

## Tests

In order to test the package, first install it in editable mode along with the development dependencies. So go to the root directory and type:

```bash
pip install -e .
pip install pytest
```

To run the full test suite, execute:

```bash
pytest
```

All tests are located in the `tests/` directory. You can also run a specific test file:

```bash
pytest tests/test_instruments.py
```

By default, `pytest` will discover any files matching the pattern `test_*.py` inside the `tests/` folder.


