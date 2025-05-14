from datetime import datetime
from enum import Enum
from typing import Any, TypeGuard, TypeVar, overload
from xml.etree.ElementTree import Element
from lxml.etree import _Element
from xliff.constants import __FAKE__ELEMENT__, ElementLikeProtocol


def ensure_correct_element(expected_tag: str, element: Any) -> None:
  """
  Ensures that the given XML element has the expected tag name.

  Args:
      expected_tag (str): The expected XML tag name.
      element (Any): The XML element to validate.

  Raises:
      ValueError: If the tag name of the element does not match the expected tag.
  """
  if element is not __FAKE__ELEMENT__ and element.tag != expected_tag:
    raise ValueError(
      f"Incorrect xml tag. Expected <{expected_tag}> but got <{element.tag!r}>"
    )


def ensure_usable_element(
  unknown_element: Any,
) -> TypeGuard[ElementLikeProtocol | _Element | Element]:
  """
  Determines whether the given object is usable as an XML element.

  Checks if the object is either a known XML element type or implements
  the required interface (tag, text, tail, attrib).

  Args:
      unknown_element (Any): The object to verify.

  Returns:
      bool: True if the object can be used as an XML element, False otherwise.
  """
  if isinstance(unknown_element, (_Element, Element)):
    return True
  for attr in ("text", "tail", "tag", "attrib"):
    if not hasattr(unknown_element, attr):
      return False
  return True


def stringify(value: Any) -> str:
  """
  Converts a Python value into a string suitable for XML serialization.

  Supported types include: str, int, float, datetime, Enum, and bool.

  Args:
      value (Any): The value to convert.

  Returns:
      str: The stringified representation of the value.

  Raises:
      NotImplementedError: If the value type is unsupported.
  """
  match value:
    case str() | int() | float():
      return str(value)
    case datetime():
      return value.strftime("%Y%m%dT%H%M%SZ")
    case Enum():
      return value.value
    case bool():
      return "yes" if value is True else "no"
    case _:
      raise NotImplementedError


def convert_to_boolean(value: Any) -> bool:
  """
  Converts a string to a boolean value, returns the value if already a boolean.

  Args:
      value (str | bool): The input value to convert.

  Returns:
      bool: The corresponding boolean value.

  Raises:
      TypeError: If input is not a boolean or one of the valid strings ('yes', 'no').
  """
  match value:
    case True | False:
      return value
    case "yes":
      return True
    case "no":
      return False
    case _:
      raise TypeError(f"expected a bool or one of 'yes' or 'no' but got {value!r}")


T = TypeVar("T", bound=Enum)


@overload
def ensure_enum(value: T, enum: type[T]) -> T: ...
@overload
def ensure_enum(value: str | T, enum: type[T]) -> str | T: ...
def ensure_enum(value: str | T, enum: type[T]) -> str | T:
  """
  Converts `value` to a member of `enum` if possible or returns it as-is if it is a
  `str` starting with 'x-'

  Args:
    value (Any): the value to check
    enum (T): The enum to convert to

  Returns:
    T | str: A member of the Enum or the string it if it starts with 'x-'

  Raises:
    TypeError: If `value` is not a str
    ValueError: If `value` cannot be converted to a member of the Enum and it doesn't starts with 'x-'
  """
  if isinstance(value, enum):
    return value
  elif isinstance(value, str):
    if value.startswith("x-"):
      return value
    return enum(value)
  else:
    raise TypeError(f"expected a string or a member of {enum} but got {type(value)}")


def validate_type(
  value: Any,
  *,
  expected_type: type | tuple[type, ...],
  name: str,
  optional: bool = False,
) -> None:
  """Generic type validator with standardized error messages."""
  if value is None:
    if not optional:
      raise TypeError(f"Required attribute '{name}' cannot be None")
  if not isinstance(value, expected_type):
    type_name = getattr(expected_type, "__name__", str(expected_type))
    raise TypeError(f"Expected {type_name} for '{name}' but got {type(value)}")


def validate_enum(
  value: Any,
  *,
  enum_class: type[Enum],
  name: str,
  optional: bool = False,
) -> None:
  """Validates that a value is either an enum instance or a valid string."""
  if value is None:
    if not optional:
      raise TypeError(f"Required attribute '{name}' cannot be None")
  match value:
    case None if not optional:
      raise ValueError(f"Required attribute '{name}' cannot be None")
    case value if value in enum_class:
      return
    case str():
      if not value.startswith("x-"):
        raise ValueError(
          f"{value} doesn't start with 'x-' (found {value[:2]} nor is it part of {enum_class.__name__})"
        )
    case _:
      raise TypeError(
        f"Expected {enum_class.__name__} or str starting with 'x-' for '{name}' but got {type(value)}"
      )
