from __future__ import annotations
from collections.abc import Callable, Iterable, Mapping, MutableSequence
from functools import partial
from typing import ClassVar, Optional, overload, override
from warnings import warn
from xml.dom import XML_NAMESPACE
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
from xliff.errors import ValidationError, ValidationErrorGroup
from xliff.helpers import (
  try_convert_to_boolean,
  ensure_correct_element,
  try_convert_to_enum,
  ensure_usable_element,
  stringify,
  validate_enum,
  validate_type,
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
  ) -> ElementLike:
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
  _children: Iterable[BaseXliffElement]
  _validators: ClassVar[dict[str, partial[None]]]
  __slots__ = ("_source_element", "_children")

  def __init__(self, **kwargs) -> None:
    # Check if we have a source xml element and ensure it's correct else use a temp
    # element to not break anything
    self._children = tuple()
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
    self.validate(recurse=True)
    element_factory_ = let.Element if element_factory is None else element_factory
    element = element_factory_(self._xml_tag, self._attribute_dict)
    return element

  def _validate_attributes(
    self, *, gather_all_errors: bool = False
  ) -> ValidationErrorGroup:
    """
    Validates all attributes of the element using their registered validators.

    This method checks each attribute against its validator defined in the class's
    _validators dictionary. It either raises the first error encountered or collects
    all errors into a ValidationErrorGroup.

    Args:
      gather_all_errors (bool): If True, collects all validation errors instead of raising on the first one encountered. Defaults to False.

    Returns:
      ValidationErrorGroup: A group containing all validation errors found. Will be empty if no errors were encountered.

    Raises:
      ValidationError: If validation fails for any attribute and gather_all_errors is False.
    """
    # Initialize our error group
    validation_error_group = ValidationErrorGroup()
    for attribute, validator in self._validators.items():
      try:
        # Run each validator (subclass dependent)
        value = getattr(self, attribute)
        validator(value)
      except (ValueError, TypeError) as e:
        # Create the ValidationError with the correct info
        Error = ValidationError(
          e,
          {
            "attribute": attribute,
            "value": value,
            "expected": validator.keywords["expected"],
            "source": self,
          },
        )
        if not gather_all_errors:
          # Immediately raise if not gathering.
          # Since gather_all_errors is passed down from the original validate call
          # this error will bubble up back to it immediately
          raise Error
        # Append our error to our group and move to the next attribute to collect all errors
        validation_error_group.errors.append((self, Error))
    # Return all errors
    return validation_error_group

  def _validate_children(
    self,
    *,
    recurse: bool = True,
    gather_all_errors: bool = False,
  ) -> ValidationErrorGroup:
    """
    Validates all child elements of this element.

    This method iterates through all children in self._children and validates each one.
    Validation can be performed recursively through the entire element tree.

    Args:
      recurse (bool): If True, validates all descendants recursively. If False, only validates direct children. Defaults to True.
      gather_all_errors (bool): If True, collects all validation errors instead of raising on the first one encountered. Defaults to False.

    Returns:
      ValidationErrorGroup: A group containing all validation errors found in children. Will be empty if no errors were encountered.

    Raises:
      ValidationError: If validation fails for any child and gather_all_errors is False.
      ValidationErrorGroup: If validation fails for multiple children and gather_all_errors is True.
    """
    # Initialize the error group
    validation_error_group = ValidationErrorGroup()
    for child in self._children:
      try:
        # Validate each child, passing down recurse and gather_all_error for consistent behavior
        child.validate(recurse=recurse, gather_all_errors=gather_all_errors)
      except ValidationError as e:
        # Raise directly if not a group since we're not gathering
        raise e
      except ValidationErrorGroup as e:
        # Extend our group with all the errors of that child
        validation_error_group.errors.extend(e.errors)
    # Return all the errors
    return validation_error_group

  def validate(self, *, recurse=True, gather_all_errors=False) -> None:
    """
    Validates this element and optionally its children.

    This method performs comprehensive validation on the element, checking that:
    1. All required attributes are present and have valid values
    2. If recurse=True, all child elements are also valid

    Following the "lax input, strict output" philosophy, this validation is primarily
    meant to be called before serialization to ensure only valid data is exported.

    Args:
      recurse (bool): If True, validates all descendants recursively. If False, only validates this element. Defaults to True.
      gather_all_errors (bool): If True, collects and raises all validation errors together. If False, raises on the first error encountered. Defaults to False.

    Raises:
      ValidationError: If validation fails for a single attribute or child and gather_all_errors is False.
      ValidationErrorGroup: If validation fails for multiple attributes or children and gather_all_errors is True.
    """
    # Initialize our error group
    all_errors = ValidationErrorGroup()
    # Validate attributes
    # If not gathering errors, this will simply raise a ValidationError
    # Else, we collect all the attribute errors
    all_errors.errors.extend(
      self._validate_attributes(gather_all_errors=gather_all_errors).errors
    )
    # Check all children if needed
    if recurse:
      # Validate children
      # If not gathering error, this will let the first ValidationError bubble up
      # Else, we'll simply extend our error list with all of the errors in the children
      all_errors.errors.extend(
        self._validate_children(
          recurse=recurse, gather_all_errors=gather_all_errors
        ).errors
      )
    # Raise if we have errors
    if len(all_errors.errors):
      raise all_errors
    return None


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
