# Contains the Futures class

from assets.core.derivative import Derivative
from assets.core.underlying import Underlying

#################################
# Futures class
#################################
    
class Futures(Derivative):
    """
    Class representing a Futures contract.

    Attributes
    ----------
    forward_price : float
        Forward price of the underlying asset in the futures contract.
    contract_size : float
        Contract size, representing the quantity of the underlying asset in one futures contract.
    name : str
        Name of the futures contract, generated based on the underlying asset, expiration month, and year.
    expiration : str
        Expiration date of the futures contract in the YYMMDD format.
    """
    # Futures month codes
    futures_month_codes = {
        "01": "F",  # January
        "02": "G",  # February
        "03": "H",  # March
        "04": "J",  # April
        "05": "K",  # May
        "06": "M",  # June
        "07": "N",  # July
        "08": "Q",  # August
        "09": "U",  # September
        "10": "V",  # October
        "11": "X",  # November
        "12": "Z"   # December
    }

    def __init__(self, underlying: Underlying, expiration: str, forward_price: float, contract_size: float, price: float = None): 
        """
        Initialize a Futures instance.

        Parameters
        ----------
        underlying : Underlying
            The underlying asset for the futures contract.
        expiration : str
            Expiration date of the futures contract in the YYMMDD format.
        forward_price : float
            The agreed-upon price for the underlying asset at expiration.
        contract_size : float
            The quantity of the underlying asset represented by the futures contract.
        price : float
            The current market price of the futures contract.

        Raises
        ------
        TypeError
            If the expiration date is not provided or is not a string.
        ValueError
            If the expiration date is not in the expected format (YYMMDD).
        """
        self.forward_price = forward_price
        self.contract_size = contract_size
        name = self._make_name(underlying, expiration) 
        super().__init__(name, underlying, expiration, price=price)

    @classmethod
    def _make_name(cls, underlying, expiration, *args, **kwargs):
        if not expiration:
            raise TypeError("Futures contract must have an expiration date. 'expiration' cannot be None.")
        try:
            return underlying.name + cls.futures_month_codes[expiration[2:4]] + str(expiration[4:6])
        except KeyError:
            raise ValueError(f"Invalid month in expiration: '{expiration[2:4]}'. Must be 01–12.")

    def price_at_expiration(self, ST: float) -> float:
        """
        Calculate the settlement price of the futures contract at expiration.

        Parameters
        ----------
        ST : float
            The price of the underlying asset at the expiration date.

        Returns
        -------
        float
            Settlement price of the futures contract.
        """
        price_at_expr = self.contract_size * (ST - self.forward_price)
        return price_at_expr