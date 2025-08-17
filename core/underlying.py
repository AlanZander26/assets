# Contains the Underlying ABC

from abc import ABC
from assets.core.asset import Asset 

#################################
# Underlying class
#################################

class Underlying(Asset, ABC):
    """
    Abstract base class for all underlying assets.

    Inherits from Asset and represents any financial instrument that
    can serve as the underlying for derivatives such as options or futures.

    Attributes
    ----------
    asset_category : str
        Returns the asset category (here "Underlying").
    """
        
    asset_category = "Underlying"
    
    
    def price_at_expiration(self, ST):
        return ST
