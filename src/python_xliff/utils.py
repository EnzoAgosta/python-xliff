from collections.abc import Callable
from enum import Enum
from typing import TypeVar

T = TypeVar("T", bound=Enum)


def _try_convert_to_enum(value: str, enum: Callable[[str], T]) -> T | str:
    """
    Simple internal wrapper to try to convert a str to a member of an Enum.

    If the value does not match any member of the Enum, it will be returned if
    and only if it starts with "x-" else a ValueError will be raised.

    Parameters
    ----------
    value : str
        THe value to convert
    enum : Callable[[str], T]
        The Enum to try and convert the value to a member of

    Returns
    -------
    T | str
        the original str or a member of the Enum

    Raises
    ------
    ValueError
        If the value does not match any member of the Enum and does not start
        with "x-"
    """
    try:
        return enum(value)
    except ValueError:
        if not value.startswith("x-"):
            raise ValueError("Custom values must start with 'x-'")
        return value


def _try_convert_to_bool(value: str) -> bool:
    """
    Simple helper that return True if value is 'yes', False if it's 'no' or
    raises a ValueError otherwise

    Parameters
    ----------
    value : str
        The value to try and convert

    Returns
    -------
    bool
        True if 'yes', False if 'no'

    Raises
    ------
    ValueError
        If value is not 'yes' or 'no'
    """
    if value == "yes":
        return True
    elif value == "no":
        return False
    else:
        raise ValueError(f"value must be 'yes' or 'no' but got {value}")
