# Contains the Asset ABC

from abc import ABC, abstractmethod

#################################
# Asset Class
#################################

class Asset(ABC):
    """
    Represents a financial asset, such as a stock or derivative.
    Stores information about the asset itself (name, current price),
    but does not handle ownership or trading details. Only one instance 
    per asset can exist.

    Attributes
    ----------
    _assets : dict
        Class-level dictionary to store the existing assets.
    name : str
        Name of the asset (e.g., "AAPL" for Apple stock).
    _price : float or None
        Current price of the asset.
    _initialized : bool
        Whether the asset already exist or not.
    """

    _assets = {}

    def __new__(cls, *args, **kwargs):
        name = cls._make_name(*args, **kwargs)  
        key = f"{cls.__name__}({name})"  
        if key in cls._assets:
            return cls._assets[key]
        instance = object.__new__(cls)
        cls._assets[key] = instance
        return instance

    def __init__(self, name: str, price : float = None):
        """
        Initialize the Asset.

        Parameters
        ----------
        name : str
            Name of the asset (e.g., stock ticker).
        price : float or None
            Current price of the asset.
        """
        if not hasattr(self, "_initialized"):
            self._name = name
            self._initialized = True
        self.set_price(price)

    def __repr__(self) -> str:
        """
        Provide a string representation of the asset.

        Returns
        -------
        str
            A string in the format: Asset(name).
        """
        return f"{self.__class__.__name__}({self.name})"

    @classmethod
    @abstractmethod
    def _make_name(cls, *args, **kwargs) -> str:
        """Subclasses must return the canonical name for the asset."""
        pass

    def asset_type(self) -> str:
        """
        Determine the specific asset type (e.g., 'Stock', 'Option', etc.).

        Returns
        -------
        str
            The specific type of the asset.
        """
        return self.__class__.__name__

    @property
    def name(self) -> str:
        """
        Get the immutable name of the asset.
    
        Returns
        -------
        str
            The name of the asset, as defined during initialization
            (e.g., stock ticker, currency code). This value cannot
            be modified after creation.
        """
        return self._name

    @property
    def price(self) -> float:
        """
        Get the current stored price of the asset.
    
        Returns
        -------
        float or None
            The most recently set price for the asset. May be ``None``
            if no price has been assigned yet.
        """
        return self._price

    def set_price(self, price: float = None) -> None:
        """
        Set the price of the asset.
    
        Parameters
        ----------
        price : float or None, optional
            The new price to assign to the asset. Can be ``None`` to
            indicate that the price is unknown or not set.
        """
        self._price = price

    @abstractmethod
    def price_at_expiration(self, ST):
        """
        Abstract method to calculate the price of the asset at expiration.

        This method must be implemented by subclasses and defines how the asset's value 
        is determined at expiration, based on the underlying price.

        Parameters
        ----------
        ST : float 
            The price of the underlying asset at expiration.

        Returns
        -------
        float
            The price of the asset at expiration.
        """
        pass

    def change_to_target(self, target_price: float) -> float:
        """
        Calculate the percentage change required for the asset to reach a target price.

        Parameters
        ----------
        target_price : float
            The target price to which the asset's current price will be compared.

        Returns
        -------
        float
            The percentage change needed to reach the target price.

        Raises
        ------
        ValueError
            If the current price (`self.price`) is not set or is None.

        Notes
        -----
        Percentage Change = ((target_price - current_price) / current_price) * 100
        """
        if self.price is None:
            raise ValueError("Current price is not set. Cannot calculate percentage change.")
        return (target_price - self.price) / self.price * 100


    def get_true_underlying(self, get_order=False):
        """
        Recursively identifies the ultimate underlying asset. If the asset is a derivative, and its    underlying is also a derivative, the process continues until an asset that is not a derivative is reached.

        Returns
        -------
        Underlying
            The true underlying asset, or self if already an underlying.

        Notes
        -----
        - If the asset is an instance of Underlying, it is returned directly.
        - If the asset is an instance of Derivative, the function drills down
          through the underlying hierarchy until it finds a non-derivative underlying.
        """
        current_asset = self
        i = 0
        while hasattr(current_asset, 'underlying'):
            current_asset = current_asset.underlying
            i += 1
        order = i # order of the derivative. 
        if not get_order:
            return current_asset
        return current_asset, order
    
    def get_true_underlying_price(self):
        """
        Returns the price of the true underlying asset.

        Returns
        -------
        float
            The price of the true underlying asset.
        """
        return self.get_true_underlying().price