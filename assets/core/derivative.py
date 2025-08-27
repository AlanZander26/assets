# Contains the Derivative ABC

from abc import ABC, abstractmethod
from assets.core.asset import Asset
from assets.utils.expiration_date import ExpirationDate

#################################
# Derivative class
#################################

class Derivative(Asset, ABC):
    """
    Base class for financial derivatives, representing instruments whose value is derived 
    from an underlying asset.

    Inherits from Asset.

    Attributes
    ----------
    asset_category : str
        Returns the asset category (here "Derivative")
    underlying : Underlying
        The underlying asset for the derivative.
    expiration : str or None
        Expiration date of the derivative in 'YYMMDD' format. If None, the derivative does not expire.
    """

    asset_category = "Derivative"
    
    def __init__(self, name: str, underlying: Asset, expiration: str = None, price: float = None): 
        """
        Initialize a Derivative instance.

        Parameters
        ----------
        name : str
            Name of the derivative.
        price : float
            Current price of the derivative.
        underlying : Asset
            The underlying asset for the derivative. The underlying need not be an instance of the class Underlying, since there are derivatives on derivatives, e.g. options on futures.
        expiration : str, optional
            Expiration date in 'YYMMDD' format. Defaults to None for derivatives without expiration.
        """
        super().__init__(name, price=price)
        self.underlying = underlying
        if expiration is not None:
            self.expiration = ExpirationDate(expiration)
        else:
            self.expiration = expiration
    
    @abstractmethod
    def price_at_expiration(self, ST): # Maybe constrain the price to be at price at expiration when the derivative expires?
        pass
