from collections.abc import Mapping
from typing import Optional, Protocol, Self
import lxml.etree as et
import xml.etree.ElementTree as ET

__FAKE__ELEMENT__ = et.Element("fake")


class ElementLikeProtocol(Protocol):
  """
  A protocol defining the minimal interface expected of XML element-like objects.

  Any object that supports this protocol can be used as a replacement for lxml and the
  standard library XML Element objects.

  Only recommended for advanced users, if possible, stick to using lxml.
  """

  tag: str | bytes
  text: Optional[str]
  tail: Optional[str]
  attrib: Mapping[str, str]

  def append(self, other: Self) -> None: ...


type ElementLike = ElementLikeProtocol | et._Element | ET.Element
