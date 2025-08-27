# Contains the PriceProvider class

from abc import ABC, abstractmethod
from collections.abc import Iterable
from assets.core.asset import Asset
from assets.utils.validation import validate_type

#################################
# PriceProvider Abstract Base Class
#################################

class PriceProvider(ABC):
    """
    Abstract base class for all price providers.

    Price providers are responsible for fetching the current market price
    of a given Asset instance from an external source and, if requested,
    updating the Asset's stored price.

    Attributes
    ----------
    asset_class : type
        The class of asset that the provider supports (e.g., Stock, Currency).
        Subclasses must override this to declare which asset type they handle.
        Used for type validation.

    Methods
    -------
    update_price(asset)
        Fetch the latest price and update the asset's stored price.
    get_price(asset)
        Fetch and return the current market price for the given asset.
    get_previous_close_price(asset)
        Fetch the previous close price for the given asset.
    """

    @property
    @abstractmethod
    def asset_class(self):
        """The class of asset supported by this provider (e.g., Stock, Currency)."""
        pass

    def update_price(self, asset) -> None:
        """
        Fetch and update the price of one or many assets in-place.

        Parameters
        ----------
        asset : Asset or iterable of Asset
            A single Asset instance or an iterable of Asset instances.

        Raises
        ------
        TypeError
            If `asset` is not an Asset or iterable of Assets.
        """
        validate_type(asset, self.asset_class)

        if isinstance(asset, Iterable) and not isinstance(asset, (str, bytes)):
            for a in asset:
                self.update_price(a)  # recursion
        else:
            price = self.get_price(asset)
            if price is None:
                raise ValueError(f"Failed to fetch price for {asset}.")
            asset.set_price(price)

    @abstractmethod
    def get_price(self, asset) -> float:
        """
        Fetch the current market price for the given asset.

        Parameters
        ----------
        asset : Asset
            The asset whose price should be fetched.

        Returns
        -------
        float
            The latest available price for the asset.
        """
        pass

    @abstractmethod
    def get_previous_close_price(self, asset) -> float:
        """Fetch the previous close price for the given asset."""
        pass
        