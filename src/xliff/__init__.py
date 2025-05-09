from collections.abc import Mapping
from typing import Optional, Protocol
import lxml.etree as et
import xml.etree.ElementTree as ET


class ElementProtocol(Protocol):
  tag: str
  text: Optional[str]
  tail: Optional[str]
  attrib: Mapping[str, str]


type ElementLike = ElementProtocol | et._Element | ET.Element
__TEMP_ELEMENT__ = et.Element("fake")
