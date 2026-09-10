# Contains the Derivative ABC

from abc import ABC, abstractmethod
from assets.core.asset import Asset
from assets.utils.expiration_date import ExpirationDate
from datetime import datetime

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

    def value_on_date(self, St, target_date, price_model, *args, **kwargs):
        """ 
        Calculates the value of the asset on a specific date using the specified pricing model. 

        Parameters 
        ---------- 
        St : float or np.ndarray 
            Current underlying price. 
        target_date : datetime 
            The target date for which to calculate the asset value. 
        price_model : type 
            The pricing model class to use. 
        *args 
            Additional positional arguments passed to the pricing model. 
        **kwargs Additional keyword arguments passed to the pricing model. 
        """ 
        model = self._initialize_price_model(price_model)
        if self.expiration is None: 
            return model.value(St, *args, **kwargs)
        self.expiration._validate_date(target_date)
        target_date = self.expiration._convert_date_into_datetime(target_date)
        T = (self.expiration.expiration_time - target_date).total_seconds() / (365 * 24 * 60 * 60)
        if T < 0: # expired asset. Note that method 'value()' must handle the case T = 0 (expiration).
            raise ValueError(f"Invalid input: {target_date}. Target date must be before expiration: '{self.expiration.expiration_date}'.")
        return model.value(St, T, *args, **kwargs)
    
    @abstractmethod
    def payoff(self, ST): # Maybe constrain the price to be at price at expiration when the derivative expires?
        pass

    @abstractmethod
    def _initialize_price_model(self, price_model):
        pass

    def current_value(self, price_model, *args, **kwargs):
        S0 = self.get_true_underlying_price()
        today_date = datetime.now().strftime("%y%m%d")
        return self.value_on_date(S0, today_date, price_model, *args, **kwargs)
    
    def current_valuation(self, price_model, *args, **kwargs):
        P = self.price
        return 100 * (self.current_value(price_model, *args, **kwargs) - P) / P


