from collections.abc import MutableSequence

from pydantic import ConfigDict, ValidatorFunctionWrapHandler, field_validator
from pydantic_xml import BaseXmlModel, attr, element

from python_xliff.objects.enums import DATACLASS, RESTYPE, SIZEUNIT, Coord, Font
from python_xliff.objects.named_groups import ContextGroup, CountGroup, PropGroup
from python_xliff.utils.validators import validate_enum_or_custom_str_attr_value


class Group(
    BaseXmlModel, tag="group", nsmap={"xml": "http://www.w3.org/XML/1998/namespace"}
):
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
    id: str | None = attr(name="id", default=None)
    datatype: str | DATACLASS | None = attr(name="datatype", default=None)
    space: str | None = attr(name="space", default=None, ns="xml")
    restype: str | RESTYPE | None = attr(name="restype", default=None)
    resname: str | None = attr(name="resname", default=None)
    extradata: str | None = attr(name="extradata", default=None)
    help_id: str | None = attr(name="help-id", default=None)
    menu: str | None = attr(name="menu", default=None)
    menu_option: str | None = attr(name="menu-option", default=None)
    menu_name: str | None = attr(name="menu-name", default=None)
    coord: Coord | None = attr(name="coord", default=None)
    font: Font | None = attr(name="font", default=None)
    css_style: str | None = attr(name="css-style", default=None)
    exstyle: str | None = attr(name="exstyle", default=None)
    extype: str | None = attr(name="exstyle", default=None)
    translate: bool | None = attr(name="translate", default=None)
    reformat: bool | str | None = attr(name="reformat", default=None)
    maxbytes: int | None = attr(name="maxbytes", default=None)
    minbytes: int | None = attr(name="minbytes", default=None)
    size_unit: str | SIZEUNIT | None = attr(name="size-unit", default=None)
    maxheight: int | None = attr(name="maxheight", default=None)
    minheight: int | None = attr(name="minheight", default=None)
    maxwidth: int | None = attr(name="maxwidth", default=None)
    minwidth: int | None = attr(name="minwidth", default=None)
    charclass: str | None = attr(name="charclass", default=None)
    merged_trans: bool | None = attr(name="merged-trans", default=None)

    context_groups: MutableSequence[ContextGroup] = element(
        "context-group", default_factory=list
    )
    count_groups: MutableSequence[CountGroup] = element(
        "count-group", default_factory=list
    )
    prop_groups: MutableSequence[PropGroup] = element(
        "prop-group", default_factory=list
    )
    notes: MutableSequence["Note"] = element("note", default_factory=list)
    groups: MutableSequence["Group"] = element("group", default_factory=list)
    trans_units: MutableSequence["TransUnit"] = element(
        "trans-unit", default_factory=list
    )
    bin_units: MutableSequence["BinUnit"] = element("bin-unit", default_factory=list)

    @field_validator("dataclass")
    @classmethod
    def validate_dataclass(cls, value: str | DATACLASS) -> str | DATACLASS:
        return validate_enum_or_custom_str_attr_value(DATACLASS, value)

    @field_validator("restype")
    @classmethod
    def validate_restype(cls, value: str | RESTYPE) -> str | RESTYPE:
        return validate_enum_or_custom_str_attr_value(RESTYPE, value)

    @field_validator("coord", mode="wrap")
    @classmethod
    def validate_coord(
        cls, value: str | None, handler: ValidatorFunctionWrapHandler
    ) -> Coord | None:
        if value is None:
            return value
        if not isinstance(value, str):
            raise TypeError(
                f"value must be a string or None but got {value.__class__.__name__}"
            )
        return Coord(*(int(i) if i != "#" else None for i in value.split(";")))

    @field_validator("font", mode="wrap")
    @classmethod
    def validate_font(
        cls, value: str | None, handler: ValidatorFunctionWrapHandler
    ) -> Font | None:
        if value is None:
            return value
        if not isinstance(value, str):
            raise TypeError(
                f"value must be a string or None but got {value.__class__.__name__}"
            )
        return Font(*(i for i in value.split(";")))

    @field_validator("size_unit")
    @classmethod
    def validate_size_unit(cls, value: str | SIZEUNIT) -> str | SIZEUNIT:
        return validate_enum_or_custom_str_attr_value(SIZEUNIT, value)
