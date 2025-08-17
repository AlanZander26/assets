# Contains the Stock class

from assets.core.underlying import Underlying

#################################
# Stock class
#################################
        
class Stock(Underlying):
    """
    Class representing a stock as an underlying asset.

    Attributes
    ----------
    ticker : str
        The stock ticker symbol (e.g., 'AAPL', 'TSLA').
    price : float
        The current price of the stock.
    """

    def __init__(self, ticker: str, price: float = None):
        """
        Initialize a Stock instance.

        Parameters
        ----------
        ticker : str
            The stock ticker symbol (e.g., 'AAPL', 'TSLA').
        price : float
            The current price of the stock.
        """
        name = self._make_name(ticker)
        super().__init__(name, price=price)

    @classmethod
    def _make_name(cls, ticker: str, *args, **kwargs):
        """
        Construct the canonical name for the stock.
    
        Parameters
        ----------
        ticker : str
            The stock ticker symbol (e.g., 'AAPL', 'TSLA').
    
        *args, **kwargs
            Additional positional and keyword arguments. Ignored in this implementation.
    
        Returns
        -------
        str
            The uppercase version of the ticker symbol.
        """
        return ticker.upper()
        