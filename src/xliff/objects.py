from collections.abc import Callable, Mapping, MutableSequence
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
  convert_to_boolean,
  ensure_enum,
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
    """
    Serializes the object to an XML element using the provided factory.

    By default, this uses `lxml.etree.Element`, but you may supply either the Standard
    library's `Element` function, or any function that can return an object that follows
    the `ElementLikeProtocol` from a str (the element's tag) and a dict[str, str] (the
    element's attrib).

    Args:
        element_factory: A callable that returns an XML element object given a tag name
        and a dictionary of attributes. Defaults to `lxml.etree.Element`.

    Returns:
        ElementLike: The resulting XML element, a `lxml.etree._Element`,
        `xml.etree.ElementTree.Element` or any object adhering to the `ElementLikeProtocol`
    """
    if element_factory is None:
      # Getting around BOTH lxml and ElementTree typing is a mega mess
      # Just ignoring here until something breaks...
      element_factory = let.Element  # type: ignore
    return self._to_element(element_factory)  # type: ignore


class BaseXliffElement(ElementSerializationMixin):
  _xml_tag: ClassVar[str]
  _xml_attribute_map: ClassVar[dict[str, str]]
  _has_content: ClassVar[bool]
  _source_element: Optional[ElementLike]
  __slots__ = ("_source_element",)

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
        dict: A dict of all the object's attributes that should be attributes in its
        xml representation, ready for serialization.
    """
    return {
      xml_name: stringify(getattr(self, attribute))
      for attribute, xml_name in self._xml_attribute_map.items()
      if getattr(self, attribute) is not None
    }

  def _to_element(self, element_factory: Callable[..., ElementLike]) -> ElementLike:
    element_factory_ = let.Element if element_factory is None else element_factory
    element = element_factory_(self._xml_tag, self._attribute_dict)
    return element

  def validate(self, *, raise_on_error: bool = True) -> bool:
    """
    Validates that all the the attributes of the objects are of an expected type.

    The optional `raise_on_error` argument can be used to simply return False instead
    of raising.

    In some implementations, the `recurse`flag can also be set to recursively validate
    all the object's children as well.

    Args:
        raise_on_error (bool, optional): If the function should raise a TypeError or simply return False. Defaults to True.
        recurse (bool, optional): If the object's children should also be validated. Defaults to True.

    Raises:
        TypeError: If one of the object's attribute is not one of its expected type.

    Returns:
        bool: True if the object is valid and ready for serialization or False if
        `raise_on_error` is False and the object is incorrect.
    """
    raise NotImplementedError


class Count(BaseXliffElement):
  _has_content = True
  _xml_tag = "count"
  _xml_attribute_map = {
    "count_type": "count-type",
    "phase_name": "phase-name",
    "unit": "unit",
  }
  _value: int
  count_type: str | COUNT_TYPE
  phase_name: Optional[str]
  unit: Optional[str | UNIT]

  __slots__ = (
    "value",
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
    """Represents an XLIFF `<count>` element used for count metrics.

    When initilizing using explicit values only, both `value` AND `count_type` are required.

    Args:
      source_element (Optional[ElementLike]): An optional xml Element to parse all values from value (int): The numeric value associated with the count element.
      count_type (str | COUNT_TYPE): Type of count (e.g., 'word', 'character'). Ideally one of the `COUNT_TYPE` StrEnum. If using a custom value as a str, please ensure it is preppended with 'x-'
      phase_name (Optional[str]): Optional phase name referencing the `Phase` in which the count was produced.
      unit (Optional[str | UNIT]): Optional unit for the count (e.g., 'word', 'segment'). Ideally one of the `UNIT` StrEnum. If using a custom value as a str, please ensure it is preppended with 'x-'

    Raises:
      TypeError: If `source_element` is not a valid XML element-like object, or one of the attibute is not the correct type.
      ValueError: If required attributes are missing or the tag of the element is incorrect.
    """
    super().__init__(**kwargs)
    if self.count_type is None:
      raise ValueError("Missing a value for attribute 'count_type'")
    else:
      self.count_type = ensure_enum(self.count_type, COUNT_TYPE)
    if self.unit is not None:
      self.unit = ensure_enum(self.unit, UNIT)

  @override
  def _init_content(self, **kwargs):
    if "value" in kwargs:
      self.value = kwargs["value"]
    elif self._source_element is None or self._source_element.text is None:
      raise ValueError("Missing a value for attribute 'value'")
    else:
      self.value = int(self._source_element.text)

  def _to_element(self, element_factory):
    element = super()._to_element(element_factory)
    element.text = stringify(self.value)
    return element

  @override
  def validate(self, *, raise_on_error: bool = True) -> bool:
    # required
    if not isinstance(self.value, int):
      if raise_on_error:
        raise TypeError(f"Expected a int for 'value' but got {type(self.value)}")
      return False
    # enums
    try:
      ensure_enum(self.count_type, COUNT_TYPE)
    except (TypeError, ValueError) as e:
      if raise_on_error:
        raise TypeError(
          f"Expected a COUNT_TYPE or str starting with 'x-' for 'count_type' but got {type(self.value)}"
        ) from e
      return False
    if self.unit is not None:
      try:
        ensure_enum(self.unit, UNIT)
      except (TypeError, ValueError) as e:
        if raise_on_error:
          raise TypeError(
            f"Expected a UNIT or str starting with 'x-' for 'unit' but got {type(self.unit)}"
          ) from e
        return False
    # optional
    if self.phase_name is not None and not isinstance(self.phase_name, str):
      if raise_on_error:
        raise TypeError(
          f"Expected a str or None for 'phase_name' but got {type(self.phase_name)}"
        )
      return False
    return True


class CountGroup(BaseXliffElement):
  _xml_tag = "count-group"
  _xml_attribute_map = {
    "name": "name",
  }
  _has_content = True
  __slots__ = ("name", "counts")
  name: str
  counts: MutableSequence[Count]

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
    Represents an XLIFF `<count-group>` element used for grouping <count> metrics.

    When initializing using explicit values only, `name` is required.

    Args:
      source_element (Optional[ElementLike]): An optional xml Element to parse all values from
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

  def _to_element(self, element_factory):
    element = super()._to_element(element_factory)
    for count in self.counts:
      element.append(count.to_element(element_factory))
    return element

  @override
  def validate(self, *, recurse: bool = False, raise_on_error: bool = True) -> bool:
    # required
    if not isinstance(self.name, str):
      if raise_on_error:
        raise TypeError(f"Expected a str for 'name' but got {type(self.name)}")
      return False
    # recurse
    if recurse:
      for count in self.counts:
        try:
          if not isinstance(count, Count) or not count.validate(
            raise_on_error=raise_on_error
          ):
            return False
        except TypeError as e:
          if raise_on_error:
            raise TypeError(
              f"Expected an Iterable of `Count` for 'counts' but got {type(count)}"
            ) from e
          return False
    return True


class Context(BaseXliffElement):
  _xml_tag = "context"
  _xml_attribute_map = {
    "context_type": "context-type",
    "match_mandatory": "match-mandatory",
    "crc": "crc",
  }
  _has_content = True
  __slots__ = (
    "value",
    "context_type",
    "match_mandatory",
    "crc",
  )
  value: str
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
    """
    Represents an XLIFF `<context>` element used to define contextual information.

    When initializing using explicit values only, both `value` AND `context_type` are required.

    Args:
      source_element (Optional[ElementLike]): An optional xml Element to parse all values from.
      value (str): The textual content of the context.
      context_type (CONTEXT_TYPE): Type of context (e.g., 'segment', 'location'). Ideally one of the `CONTEXT_TYPE` StrEnum. If using a custom value as a str, please ensure it is preppended with 'x-'
      match_mandatory (Optional[bool]): If the context match is mandatory.
      crc (Optional[str]): Optional checksum for context identification.

    Raises:
      TypeError: If `source_element` is not a valid XML element-like object, or one of the attributes is not the correct type.
      ValueError: If required attributes are missing or the tag of the element is incorrect.
    """
    super().__init__(**kwargs)
    if self.context_type is None:
      raise ValueError("Missing a value for attribute 'context_type'")
    self.context_type = ensure_enum(self.context_type, CONTEXT_TYPE)
    if self.match_mandatory is not None:
      self.match_mandatory = convert_to_boolean(self.match_mandatory)

  def _init_content(self, **kwargs):
    if "value" in kwargs:
      self.value = kwargs["value"]
    elif self._source_element is None or self._source_element.text is None:
      raise ValueError("Missing a value for attribute 'value'")
    else:
      self.value = self._source_element.text

  def _to_element(self, element_factory):
    element = super()._to_element(element_factory)
    element.text = self.value
    return element

  @override
  def validate(self, *, raise_on_error: bool = True) -> bool:
    # required
    if not isinstance(self.value, str):
      if raise_on_error:
        raise TypeError(f"Expected a str for 'value' but got {type(self.value)}")
      return False

    # enums
    try:
      ensure_enum(self.context_type, CONTEXT_TYPE)
    except (TypeError, ValueError) as e:
      if raise_on_error:
        raise TypeError(
          f"Expected a `CONTEXT_TYPE` or str starting with 'x-' for 'context_type' but got {type(self.context_type)}"
        ) from e
      return False

    # optional
    if self.crc is not None and not isinstance(self.crc, str):
      if raise_on_error:
        raise TypeError(f"Expected a str or None for 'crc' but got {type(self.crc)}")
      return False
    if self.match_mandatory not in (None, True, False):
      if raise_on_error:
        raise TypeError(
          f"Expected a bool or None for 'match_mandatory' but got {type(self.match_mandatory)}"
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
  __slots__ = ("crc", "name", "purpose", "contexts")
  crc: Optional[str]
  name: Optional[str]
  purpose: Optional[PURPOSE]
  contexts: MutableSequence[Context]

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
    """
    Represents an XLIFF `<context-group>` element used for grouping <context> elements.

    All attributes are optional.

    Args:
      source_element (Optional[ElementLike]): An optional xml Element to parse all values from.
      name (Optional[str]): Optional name for the context group.
      purpose (Optional[str | PURPOSE]): Optional purpose of the context group. Ideally one of the `PURPOSE` StrEnum. If using a custom value as a str, please ensure it is preppended with 'x-'
      crc (Optional[str]): Optional checksum for the context group.
      contexts (MutableSequence[Context]): A MutableSequence of `Context` objects contained within the group. Defaults to an empty list.

    Raises:
      TypeError: If `source_element` is not a valid XML element-like object, or one of the attributes is not the correct type.
      ValueError: If required attributes are missing or the tag of the element is incorrect.
    """

    super().__init__(**kwargs)
    if self.purpose is not None:
      self.purpose = ensure_enum(self.purpose, PURPOSE)

  def _init_content(self, **kwargs):
    if "contexts" in kwargs:
      self.contexts = kwargs["contexts"]
    elif self._source_element is None or not len(self._source_element):
      self.contexts = []
    else:
      self.contexts = [
        Context(source_element=context) for context in self._source_element
      ]

  def _to_element(self, element_factory=None):
    element = super()._to_element(element_factory)
    for context in self.contexts:
      element.append(context.to_element(element_factory))
    return element

  def validate(self, *, recurse: bool = False, raise_on_error: bool = True) -> bool:
    # Optional
    if self.name is not None and not isinstance(self.name, str):
      if raise_on_error:
        raise TypeError(f"Expected a str or None for 'name' but got {type(self.name)}")
      return False
    if self.crc is not None and not isinstance(self.crc, str):
      if raise_on_error:
        raise TypeError(f"Expected a str or None for 'crc' but got {type(self.crc)}")
      return False
    # enums
    if self.purpose is not None:
      try:
        ensure_enum(self.purpose, PURPOSE)
      except (TypeError, ValueError) as e:
        if raise_on_error:
          raise TypeError(
            f"Expected a `PURPOSE` or str starting with 'x-' for 'purpose' but got {type(self.purpose)}"
          ) from e
        return False
    # recurse
    if recurse:
      for context in self.contexts:
        try:
          if not isinstance(context, Context) or not context.validate(
            raise_on_error=raise_on_error
          ):
            return False
        except TypeError as e:
          if raise_on_error:
            raise TypeError(
              f"Expected an Iterable of `Context` for 'contexts' but got {type(context)}"
            ) from e
          return False
    return True
