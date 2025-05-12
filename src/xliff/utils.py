from datetime import datetime
from enum import StrEnum
from typing import Any, TypeIs
from xml.etree.ElementTree import Element
from lxml.etree import _Element
from xliff import __FAKE__ELEMENT__
from xliff import ElementLikeProtocol


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
) -> TypeIs[ElementLikeProtocol | _Element | Element]:
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

  Supported types include: str, int, float, datetime, StrEnum, and bool.

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
    case StrEnum():
      return value.value
    case bool():
      return "yes" if value else "no"
    case _:
      raise NotImplementedError


def ensure_boolean(value: Any) -> bool:
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
