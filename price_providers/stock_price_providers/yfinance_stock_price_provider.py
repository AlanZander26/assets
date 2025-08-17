# Contains the YFinanceStockPriceProvider class

import yfinance as yf
from assets.price_providers.price_provider import PriceProvider
from assets.instruments.stock import Stock

#################################
# YFinanceStockPriceProvider Class
#################################

class YFinanceStockPriceProvider(PriceProvider):
    """
    A stock price provider that fetches the latest prices from Yahoo Finance using the `yfinance` library.
    """
    @property
    def asset_class(self):
        return Stock

    def get_price(self, asset) -> float:
        """
        Fetch the latest available price for the given stock.

        Parameters
        ----------
        asset : Stock
            The stock asset whose price should be fetched.

        Returns
        -------
        float
            The latest market price for the stock.

        Raises
        ------
        ValueError
            If no price could be retrieved for the stock.
        """
        ticker = asset.name
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
        ticker = asset.name
        try:
            data = yf.Ticker(ticker)
            hist = data.history(period="2d")
            if len(hist) < 2:
                raise ValueError(f"No previous close data found for {ticker}.")
            price = hist["Close"].iloc[-2]
            return price
        except Exception as e:
            raise ValueError(f"Failed to fetch previous close price for {asset}: {e}")

