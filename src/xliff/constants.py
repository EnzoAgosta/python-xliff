from enum import StrEnum
from typing import TypeVar
from collections.abc import Callable, Mapping
from typing import Any, Optional, Protocol, Self, TypeAlias
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
_ElementFactory: TypeAlias = Callable[[Any, dict[Any, Any]], ET.Element]


T = TypeVar("T", bound=ElementLike)


class COUNT_TYPE(StrEnum):
  NUM_USAGE = "num-usage"
  """
  Indicates the count units are items that are used X times in a certain context
  """
  REPETITION = "repetition"
  """
  Indicates the count units are translation units existing already in the same document.
  """
  TOTAL = "total"
  """
  Indicates a total count.
  """


class UNIT(StrEnum):
  WORD = "word"
  """
  Refers to words.
  """
  PAGE = "page"
  """
  Refers to pages.
  """
  TRANS_UNIT = "trans-unit"
  """
  Refers to <trans-unit> elements.
  """
  BIN_UNIT = "bin-unit"
  """
  Refers to <bin-unit> elements.
  """
  GLYPH = "glyph"
  """
  Refers to glyphs.
  """
  ITEM = "item"
  """
  Refers to <trans-unit> and/or <bin-unit> elements.
  """
  INSTANCE = "instance"
  """
  Refers to the occurrences of instances defined by the count-type value.
  """
  CHARACTER = "character"
  """
  Refers to characters.
  """
  LINE = "line"
  """
  Refers to lines.
  """
  SENTENCE = "sentence"
  """
  Refers to sentences.
  """
  PARAGRAPH = "paragraph"
  """
  Refers to paragraphs.
  """
  SEGMENT = "segment"
  """
  Refers to segments.
  """
  PLACEABLE = "placeable"
  """
  Refers to placeables (inline elements).
  """


class CONTEXT_TYPE(StrEnum):
  DATABASE = "database"
  """
  Indicates a database content.
  """
  ELEMENT = "element"
  """
  Indicates the content of an element within an XML document.
  """
  ELEMENTTITLE = "elementtitle"
  """
  Indicates the name of an element within an XML document.
  """
  LINENUMBER = "linenumber"
  """
  Indicates the line number from the sourcefile (see context-type="sourcefile") where
  the <source> is found.
  """
  NUMPARAMS = "numparams"
  """
  Indicates a the number of parameters contained within the <source>.
  """
  PARAMNOTES = "paramnotes"
  """
  Indicates notes pertaining to the parameters in the <source>.
  """
  RECORD = "record"
  """
  Indicates the content of a record within a database.
  """
  RECORDTITLE = "recordtitle"
  """
  Indicates the name of a record within a database.
  """
  SOURCEFILE = "sourcefile"
  """
  Indicates the original source file in the case that multiple files are merged to form
  the original file from which the XLIFF file is created. This differs from the original
  <file> attribute in that this sourcefile is one of many that make up that file.
  """


class PURPOSE(StrEnum):
  INFORMATION = "information"
  """
  Indicates that the context is informational in nature, specifying for example, how a
  term should be translated. Thus, should be displayed to anyone editing the XLIFF
  document.
  """
  LOCATION = "location"
  """
  Indicates that the context-group is used to specify where the term was found in the
  translatable source. Thus, it is not displayed.
  """
  MATCH = "match"
  """
  Indicates that the context information should be used during translation memory lookups.
  Thus, it is not displayed.
  """
