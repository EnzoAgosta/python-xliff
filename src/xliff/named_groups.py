from collections.abc import MutableSequence
from functools import partial
from typing import Optional, overload, override
from warnings import warn
from xml.dom import XML_NAMESPACE
from xliff.constants import CONTEXT_TYPE, COUNT_TYPE, PURPOSE, UNIT, ElementLike
from xliff.helpers import (
  stringify,
  try_convert_to_boolean,
  try_convert_to_enum,
  validate_enum,
  validate_type,
)
from xliff.objects import BaseXliffElement


class Count(BaseXliffElement):
  _has_content = True
  _xml_tag = "count"
  _xml_attribute_map = {
    "count_type": "count-type",
    "phase_name": "phase-name",
    "unit": "unit",
  }
  value: int
  count_type: str | COUNT_TYPE
  phase_name: Optional[str]
  unit: Optional[str | UNIT]

  _validators = {
    "value": partial(validate_type, expected=int, name="value", optional=False),
    "count_type": partial(
      validate_enum, expected=COUNT_TYPE, name="count_type", optional=False
    ),
    "phase_name": partial(
      validate_type, expected=str, name="phase_name", optional=True
    ),
    "unit": partial(validate_enum, expected=UNIT, name="unit", optional=True),
  }

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
    self.count_type = try_convert_to_enum(self.count_type, COUNT_TYPE)
    self.unit = try_convert_to_enum(self.unit, UNIT)
    for _, e in self._validate_attributes(gather_all_errors=True).errors:
      warn(str(e))

  @override
  def _init_content(self, **kwargs):
    if "value" in kwargs:
      self.value = kwargs["value"]
    elif self._source_element is None or self._source_element.text is None:
      self.value = None
      warn("Missing a value for attribute 'value'")
    else:
      self.value = int(self._source_element.text)

  def _to_element(self, element_factory):
    element = super()._to_element(element_factory)
    element.text = stringify(self.value)
    return element


class CountGroup(BaseXliffElement):
  _xml_tag = "count-group"
  _xml_attribute_map = {
    "name": "name",
  }
  _has_content = True
  __slots__ = ("name", "counts")
  name: str
  counts: MutableSequence[Count]

  _validators = {
    "name": partial(validate_type, expected=str, name="name", optional=False),
  }

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
    self._children = self.counts
    for _, e in self._validate_attributes(gather_all_errors=True).errors:
      warn(str(e))

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


class Context(BaseXliffElement):
  _xml_tag = "context"
  _xml_attribute_map = {
    "context_type": "context-type",
    "match_mandatory": "match-mandatory",
    "crc": "crc",
  }
  _has_content = True
  _validators = {
    "value": partial(validate_type, expected=str, name="value", optional=False),
    "context_type": partial(
      validate_enum, expected=CONTEXT_TYPE, name="count_type", optional=False
    ),
    "match_mandatory": partial(
      validate_type, expected=bool, name="match_mandatory", optional=True
    ),
    "crc": partial(validate_type, expected=str, name="unit", optional=True),
  }

  __slots__ = (
    "value",
    "context_type",
    "match_mandatory",
    "crc",
  )
  value: str
  context_type: str | CONTEXT_TYPE
  match_mandatory: Optional[bool]
  crc: Optional[str]

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
    self._children = tuple()
    self.context_type = try_convert_to_enum(self.context_type, CONTEXT_TYPE)
    self.match_mandatory = try_convert_to_boolean(self.match_mandatory)
    for _, e in self._validate_attributes(gather_all_errors=True).errors:
      warn(str(e))

  def _init_content(self, **kwargs):
    if "value" in kwargs:
      self.value = kwargs["value"]
    elif self._source_element is None or self._source_element.text is None:
      self.value = None
      warn("Missing a value for attribute 'value'")
    else:
      self.value = self._source_element.text

  def _to_element(self, element_factory):
    element = super()._to_element(element_factory)
    element.text = self.value
    return element


class ContextGroup(BaseXliffElement):
  _xml_tag = "context-group"
  _xml_attribute_map = {
    "crc": "crc",
    "name": "name",
    "purpose": "purpose",
  }
  _has_content = True
  _validators = {
    "crc": partial(validate_type, expected=str, name="unit", optional=True),
    "name": partial(validate_type, expected=str, name="value", optional=True),
    "purpose": partial(validate_enum, expected=PURPOSE, name="purpose", optional=True),
  }
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
    self._children = self.contexts
    self.purpose = try_convert_to_enum(self.purpose, PURPOSE)
    for _, e in self._validate_attributes(gather_all_errors=True).errors:
      warn(str(e))

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


class Prop(BaseXliffElement):
  _xml_tag = "prop"
  _xml_attribute_map = {"prop_type": "prop-type", "lang": f"{{{XML_NAMESPACE}}}lang"}
  _has_content = True
  _validators = {
    "prop_type": partial(validate_type, expected=str, name="prop_type", optional=False),
    "value": partial(validate_type, expected=str, name="value", optional=False),
    "lang": partial(validate_type, expected=str, name="lang", optional=True),
  }
  value: str
  prop_type: str
  lang: Optional[str]
  __slots__ = ("value", "prop_type", "lang")

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
    prop_type: Optional[str] = None,
    lang: Optional[str | PURPOSE] = None,
  ) -> None: ...
  @overload
  def __init__(
    self,
    *,
    value: str,
    prop_type: str,
    lang: Optional[str] = None,
  ) -> None: ...
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    for _, e in self._validate_attributes(gather_all_errors=True).errors:
      warn(str(e))

  def _init_content(self, **kwargs):
    if "value" in kwargs:
      self.value = kwargs["value"]
    elif self._source_element is None or self._source_element.text is None:
      self.value = None
      warn("Missing a value for attribute 'value'")
    else:
      self.value = self._source_element.text

  def _to_element(self, element_factory):
    element = super()._to_element(element_factory)
    element.text = self.value
    return element


class PropGroup(BaseXliffElement):
  _xml_tag = "prop-group"
  _xml_attribute_map = {
    "name": "name",
  }
  _has_content = True
  __slots__ = ("name", "props")
  name: str
  props: MutableSequence[Prop]

  _validators = {
    "name": partial(validate_type, expected=str, name="name", optional=False),
  }

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
    props: Optional[MutableSequence[Prop]] = None,
  ) -> None: ...
  @overload
  def __init__(self, *, name: str, props: MutableSequence[Prop]) -> None: ...
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self._children = self.props
    for _, e in self._validate_attributes(gather_all_errors=True).errors:
      warn(str(e))

  def _init_content(self, **kwargs):
    if "props" in kwargs:
      self.props = kwargs["props"]
    elif self._source_element is None or not len(self._source_element):
      self.props = []
    else:
      self.props = [Prop(source_element=prop) for prop in self._source_element]

  def _to_element(self, element_factory):
    element = super()._to_element(element_factory)
    for prop in self.props:
      element.append(prop.to_element(element_factory))
    return element
