from __future__ import annotations
from collections.abc import Callable, Iterable, Mapping
from functools import partial
from typing import ClassVar, Optional, overload
from xliff.constants import (
  __FAKE__ELEMENT__,
  ElementLike,
  Python_ElementFactory,
  ElementLikeProtocol,
)
from xliff.errors import ValidationError, ValidationErrorGroup
from xliff.helpers import (
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


class Coord:
  x: Optional[float]
  y: Optional[float]
  cx: Optional[float]
  cy: Optional[float]

  __slots__ = ("x", "y", "cx", "cy")

  def __init__(
    self,
    x: Optional[float | str] = None,
    y: Optional[float | str] = None,
    cx: Optional[float | str] = None,
    cy: Optional[float | str] = None,
  ):
    self.x = x if isinstance(x, float) else float(x) if x is not None else None
    self.y = y if isinstance(y, float) else float(y) if y is not None else None
    self.cx = cx if isinstance(cx, float) else float(cx) if cx is not None else None
    self.cy = cy if isinstance(cy, float) else float(cy) if cy is not None else None

  def __str__(self) -> str:
    return ";".join(
      getattr(self, attr) if getattr(self, attr) is not None else "#"
      for attr in (
        "x",
        "y",
        "cx",
        "cy",
      )
    )


class Font:
  name: str
  size: Optional[str]
  weight: Optional[str]
  style: Optional[str]
  encoding: Optional[str]

  __slots__ = ("name", "size", "weight", "style", "encoding")

  def __init__(
    self,
    name: str,
    size: Optional[str] = None,
    weight: Optional[str] = None,
    style: Optional[str] = None,
    encoding: Optional[str] = None,
  ):
    self.name = name
    self.size = size
    self.weight = weight
    self.style = style
    self.encoding = encoding

  def __str__(self) -> str:
    return ";".join(
      getattr(self, attr)
      for attr in ("name", "size", "weight", "style", "encoding")
      if getattr(self, attr) is not None
    )
