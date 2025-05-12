from collections.abc import Callable, Generator, Iterable, Mapping, MutableSequence
from types import NoneType
from typing import ClassVar, Optional, overload, override
from xliff.constants import (
  __FAKE__ELEMENT__,
  ElementLike,
  Python_ElementFactory,
  ElementLikeProtocol,
  CONTEXT_TYPE,
  COUNT_TYPE,
  PURPOSE,
  UNIT,
)
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

  def _to_element(self, element_factory: Callable) -> ElementLike:
    raise NotImplementedError

  @overload
  def to_element(
    self, element_factory: Callable[[str, Mapping[str, str]], ElementLikeProtocol]
  ) -> ElementLikeProtocol: ...
  @overload
  def to_element(self, element_factory: Python_ElementFactory) -> pet.Element: ...
  @overload
  def to_element(self, element_factory: None = None) -> let._Element: ...
  def to_element(
    self,
    element_factory: Optional[
      Python_ElementFactory | Callable[[str, Mapping[str, str]], ElementLikeProtocol]
    ] = None,
  ) -> ElementLikeProtocol | let._Element | pet.Element:
    if element_factory is None:
      # Getting around BOTH lxml and ElementTree typing is a mega mess
      # Just ignoring here until something breaks...
      element_factory = let.Element  # type: ignore
    return self._to_element(element_factory)  # type: ignore


class BaseXliffElement(ElementSerializationMixin):
  _xml_tag: ClassVar[str]
  _source_element: Optional[ElementLike]
  _required_attrs: tuple[str, ...]
  _xml_attribute_map: ClassVar[dict[str, str]]
  __slots__ = (
    "_xml_tag",
    "_source_element",
    "_required_attrs",
    "_xml_attribute_map",
  )
  _has_content: ClassVar[bool]

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
    if self.__class__._has_content:
      self._init_content(**kwargs)
    self._init_xml_attributes(source_element, **kwargs)

  def _init_content(self, **kwargs) -> None:
    raise NotImplementedError

  def _init_xml_attributes(self, source_element: ElementLike, **kwargs) -> None:
    # assign attribute values, prioritizing kwargs over the source_element
    for attribute, xml_name in self._xml_attribute_map.items():
      if attribute in kwargs:  # Explicit value given
        setattr(self, attribute, kwargs[attribute])
      elif (
        xml_name in source_element.attrib
      ):  # No explicit value, check the source element
        setattr(self, attribute, source_element.attrib[xml_name])
      else:
        setattr(self, attribute, None)  # not found anywhere, setting to None

  @property
  def _attribute_dict(self) -> dict[str, str]:
    """
    A dict representation of the object's attributes.

    Only includes the attributes that should become xml attributes.

    Returns:
        dict[str, str]: A dict od the object's attributes, ready to be serialized.
    """
    return {
      xml_name: stringify(getattr(self, attribute))
      for attribute, xml_name in self._xml_attribute_map.items()
      if getattr(self, attribute) is not None
    }

  def _to_element(self, element_factory: Callable[..., ElementLike]) -> ElementLike:
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
      if getattr(self, attr) is None:
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
  _has_content = True
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
    if self.count_type is None:
      raise ValueError("Missing a value for attribute 'count_type'")
    else:
      self.count_type = COUNT_TYPE(self.count_type)
    if self.unit is not None:
      self.unit = UNIT(self.unit)

  @override
  def _init_content(self, **kwargs):
    if "value" in kwargs:
      self.value = kwargs["value"]
    elif self._source_element is None or self._source_element.text is None:
      raise ValueError("Missing a value for attribute 'value'")
    else:
      self.value = int(self._source_element.text)

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
      "phase_name": (str, NoneType),
    }.items():
      if not isinstance(getattr(self, attr), expected_type):
        if raise_on_error:
          raise TypeError(
            f"Expected a {expected_type} for attribute {attr} but got {type(getattr(self, attr))!r}"
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
  _has_content = True
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
    if not isinstance(self.name, str):
      raise ValueError("No value provided for required attribute 'name'")

  def _init_content(self, **kwargs):
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

  def _to_element(self, element_factory):
    element = super()._to_element(element_factory)
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
  _has_content = True
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
    if self.context_type is None:
      raise ValueError("Missing a value for attribute 'context_type'")
    self.context_type = CONTEXT_TYPE(self.context_type)
    if self.match_mandatory is not None:
      self.match_mandatory = ensure_boolean(self.match_mandatory)

  def _init_content(self, **kwargs):
    if "value" in kwargs:
      self.value = kwargs["value"]
    elif self._source_element is None or self._source_element.text is None:
      raise ValueError("Missing a value for attribute 'value'")
    else:
      self.value = self._source_element.text

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
      if not isinstance(getattr(self, attr), expected_type):
        if raise_on_error:
          raise TypeError(
            f"Expected a {expected_type} for attribute {attr} but got {type(getattr(self, attr))!r}"
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
  _has_content = True
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

  def _init_content(self, **kwargs):
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

  def _to_element(self, element_factory=None):
    element = super()._to_element(element_factory)
    for context in self._contexts:
      element.append(context.to_element(element_factory))
    return element

  def validate(self, *, recurse: bool = False, raise_on_error: bool = True) -> bool:
    for attr, expected_type in {
      "name": (str, NoneType),
      "crc": (str, NoneType),
      "purpose": (PURPOSE, NoneType),
    }.items():
      if not isinstance(getattr(self, attr), expected_type):
        if raise_on_error:
          raise TypeError(
            f"Expected a {expected_type} for attribute {attr} but got {type(getattr(self, attr))!r}"
          )
        return False
    if recurse:
      for context in self.contexts:
        if not context.validate(raise_on_error=raise_on_error):
          return False
    return True
