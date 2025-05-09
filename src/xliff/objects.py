from collections.abc import Generator, Iterable, MutableSequence
from typing import ClassVar, Optional, overload
from xml.dom import XML_NAMESPACE
from xliff import __TEMP_ELEMENT__, ElementLike
from xliff.utils import ensure_correct_element, ensure_usable_element


class BaseXliffElement:
  _xml_tag: ClassVar[str]
  _source_element: Optional[ElementLike]
  _required_attrs: tuple[str, ...]
  __slots__ = ("_xml_tag", "_source_element", "_required_attrs")

  def __init__(self, **kwargs) -> None:
    source_element = kwargs.pop("source_element", __TEMP_ELEMENT__)
    if not ensure_usable_element(source_element):
      raise TypeError(f"{source_element!r} is not a valid XML Element like object")
    ensure_correct_element(self._xml_tag, source_element)
    for attribute in self.__slots__:
      if attribute.startswith("_"):
        continue
      if attribute in kwargs:
        self.__setattr__(attribute, kwargs[attribute])
      if attribute in source_element.attrib:
        self.__setattr__(attribute, source_element.attrib[attribute])
      elif (o_attr := f"o-{attribute}") in source_element.attrib:
        self.__setattr__(attribute, kwargs[o_attr])
      elif (dash_attr := attribute.replace("_", "-")) in source_element.attrib:
        self.__setattr__(attribute, source_element.attrib[dash_attr])
      elif (xml_attr := f"{{{XML_NAMESPACE}}}{attribute}") in source_element.attrib:
        self.__setattr__(attribute, source_element.attrib[xml_attr])
      else:
        if attribute in self._required_attrs:
          raise ValueError(f"No value provided for required attr {attribute}")
        self.__setattr__(attribute, None)
    self._source_element = (
      source_element if source_element is not __TEMP_ELEMENT__ else None
    )


class Count(BaseXliffElement):
  _xml_tag = "count"
  _value: int
  count_type: str
  phase_name: Optional[str]
  unit: Optional[str]

  _required_attrs = ("value", "count_type")

  __slots__ = (
    "_value",
    "count_type",
    "phase_name",
    "unit",
  )

  @overload
  def __init__(self, *, source_element: ElementLike) -> None: ...
  @overload
  def __init__(
    self,
    *,
    source_element: ElementLike,
    value: Optional[int] = None,
    count_type: Optional[str] = None,
    phase_name: Optional[str] = None,
    unit: Optional[str] = None,
  ) -> None: ...
  @overload
  def __init__(
    self,
    *,
    value: int,
    count_type: str,
    phase_name: Optional[str] = None,
    unit: Optional[str] = None,
  ) -> None: ...
  def __init__(self, **kwargs) -> None:
    """
    Represents an XLIFF <count> element used for count metrics.

    This class can be initialized in one of the following ways:
    1. From an existing XML element:
        ```python
          Count(source_element=element)
        ```
    2. From an XML element with optional overrides:
        ```python
          Count(
            source_element=element,
            value=123,
            count_type="word",
            phase_name="translation",
            unit="word",
          )
        ```
    3. Directly via explicit values (no XML element):
        ```python
          Count(
            value=123,
            count_type="word",
            phase_name="translation",
            unit="word",
          )
        ```
        When initilizing using explicit values only, both `value` AND `count_type` are required.

    Attributes:
        value (int): The numeric value associated with the count element.
        count_type (str): Type of count (e.g., 'word', 'character').
        phase_name (Optional[str]): Optional phase name referencing the `Phase` in which the count was produced.
        unit (Optional[str]): Optional unit for the count (e.g., 'word', 'segment').

    Raises:
        TypeError: If `source_element` is not a valid XML element-like object.
        ValueError: If required attributes are missing.
    """
    super().__init__(**kwargs)
    if "value" in kwargs:
      self.value = kwargs["value"]
    elif self._source_element is not None:
      if self._source_element.text is None:
        raise ValueError("No value provided for required attribute 'value'")
      self.value = int(self._source_element.text)

  @property
  def value(self) -> int:
    return self._value

  @value.setter
  def value(self, value: int) -> None:
    self._value = value


class CountGroup(BaseXliffElement):
  _xml_tag = "count-group"
  name: str
  _counts: MutableSequence[Count]

  __slots__ = ("name", "_counts")

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    if self.name is None:
      raise ValueError("No value provided for required attribute 'name'")
    if "counts" in kwargs:
      self.counts = kwargs["counts"]
    elif self._source_element is not None and len(self._source_element):
      self.counts = [Count(source_element=count) for count in self._source_element]
    else:
      self.counts = []

  @property
  def counts(self) -> MutableSequence[Count]:
    return self._counts

  @counts.setter
  def counts(self, value: MutableSequence[Count]) -> None:
    self._counts = value

  # Convenience Sequence methods
  def __iter__(self) -> Generator[Count]:
    yield from self._counts

  def __len__(self) -> int:
    return len(self._counts)

  def append(self, count: Count) -> None:
    self._counts.append(count)

  def extend(self, counts: Iterable[Count]) -> None:
    self._counts.extend(counts)
