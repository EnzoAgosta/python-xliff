from collections.abc import Callable, Generator, Iterable, Mapping, MutableSequence
from types import NoneType
from typing import ClassVar, Optional, overload, override
from xliff import __FAKE__ELEMENT__, ElementLike, _ElementFactory
from xliff.constants import CONTEXT_TYPE, COUNT_TYPE, PURPOSE, T, UNIT
from xliff.utils import (
  ensure_boolean,
  ensure_correct_element,
  ensure_usable_element,
  stringify,
)
import lxml.etree as let
import xml.etree.ElementTree as pet


class ElementSerializationMixin:
  """
  Only used as a mixin for simpler type hinting for the `to_element` method.

  Lets us define the overloads once and not have to override them all the time.
  """

  @overload
  def to_element(self, element_factory: Callable[[str, Mapping[str, str]], T]) -> T: ...
  @overload
  def to_element(self, element_factory: _ElementFactory) -> pet.Element: ...
  @overload
  def to_element(self, element_factory: None) -> let._Element: ...
  def to_element(
    self,
    element_factory: Optional[
      _ElementFactory | Callable[[str, Mapping[str, str]], T]
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
    for attribute, xml_name in self._xml_attribute_map.items():
      if (value := kwargs.get(attribute)) is not None:  # Explicit value given
        self.__setattr__(attribute, value)
      elif (
        value := source_element.attrib.get(xml_name)
      ) is not None:  # No explicit value, check the source element
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
      xml_name: stringify(self.__getattribute__(attribute))
      for attribute, xml_name in self._xml_attribute_map.items()
      if self.__getattribute__(attribute) is not None
    }

  def to_element(self, element_factory=None):
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
    for attr in self._required_attrs:
      if self.__getattribute__(attr) is None:
        raise AttributeError(f"Missing value for required attribute {attr}")
    element_factory_ = let.Element if element_factory is None else element_factory
    element = element_factory_(self._xml_tag, self._attribute_dict)
    if hasattr(self, "value"):
      element.text = stringify(self.value)
    return element

  def validate(self, *, raise_on_error: bool = True) -> bool | None:
    raise NotImplementedError


class Count(BaseXliffElement):
  _xml_tag = "count"
  _xml_attribute_map = {
    "count_type": "count-type",
    "phase_name": "phase-name",
    "unit": "unit",
  }
  _required_attrs = ("value", "count_type")

  _value: int
  count_type: COUNT_TYPE
  phase_name: Optional[str]
  unit: Optional[UNIT]

  __slots__ = (
    "_value",
    "count_type",
    "phase_name",
    "unit",
  )

  @overload
  def __init__(
    self,
    *,
    source_element: ElementLike,
  ) -> None: ...
  @overload
  def __init__(
    self,
    *,
    source_element: ElementLike,
    value: Optional[int] = None,
    count_type: Optional[COUNT_TYPE | str] = None,
    phase_name: Optional[str] = None,
    unit: Optional[UNIT | str] = None,
  ) -> None: ...
  @overload
  def __init__(
    self,
    *,
    value: int,
    count_type: COUNT_TYPE | str,
    phase_name: Optional[str] = None,
    unit: Optional[UNIT | str] = None,
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
    if not hasattr(self, "_value"):
      if "value" in kwargs:
        self.value = kwargs["value"]
      elif self._source_element is None or self._source_element.text is None:
        raise ValueError("Missing a value for attribute 'value'")
      else:
        self.value = int(self._source_element.text)
    if self.count_type is None:
      raise ValueError("Missing a value for attribute 'count_type'")
    else:
      self.count_type = COUNT_TYPE(self.count_type)
    if self.unit is not None:
      self.unit = UNIT(self.unit)

  @property
  def value(self) -> int:
    return self._value

  @value.setter
  def value(self, value: int) -> None:
    self._value = value

  @override
  def validate(self, *, raise_on_error: bool = True) -> bool:
    for attr, expected_type in {
      "value": (int,),
      "count_type": (COUNT_TYPE,),
      "unit": (UNIT, NoneType),
      "phase-name": (str, NoneType),
    }.items():
      if not isinstance(self.__getattribute__(attr), expected_type):
        if raise_on_error:
          raise TypeError(
            f"Expected a {expected_type} for attribute {attr} but got {type(self.__getattribute__(attr))!r}"
          )
        return False
    return True


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
  def __init__(
    self,
    *,
    source_element: ElementLike,
  ) -> None: ...
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
    if not hasattr(self, "_counts"):
      if "counts" in kwargs:
        self.counts = kwargs["counts"]
      elif self._source_element is None or not len(self._source_element):
        self.counts = []
      else:
        self.counts = [Count(source_element=count) for count in self._source_element]

  @property
  def counts(self) -> MutableSequence[Count]:
    return self._counts

  @counts.setter
  def counts(self, value: MutableSequence[Count]) -> None:
    self._counts = value

  def __iter__(self) -> Generator[Count]:
    yield from self._counts

  def __len__(self) -> int:
    return len(self._counts)

  def append(self, count: Count) -> None:
    self._counts.append(count)

  def extend(self, counts: Iterable[Count]) -> None:
    self._counts.extend(counts)

  def to_element(self, element_factory):
    element = super().to_element(element_factory)
    for count in self.counts:
      element.append(count.to_element(element_factory))
    return element

  @override
  def validate(self, *, recurse: bool = False, raise_on_error: bool = True) -> bool:
    if not isinstance(self.name, str):
      if raise_on_error:
        raise TypeError(
          f"Expected a str for attribute name but got {type(self.name)!r}"
        )
      return False
    if recurse:
      for count in self.counts:
        if not count.validate(raise_on_error=raise_on_error):
          return False
    return True


class Context(BaseXliffElement):
  _xml_tag = "context"
  _xml_attribute_map = {
    "context_type": "context-type",
    "match_mandatory": "match-mandatory",
    "crc": "crc",
  }
  _required_attrs = ("context_type", "value")
  __slots__ = (
    "_value",
    "context_type",
    "match_mandatory",
    "crc",
  )
  _value: str
  context_type: CONTEXT_TYPE
  match_mandatory: Optional[bool]
  crc: str

  @overload
  def __init__(
    self,
    *,
    source_element: ElementLike,
  ) -> None: ...
  @overload
  def __init__(
    self,
    *,
    source_element: ElementLike,
    value: Optional[str] = None,
    context_type: Optional[str | CONTEXT_TYPE] = None,
    match_mandatory: Optional[str | bool] = None,
    crc: Optional[str] = None,
  ) -> None: ...
  @overload
  def __init__(
    self,
    *,
    value: str,
    context_type: str | CONTEXT_TYPE,
    match_mandatory: Optional[str | bool] = None,
    crc: Optional[str] = None,
  ) -> None: ...
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    if not hasattr(self, "_value"):
      if "value" in kwargs:
        self.value = kwargs["value"]
      elif self._source_element is None or self._source_element.text is None:
        raise ValueError("Missing a value for attribute 'value'")
      else:
        self.value = self._source_element.text
    if self.context_type is None:
      raise ValueError("Missing a value for attribute 'context_type'")
    self.context_type = CONTEXT_TYPE(self.context_type)
    if self.match_mandatory is not None:
      self.match_mandatory = ensure_boolean(self.match_mandatory)

  @property
  def value(self) -> str:
    return self._value

  @value.setter
  def value(self, value: str) -> None:
    self._value = value

  @override
  def validate(self, *, raise_on_error: bool = True) -> bool:
    for attr, expected_type in {
      "value": (str,),
      "context_type": (CONTEXT_TYPE,),
      "match_mandatory": (bool, NoneType),
      "crc": (str, NoneType),
    }.items():
      if not isinstance(self.__getattribute__(attr), expected_type):
        if raise_on_error:
          raise TypeError(
            f"Expected a {expected_type} for attribute {attr} but got {type(self.__getattribute__(attr))!r}"
          )
        return False
    return True


class ContextGroup(BaseXliffElement):
  _xml_tag = "context-group"
  _xml_attribute_map = {
    "crc": "crc",
    "name": "name",
    "purpose": "purpose",
  }
  _required_attrs = tuple()
  __slots__ = ("crc", "name", "purpose", "_contexts")
  crc: Optional[str]
  name: Optional[str]
  purpose: Optional[PURPOSE]
  _contexts: MutableSequence[Context]

  @overload
  def __init__(
    self,
    *,
    source_element: ElementLike,
  ) -> None: ...
  @overload
  def __init__(
    self,
    *,
    source_element: ElementLike,
    name: Optional[str] = None,
    crc: Optional[str] = None,
    purpose: Optional[str | PURPOSE] = None,
    contexts: Optional[MutableSequence[Context]] = None,
  ) -> None: ...
  @overload
  def __init__(
    self,
    *,
    name: Optional[str] = None,
    purpose: Optional[str | PURPOSE] = None,
    crc: Optional[str] = None,
    contexts: Optional[MutableSequence[Context]] = None,
  ) -> None: ...
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    if not hasattr(self, "_contexts"):
      if "contexts" in kwargs:
        self.contexts = kwargs["contexts"]
      elif self._source_element is None or not len(self._source_element):
        self.contexts = []
      else:
        self.contexts = [
          Context(source_element=context) for context in self._source_element
        ]

  @property
  def contexts(self) -> MutableSequence[Context]:
    return self._contexts

  @contexts.setter
  def contexts(self, value: MutableSequence[Context]) -> None:
    self._contexts = value

  def __iter__(self) -> Generator[Context]:
    yield from self._contexts

  def __len__(self) -> int:
    return len(self._contexts)

  def append(self, context: Context) -> None:
    self._contexts.append(context)

  def extend(self, context: Iterable[Context]) -> None:
    self._contexts.extend(context)

  def to_element(self, element_factory):
    element = super().to_element(element_factory)
    for context in self._contexts:
      element.append(context.to_element(element_factory))
    return element

  def validate(self, *, recurse: bool = False, raise_on_error: bool = True) -> bool:
    for attr, expected_type in {
      "name": (str, NoneType),
      "crc": (str, NoneType),
      "purpose": (PURPOSE, NoneType),
    }.items():
      if not isinstance(self.__getattribute__(attr), expected_type):
        if raise_on_error:
          raise TypeError(
            f"Expected a {expected_type} for attribute {attr} but got {type(self.__getattribute__(attr))!r}"
          )
        return False
    if recurse:
      for context in self.contexts:
        if not context.validate(raise_on_error=raise_on_error):
          return False
    return True
