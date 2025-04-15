from collections.abc import MutableSequence
from typing import Any
from warnings import deprecated

from langcodes import Language
from pydantic import (
    ConfigDict,
    ValidatorFunctionWrapHandler,
    field_serializer,
    field_validator,
)
from pydantic_xml import BaseXmlModel, attr, element

from python_xliff.objects.enums import CONTEXTTYPE, COUNTTYPE, PURPOSE, UNIT
from python_xliff.utils.validators import (
    validate_enum_or_custom_str_attr_value,
    validate_language,
)


class Count(BaseXmlModel, tag="count"):
    count_type: str | COUNTTYPE = attr(name="count-type")
    phase_name: str | None = attr(name="phase-name", default=None)
    unit: str | UNIT | None = attr(name="unit", default=None)
    value: int

    @field_validator("count_type")
    @classmethod
    def validate_count_type(cls, value: str | COUNTTYPE) -> str | COUNTTYPE:
        return validate_enum_or_custom_str_attr_value(COUNTTYPE, value)

    @field_validator("unit")
    @classmethod
    def validate_unit(cls, value: str | UNIT) -> str | UNIT:
        return validate_enum_or_custom_str_attr_value(UNIT, value)


class CountGroup(BaseXmlModel, tag="count-group"):
    name: str = attr(name="name")
    counts: MutableSequence[Count] = element(tag="count", default_factory=list)


class Context(BaseXmlModel, tag="context"):
    context_type: str | CONTEXTTYPE | None = attr(name="context-type", default=None)
    match_mandatory: bool | None = attr(name="match-mandatory", default=None)
    crc: int | float | None = attr(name="crc", default=None)
    content: str

    @field_validator("context_type")
    @classmethod
    def validate_context_type(cls, value: str | CONTEXTTYPE) -> str | CONTEXTTYPE:
        return validate_enum_or_custom_str_attr_value(CONTEXTTYPE, value)


class ContextGroup(BaseXmlModel, tag="context-group"):
    crc: int | float | None = attr(name="crc", default=None)
    name: str | None = attr(name="name", default=None)
    purpose: str | PURPOSE | None = attr(name="purpose", default=None)
    contexts: MutableSequence[Context] = element(tag="context", default_factory=list)

    @field_validator("purpose")
    @classmethod
    def validate_purpose(cls, value: str | PURPOSE) -> str | PURPOSE:
        return validate_enum_or_custom_str_attr_value(PURPOSE, value)


@deprecated(
    "The <prop> element was DEPRECATED in version 1.1. Instead, use attributes defined in a namespace different from XLIFF.",
    category=None,
)
class Prop(
    BaseXmlModel, tag="prop", nsmap={"xml": "http://www.w3.org/XML/1998/namespace"}
):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    prop_type: str | None = attr(name="prop-type", default=None)
    lang: Language | None = attr(
        name="lang",
        default=None,
        ns="xml",
    )
    content: str

    @field_validator("lang", mode="wrap")
    @classmethod
    def validate_lang(
        cls, value: Any, handler: ValidatorFunctionWrapHandler
    ) -> Language:
        return validate_language(value)

    @field_serializer("lang")
    def serialize_lang(self, value: Language) -> str:
        return value.to_tag()


@deprecated(
    "The <prop-group> element was DEPRECATED in version 1.1. Instead, use attributes defined in a namespace different from XLIFF.",
    category=None,
)
class PropGroup(BaseXmlModel, tag="prop-group"):
    name: str | None = attr(name="name", default=None)
    props: MutableSequence[Prop] = element(tag="prop", default_factory=list)
