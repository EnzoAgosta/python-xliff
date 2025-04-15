from enum import Enum
from typing import Any, TypeVar

from langcodes import Language

T = TypeVar("T", bound=Enum)


def validate_enum_or_custom_str_attr_value(enum: type[T], value: str | Enum) -> str | T:
    """
    Validation function for enums and custom strings. Meant for use with partials
    and pydantic's AfterValidator.

    Ensures that the value is a member of the enum or starts with "x-".

    Parameters
    ----------
    enum : type[Enum]
        The Enum to check against.
    value : str
        The value to check.

    Returns
    -------
    str | Enum
        The Enum value if the value is a member of the enum or the raw value if
        it is a string starting with "x-".

    Raises
    ------
    ValueError
        If the value is not a member of the enum and does not start with "x-".
    TypeError
        If the value is not a string nor a member of the enum.
    """
    if value is None:
        return value
    elif value in enum:
        return enum(value)
    elif isinstance(value, str) and value.startswith("x-"):
        return value
    else:
        raise TypeError(
            "value must be a string starting with 'x-' or a member of "
            f"{enum.__name__} but got {value!r}"
        )


def validate_language(value: Any) -> Language:
    """
    Validation function for Languages.

    Simple wrapper around `tag_is_valid` function from `langcodes` package that
    raises a `ValueError` if the language is not valid.

    Parameters
    ----------
    value : str
        The value to check.

    Returns
    -------
    Language
        The Language object.

    Raises
    ------
    ValueError
        If the language is not valid.
    """
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    lang = Language.get(value)
    if not lang.is_valid():
        raise ValueError(f"Language {value} is not valid")
    return lang
