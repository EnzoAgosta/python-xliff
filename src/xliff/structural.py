from __future__ import annotations
from collections.abc import MutableSequence
from functools import partial
from typing import Optional, Self
from xml.dom import XML_NAMESPACE
from xliff.constants import DATATYPE, REFORMAT, RESTYPE, SIZE_UNIT
from xliff.helpers import validate_enum, validate_type
from xliff.named_groups import ContextGroup, CountGroup, PropGroup
from xliff.objects import BaseXliffElement, Coord, Font


class Group(BaseXliffElement):
  _xml_tag = "group"
  _has_content = True
  _xml_attribute_map = {
    "id": "id",
    "datatype": "datatype",
    "space": f"{{{XML_NAMESPACE}}}space",
    "ts": "ts",
    "restype": "restype",
    "resname": "resname",
    "extradata": "extradata",
    "help_id": "help-id",
    "menu": "menu",
    "menu_option": "menu-option ",
    "menu_name": "menu-name",
    "coord": "coord",
    "font": "font",
    "css_style": "css-style",
    "style": "style",
    "exstyle": "exstyle",
    "extype": "extype",
    "translate": "translate",
    "reformat": "reformat ",
    "maxbytes": "maxbytes",
    "minbytes": "minbytes",
    "size_unit": "size-unit",
    "maxheight": "maxheight",
    "minheight": "minheight",
    "maxwidth ": "maxwidth ",
    "minwidth": "minwidth",
    "charclass": "charclass",
    "merged_trans": "merged-trans",
  }
  id: Optional[str]
  datatype: Optional[DATATYPE | str]
  space: Optional[str]
  ts: Optional[str]
  restype: Optional[RESTYPE | str]
  resname: Optional[str]
  extradata: Optional[str]
  help_id: Optional[str]
  menu: Optional[str]
  menu_option: Optional[str]
  menu_name: Optional[str]
  coord: Optional[Coord]
  font: Optional[Font]
  css_style: Optional[str]
  style: Optional[str]
  exstyle: Optional[str]
  extype: Optional[str]
  translate: Optional[bool]
  reformat: Optional[bool | MutableSequence[str | REFORMAT]]
  maxbytes: Optional[int]
  minbytes: Optional[int]
  size_unit: Optional[SIZE_UNIT | str]
  maxheight: Optional[int]
  minheight: Optional[int]
  maxwidth: Optional[int]
  minwidth: Optional[int]
  charclass: Optional[str]
  merged_trans: Optional[bool]
  context_groups: MutableSequence[ContextGroup]
  count_groups: MutableSequence[CountGroup]
  prop_groups: MutableSequence[PropGroup]
  notes: MutableSequence[str]
  groups: MutableSequence[Self]
  trans_units: MutableSequence[str]
  bin_units: MutableSequence[str]

  __slots__ = (
    "id",
    "datatype",
    "space",
    "ts",
    "restype",
    "resname",
    "extradata",
    "help_id",
    "menu",
    "menu_option",
    "menu_name",
    "coord",
    "font",
    "css_style",
    "style",
    "exstyle",
    "extype",
    "translate",
    "reformat",
    "maxbytes",
    "minbytes",
    "size_unit",
    "maxheight",
    "minheight",
    "maxwidth",
    "minwidth",
    "charclass",
    "merged_trans",
  )

  _validators = {
    "id": partial(validate_type, expected=str, name="id", optional=True),
    "datatype": partial(validate_enum, expected=DATATYPE, name="datatype", optional=True),
    "space": partial(validate_type, expected=str, name="space", optional=True),
    "ts": partial(validate_type, expected=str, name="ts", optional=True),
    "restype": partial(validate_enum, expected=RESTYPE, name="restype", optional=True),
    "resname": partial(validate_type, expected=str, name="resname", optional=True),
    "extradata": partial(validate_type, expected=str, name="extradata", optional=True),
    "help_id": partial(validate_type, expected=str, name="help_id", optional=True),
    "menu": partial(validate_type, expected=str, name="menu", optional=True),
    "menu_option": partial(
      validate_type, expected=str, name="menu_option", optional=True
    ),
    "menu_name": partial(validate_type, expected=str, name="menu_name", optional=True),
    "coord": partial(validate_type, expected=Coord, name="coord", optional=True),
    "font": partial(validate_type, expected=Font, name="font", optional=True),
    "css_style": partial(validate_type, expected=str, name="css_style", optional=True),
    "style": partial(validate_type, expected=str, name="style", optional=True),
    "exstyle": partial(validate_type, expected=str, name="exstyle", optional=True),
    "extype": partial(validate_type, expected=str, name="extype", optional=True),
    "translate": partial(validate_type, expected=bool, name="translate", optional=True),
    "reformat": partial(validate_type, expected=str, name="reformat", optional=True),
    "maxbytes": partial(validate_type, expected=int, name="maxbytes", optional=True),
    "minbytes": partial(validate_type, expected=int, name="minbytes", optional=True),
    "size_unit": partial(validate_enum, expected=SIZE_UNIT, name="size_unit", optional=True),
    "maxheight": partial(validate_type, expected=int, name="maxheight", optional=True),
    "minheight": partial(validate_type, expected=int, name="minheight", optional=True),
    "maxwidth": partial(validate_type, expected=int, name="maxwidth", optional=True),
    "minwidth": partial(validate_type, expected=int, name="minwidth", optional=True),
    "charclass": partial(validate_type, expected=str, name="charclass", optional=True),
    "merged_trans": partial(
      validate_type, expected=bool, name="merged_trans", optional=True
    ),
  }
