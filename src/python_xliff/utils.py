from collections.abc import Callable
from enum import Enum
from typing import Literal, TypeVar, overload

T = TypeVar("T", bound=Enum)


@overload
def _coerce_str_to_enum(
    value: str | Enum | None,
    enum: Callable[[str | Enum], T],
    error_on_none: Literal[False],
) -> T | str | None: ...
@overload
def _coerce_str_to_enum(
    value: str | Enum | None,
    enum: Callable[[str | Enum], T],
    error_on_none: Literal[True],
) -> T | str: ...
@overload
def _coerce_str_to_enum(
    value: str | Enum | None,
    enum: Callable[[str | Enum], T],
    error_on_none: bool,
) -> T | str | None: ...
def _coerce_str_to_enum(
    value: str | Enum | None,
    enum: Callable[[str | Enum], T],
    error_on_none: bool,
) -> T | str | None:
    if value is None:
        if error_on_none:
            raise TypeError("value cannot be None")
        return value
    if isinstance(value, Enum):
        return enum(value)
    if isinstance(value, str):
        if value.startswith("x-"):
            return value
        else:
            return enum(value)
    else:
        raise TypeError(
            f"value must be a string starting with 'x-' or a member of {enum.__name__}"
        )


@overload
def _coerce_str_to_bool(value: str | None, error_on_none: Literal[True]) -> bool: ...
@overload
def _coerce_str_to_bool(
    value: str | None, error_on_none: Literal[False]
) -> bool | None: ...
@overload
def _coerce_str_to_bool(value: str | None, error_on_none: bool) -> bool | None: ...
def _coerce_str_to_bool(value: str | None, error_on_none: bool) -> bool | None:
    if value is None:
        if error_on_none:
            raise TypeError("value cannot be None")
        return value
    if value == "yes":
        return True
    elif value == "no":
        return False
    else:
        raise ValueError(f"value must be 'yes' or 'no' but got {value}")


def _export_enum(value: str | Enum, enum: Callable[[str | Enum], T]) -> str:
    if isinstance(value, str):
        if value.startswith("x-"):
            return value
        else:
            raise ValueError(f"value must start with 'x-' but got {value}")
    elif isinstance(value, Enum):
        return value.value
    else:
        raise TypeError(
            f"value must be a string starting with 'x-' or a member of {enum.__name__}"
        )


@overload
def _export_bool(value: Literal[True]) -> Literal["yes"]: ...
@overload
def _export_bool(value: Literal[False]) -> Literal["no"]: ...
@overload
def _export_bool(value: bool) -> Literal["yes", "no"]: ...
def _export_bool(value: bool) -> Literal["yes", "no"]:
    if not isinstance(value, bool):
        raise TypeError("value must be a boolean")
    return "yes" if value else "no"
