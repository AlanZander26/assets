# Contains function for validation

from collections.abc import Iterable

def validate_type(obj, expected_type):
    """
    Validate that an object is an instance of the expected type(s),
    or an iterable containing only instances of the expected type(s).

    Parameters
    ----------
    obj : object or iterable
        The object (or iterable of objects) to validate.
    expected_type : type or tuple of types
        The expected class or classes.

    Raises
    ------
    TypeError
        If validation fails.
    """
    # Handle iterables (but exclude str/bytes to avoid accidental iteration)
    if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        for item in obj:
            validate_type(item, expected_type)  # recursion
        return  # nothing to return

    # Handle single object
    if not isinstance(obj, expected_type):
        raise TypeError(
            f"Expected {expected_type.__name__}, got {type(obj).__name__} instead."
        )
