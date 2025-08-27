# Contains the Option class

import numpy as np
from assets.core.derivative import Derivative

#################################
# Option class
#################################    

# Maybe in the future implement subclasses EquityOption, FuturesOption, IndexOption, ...
class Option(Derivative):
    """
    Class representing a financial option as a type of Derivative.

    Attributes
    ----------
    underlying : Underlying
        The underlying asset for the option.
    strike : float
        The strike price of the option.
    expiration : str
        Expiration date of the option in the 'YYMMDD' format.
    option_type : str
        The type of option: 'C' for call options and 'P' for put options.
    multiplier : int
        Contract multiplier that determines the quantity of the underlying asset represented by one option contract.
        Defaults to 100 for standard equity options, but may vary for futures, index, or other option types.
    name : str
        Name of the option contract, automatically generated based on the underlying asset, 
        expiration date, option type, and strike price.



    """

    def __init__(self, underlying, strike, expiration, option_type, price = None, multiplier = 100):
        """
        Initialize an Option instance.

        Parameters
        ----------
        underlying : Underlying
            The underlying asset for the option.
        expiration : str
            Expiration date of the option in the 'YYMMDD' format.
        option_type : str
            Type of option: 'call', 'put', 'C', or 'P'.
        strike : float
            Strike price of the option.
        price : float
            Current market price of the option.
        multiplier : int
            Contract multiplier that determines the quantity of the underlying asset.

        Raises
        ------
        TypeError
            If the expiration date is not provided (None).
        ValueError
            If the option type is invalid. Allowed types are 'call', 'put', 'C', or 'P'.
        """
        if expiration is None:
            raise TypeError("Option contract must have an expiration date. 'expiration' cannot be None.")
        
        # Validate and format the option type
        if option_type.upper() in ["CALL", "C", "PUT", "P"]:
            self.option_type = option_type[0].upper()  # Standardize to "C" or "P"
        else:
            raise ValueError(f"Invalid option type: {option_type}. Allowed types are 'call' or 'put'.")

        self.strike = strike  # Strike price
        self.multiplier = multiplier  # Default number of shares per option contract

        # Generate contract name
        name = self._make_name(underlying, strike, expiration, option_type)
        super().__init__(name, underlying, expiration, price=price)

    @classmethod
    def _make_name(cls, underlying, strike, expiration, option_type, *args, **kwargs):
        return (
            underlying.name
            + expiration
            + option_type[0].upper()
            + str(int(strike * 1e3)).zfill(8)  # Strike price as an 8-digit integer (padded)
        )


    def price_at_expiration(self, ST: float) -> float:
        """
        Calculate the option's payoff at expiration given the underlying asset's price.

        Parameters
        ----------
        ST : float
            Price of the underlying asset at expiration.

        Returns
        -------
        float
            The payoff of the option at expiration, calculated based on the type of option:
            - Call option: max(0, ST - K) * multiplier
            - Put option: max(0, K - ST) * multiplier
        """
        K = self.strike
        if self.option_type == "C":
            price_at_expr = self.multiplier * np.maximum(0, ST - K)  # Payoff for call option
        elif self.option_type == "P":
            price_at_expr = self.multiplier * np.maximum(0, K - ST)  # Payoff for put option
        return price_at_expr
        