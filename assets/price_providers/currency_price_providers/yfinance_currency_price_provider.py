# Contains the YFinanceCurrencyPriceProvider class

import yfinance as yf
from assets.price_providers.price_provider import PriceProvider
from assets.instruments.currency import Currency

#################################
# YFinanceCurrencyPriceProvider Class
#################################

class YFinanceCurrencyPriceProvider(PriceProvider):
    """
    A currency exchange rate provider that fetches the latest exchange from Yahoo Finance using the `yfinance` library.
    """
    @property
    def asset_class(self):
        return Currency

    def get_price(self, asset) -> float:
        """
        Fetch the latest available exchange rate for the given currency.

        Parameters
        ----------
        asset : Cash
            The currency whose price (exchange rate) should be fetched.

        Returns
        -------
        float
            The latest market price for the currency.

        Raises
        ------
        ValueError
            If no exchange rate could be retrieved for the currency.
        """
        ticker = asset.name + "USD=X"
        try:
            data = yf.Ticker(ticker)
            # Try fast_info for speed
            price = getattr(data.fast_info, "last_price", None)
            if price is None:
                hist = data.history(period="1d")
                if hist.empty:
                    raise ValueError(f"No price data found for {ticker}.")
                price = hist["Close"].iloc[-1]
            return float(price)
        except Exception as e:
            raise ValueError(f"Failed to fetch price for {asset}: {e}")

    def get_previous_close_price(self, asset) -> float:
        ticker = asset.name + "USD=X"
        try:
            data = yf.Ticker(ticker)
            price = getattr(data.fast_info, "previous_close", None)
            if price is None:
                hist = data.history(period="2d")
                if len(hist) < 2:
                    raise ValueError(f"No previous close data found for {ticker}.")
                price = hist["Close"].iloc[-2]
            return float(price)
        except Exception as e:
            raise ValueError(f"Failed to fetch previous close price for {asset}: {e}")
