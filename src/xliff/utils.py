from datetime import datetime
from enum import StrEnum
from typing import Any, TypeIs
from xml.etree.ElementTree import Element
from lxml.etree import _Element
from xliff import __FAKE__ELEMENT__
from xliff import ElementLikeProtocol


def ensure_correct_element(expected_tag: str, element: Any) -> None:
  if element is not __FAKE__ELEMENT__ and element.tag != expected_tag:
    raise ValueError(
      f"Incorrect xml tag. Expected <{expected_tag}> but got <{element.tag!r}>"
    )


def ensure_usable_element(
  unknown_element: Any,
) -> TypeIs[ElementLikeProtocol | _Element | Element]:
  if isinstance(unknown_element, (_Element, Element)):
    return True
  for attr in ("text", "tail", "tag", "attrib"):
    if not hasattr(unknown_element, attr):
      return False
  return True


def stringify(value: Any) -> str:
  match value:
    case str() | int() | float():
      return str(value)
    case datetime():
      return value.strftime("%Y%m%dT%H%M%SZ")
    case StrEnum():
      return value.value
    case _:
      raise NotImplementedError
