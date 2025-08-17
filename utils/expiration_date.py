# Contains the ExpirationDate class

from datetime import datetime

#################################
# ExpirationDate Class
#################################

class ExpirationDate:
    """
    Represents the expiration date of a financial instrument, such as an option.
    Tracks the time remaining until expiration and allows for fixing or unfixing
    the time to expiration.

    Attributes
    ----------
    expiration_date : str
        Expiration date in the format 'YYMMDD'.
    expiration_time : datetime
        The expiration date converted to a `datetime` object.
    isTimeFixed : bool
        Indicates whether the time to expiration is fixed.
    _fixed_time : float or None
        Fixed time to expiration in years, if `isTimeFixed` is True.
    """

    def __init__(self, expiration_date: str):
        """
        Initialize the ExpirationDate object.

        Parameters
        ----------
        expiration_date : str
            Expiration date in the format 'YYMMDD'.

        Raises
        ------
        TypeError
            If `expiration_date` is not a string.
        TypeError
            If `expiration_date` is not in the correct 'YYMMDD' format.
        """
        if not isinstance(expiration_date, str):
            raise TypeError(f"Expiration date must be a string of the form 'YYMMDD', not of type {type(expiration_date)}")
        try:
            self.expiration_time = datetime.strptime(expiration_date, '%y%m%d')  # Validate expiration date format
        except ValueError:
            raise ValueError(f"Invalid expiration date format: '{expiration_date}'. Expected 'YYMMDD'.")
        self.expiration_date = expiration_date
        self.isTimeFixed = False
        self._fixed_time = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.expiration_date})"

    @property
    def T(self) -> float:
        """
        Calculate the time to expiration in years.

        Returns
        -------
        float
            Time to expiration in years. If `isTimeFixed` is True, returns the fixed time.

        Notes
        -----
        - If time is not fixed, calculates the remaining time to expiration based on the
          current date and time.
        - Adds one extra day to include the expiration day itself.
        """
        if self.isTimeFixed:
            return self._fixed_time
        delta_time = self.expiration_time - datetime.now()
        delta_days = delta_time.days + delta_time.seconds / (3600 * 24) + 1  # +1 to include the expiration day
        return delta_days / 365

    def fix_time(self, years_to_expiration: float) -> None:
        """
        Fix the time to expiration to a specific value.

        Parameters
        ----------
        years_to_expiration : float
            The fixed time to expiration in years.
        """
        self.isTimeFixed = True
        self._fixed_time = years_to_expiration

    def unfix_time(self) -> None:
        """
        Unfix the time to expiration, allowing it to be calculated dynamically.
        """
        self.isTimeFixed = False
        self._fixed_time = None

    def is_expired(self) -> bool:
        """
        Check if the expiration date has passed.

        Returns
        -------
        bool
            True if the expiration date has passed, False otherwise.
        """
        return self.T <= 0

    def days_to_expiration(self) -> float:
        """
        Calculate the time to expiration in days.

        Returns
        -------
        float
            Time to expiration in days.
        """
        return self.T * 365
