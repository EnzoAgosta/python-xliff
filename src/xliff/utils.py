from typing import Any, TypeIs
from xml.etree.ElementTree import Element
from lxml.etree import _Element
from xliff import __TEMP_ELEMENT__
from xliff import ElementProtocol


def ensure_correct_element(expected_tag: str, element: Any) -> None:
  if element is not __TEMP_ELEMENT__ and element.tag != expected_tag:
    raise ValueError(
      f"Incorrect xml tag. Expected <{expected_tag}> but got <{element.tag!r}>"
    )


def ensure_usable_element(
  unknown_element: Any,
) -> TypeIs[ElementProtocol | _Element | Element]:
  if isinstance(unknown_element, (_Element, Element)):
    return True
  for attr in ("text", "tail", "tag", "attrib"):
    if not hasattr(unknown_element, attr):
      return False
  return True
