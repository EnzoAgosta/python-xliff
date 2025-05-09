from collections.abc import Callable, Generator, Iterable, Mapping, MutableSequence
from typing import ClassVar, Optional, TypeVar, overload
from xliff import __FAKE__ELEMENT__, ElementLike
from xliff.utils import ensure_correct_element, ensure_usable_element, stringify
import lxml.etree as let
import xml.etree.ElementTree as pet

T = TypeVar("T", bound=ElementLike)


class ElementSerializationMixin:
  @overload
  def to_element(self, element_factory: Callable[[str, Mapping[str, str]], T]) -> T: ...
  @overload
  def to_element(self, element_factory: pet._ElementFactory) -> pet.Element: ...
  @overload
  def to_element(self, element_factory: None) -> let._Element: ...
  def to_element(
    self,
    element_factory: Optional[
      pet._ElementFactory | Callable[[str, Mapping[str, str]], T]
    ] = None,
  ) -> T | let._Element | pet.Element:
    raise NotImplementedError


class BaseXliffElement(ElementSerializationMixin):
  _xml_tag: ClassVar[str]
  _source_element: Optional[ElementLike]
  _required_attrs: tuple[str, ...]
  _xml_attribute_map: ClassVar[dict[str, str]]
  __slots__ = ("_xml_tag", "_source_element", "_required_attrs", "_xml_attribute_map")

  def __init__(self, **kwargs) -> None:
    # Check if we have a source xml element and ensure it's correct else use a temp
    # element to not break anything
    source_element = kwargs.pop("source_element", __FAKE__ELEMENT__)
    if not ensure_usable_element(source_element):
      raise TypeError(f"{source_element!r} is not a valid XML Element like object")
    ensure_correct_element(self._xml_tag, source_element)
    self._source_element = (
      None if source_element is __FAKE__ELEMENT__ else source_element
    )

    # assign attribute values, prioritizing kwargs over the source_element
    for attribute in self._xml_attribute_map:
      if (value := kwargs.get(attribute)) is not None:  # Explicit value given
        self.__setattr__(attribute, value)
      elif (
        value := self._xml_attribute_map[attribute]
      ) in source_element.attrib:  # No explicit value, check the source element
        self.__setattr__(attribute, value)
      else:
        self.__setattr__(attribute, None)  # not found anywhere, setting to None

  @property
  def _attribute_dict(self) -> dict[str, str]:
    """
    A dict representation of the object's attributes.

    Only includes the attributes that should become xml attributes.

    Returns:
        dict[str, str]: A dict od the object's attributes, ready to be serialized.
    """
    return {
      attribute: stringify(self.__getattribute__(attribute))
      for attribute in self._xml_attribute_map
      if self.__getattribute__(attribute) is not None
    }

  def _to_element(self, element_factory=None):
    """
    Serializes the object to an XML element using the provided factory.

    By default, this uses `lxml.etree.Element`, but the caller may supply any callable
    compatible with the signature `(tag: str, attrib: Mapping[str, str]) -> ElementLike`.

    Args:
        element_factory: A callable that returns an XML element object given a tag name
        and a dictionary of attributes. Defaults to `lxml.etree.Element`.

    Returns:
        ElementLike: The resulting XML element, a `lxml.etree._Element`,
        `xml.etree.ElementTree.Element` or any object adhering to the `ElementLikeProtocol`
    """
    element_factory_ = let.Element if element_factory is None else element_factory
    return element_factory_(self._xml_tag, self._attribute_dict)


class Count(BaseXliffElement):
  _xml_tag = "count"
  _xml_attribute_map = {
    "count_type": "count-type",
    "phase_name": "phase-name",
    "unit": "unit",
  }
  _required_attrs = ("value", "count_type")

  _value: int
  count_type: str
  phase_name: Optional[str]
  unit: Optional[str]

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

  def to_element(self, element_factory):
    element = super()._to_element(element_factory)
    element.text = str(self.value)
    return element


class CountGroup(BaseXliffElement):
  _xml_tag = "count-group"
  _xml_attribute_map = {
    "name": "name",
  }
  _required_attrs = ("name",)
  name: str
  _counts: MutableSequence[Count]

  __slots__ = ("name", "_counts")

  @overload
  def __init__(self, *, source_element: ElementLike) -> None: ...
  @overload
  def __init__(
    self,
    *,
    source_element: ElementLike,
    name: Optional[str] = None,
    counts: Optional[MutableSequence[Count]] = None,
  ) -> None: ...
  @overload
  def __init__(self, *, name: str, counts: MutableSequence[Count]) -> None: ...
  def __init__(self, **kwargs):
    """
    Represents an XLIFF <count-group> element used for grouping <count> metrics.

    This class can be initialized in one of the following ways:
    1. From an existing XML element:
        ```python
          CountGroup(source_element=element)
        ```
    2. From an XML element with optional overrides:
        ```python
          CountGroup(
            source_element=element,
            name="group1",
            counts=[Count(...), Count(...)]
          )
        ```
    3. Directly via explicit values (no XML element):
        ```python
          CountGroup(
            name="group1",
            counts=[Count(...), Count(...)]
          )
        ```
        When initializing using explicit values only, `name` is required.

    Attributes:
        name (str): The name identifier of the count group.
        counts (MutableSequence[Count]): A MutableSequence of `Count` objects contained within the group.

    Raises:
        TypeError: If `source_element` is not a valid XML element-like object.
        ValueError: If required attributes are missing.
    """
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

  def _to_element(self, element_factory):
    element = super()._to_element(element_factory)
    for count in self.counts:
      element.append(count._to_element(element_factory))
    return element
