# Contains the Currency class

from assets.core.underlying import Underlying

#################################
# Currency class
#################################

class Currency(Underlying):
    """
    Class representing currency as an underlying asset.

    Inherits from Underlying.

    Attributes
    ----------
    currency : str
        The name of the currency (e.g., 'USD', 'EUR').
    exchange_rate : float
        The exchange rate of the currency relative to USD.

    """

    def __init__(self, currency: str, exchange_rate: float = None):
        """
        Initialize a Currency instance.

        Parameters
        ----------
        currency : str
            The currency of the cash (e.g., 'USD', 'EUR').
        exchange_rate : float
            The exchange rate of the currency relative to USD.

        """
        name = self._make_name(currency)
        if name == 'USD' and exchange_rate != 1:
            raise ValueError("Exchange rates are relative to the USD, i.e 'exchange_rate' must be 1 for USD.")
        super().__init__(name, price=exchange_rate)

    @classmethod
    def _make_name(cls, currency, *args, **kwargs):
        """
        Construct the canonical name for the currency.
    
        Parameters
        ----------
        currency : str
            The currency symbol (e.g., 'USD', 'EUR').
    
        *args, **kwargs
            Additional positional and keyword arguments. Ignored in this implementation.
    
        Returns
        -------
        str
            The uppercase version of the currency symbol.
        """
        return currency.upper()
        