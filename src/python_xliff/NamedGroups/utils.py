from lxml.etree import _Element

from python_xliff.Extras import CONTEXT_TYPE, COUNT_TYPE, PURPOSE, UNIT
from python_xliff.NamedGroups import (
    Context,
    ContextGroup,
    Count,
    CountGroup,
    Prop,
    PropGroup,
)
from python_xliff.utils import _try_convert_to_bool, _try_convert_to_enum

__xml__ = "{http://www.w3.org/XML/1998/namespace}"


def _parse_count(element: _Element) -> Count:
    if not element.tag == "count":
        raise ValueError(f"Expected a count element, got {element.tag!r}")
    if not element.text:
        raise ValueError("Missing value for count")
    count_ = int(element.text)
    if (count_type_attr := element.get("count-type")) is not None:
        count_type = _try_convert_to_enum(count_type_attr, COUNT_TYPE)
    if (unit_attr := element.get("unit")) is not None:
        unit_ = _try_convert_to_enum(unit_attr, UNIT)
    phase_name = element.get("phase-name")
    return Count(count=count_, count_type=count_type, unit=unit_, phase_name=phase_name)


def _parse_count_group(element: _Element) -> CountGroup:
    if not element.tag == "count-group":
        raise ValueError(f"Expected a count-group element, got {element.tag!r}")
    name = element.get("name")
    if not name:
        raise ValueError("Missing name attribute")
    counts = [_parse_count(c) for c in element.iter("count")]
    return CountGroup(name=name, counts=counts)


def _parse_context(element: _Element) -> Context:
    if not element.tag == "context":
        raise ValueError(f"Expected a context element, got {element.tag!r}")
    if element.text is None:
        raise ValueError("Context element must have a text value")
    if (context_type_attr := element.get("context-type")) is not None:
        context_type_ = _try_convert_to_enum(context_type_attr, CONTEXT_TYPE)
    else:
        raise ValueError("Missing context-type attribute")
    if (match_mandatory_attr := element.get("match-mandatory")) is not None:
        match_mandatory_ = _try_convert_to_bool(match_mandatory_attr)
    else:
        match_mandatory_ = None
    if (crc_attr := element.get("crc")) is not None:
        try:
            crc_ = float(crc_attr)
        except (ValueError, TypeError):
            crc_ = None
    else:
        crc_ = None
    return Context(
        content=element.text,
        context_type=context_type_,
        match_mandatory=match_mandatory_,
        crc=crc_,
    )


def _parse_context_group(element: _Element) -> ContextGroup:
    if not element.tag == "context-group":
        raise ValueError(f"Expected a context-group element, got {element.tag!r}")
    name = element.get("name")
    if (crc_attr := element.get("crc")) is not None:
        try:
            crc_ = float(crc_attr)
        except (ValueError, TypeError):
            crc_ = None
    else:
        crc_ = None
    if (purpose_attr := element.get("purpose")) is not None:
        purpose_ = _try_convert_to_enum(purpose_attr, PURPOSE)
    else:
        purpose_ = None
    contexts_ = [_parse_context(c) for c in element.iter("context")]
    return ContextGroup(name=name, purpose=purpose_, crc=crc_, contexts=contexts_)


def _parse_prop(element: _Element) -> Prop:
    if not element.tag == "prop":
        raise ValueError(f"Expected a prop element, got {element.tag!r}")
    if not element.text:
        raise ValueError("Prop element must have a text value")
    if (prop_type_attr := element.get("prop-type")) is not None:
        prop_type_ = prop_type_attr
    else:
        raise ValueError("Missing prop-type attribute")
    if (lang_attr := element.get(f"{__xml__}lang")) is not None:
        lang_ = lang_attr
    else:
        lang_ = None
    return Prop(prop_type=prop_type_, lang=lang_, content=element.text)


def _parse_prop_group(element: _Element) -> PropGroup:
    if not element.tag == "prop-group":
        raise ValueError(f"Expected a prop-group element, got {element.tag!r}")
    name = element.get("name")
    props = [_parse_prop(c) for c in element.iter("prop")]
    return PropGroup(name=name, props=props)
