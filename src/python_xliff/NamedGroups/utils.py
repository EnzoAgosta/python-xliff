from lxml.etree import Element, _Element

from python_xliff.Extras import CONTEXT_TYPE, COUNT_TYPE, PURPOSE, UNIT
from python_xliff.NamedGroups import (
    Context,
    ContextGroup,
    Count,
    CountGroup,
    Prop,
    PropGroup,
)
from python_xliff.utils import (
    _coerce_str_to_bool,
    _coerce_str_to_enum,
    _export_bool,
    _export_enum,
)

__xml__ = "{http://www.w3.org/XML/1998/namespace}"


def parse_count(element: _Element) -> Count:
    if not element.tag == "count":
        raise ValueError(f"Expected a count element, got {element.tag!r}")
    if element.text is None:
        raise ValueError("Missing value for count")
    count_ = int(element.text)
    count_type = _coerce_str_to_enum(element.attrib.get("count_type"), COUNT_TYPE, True)
    unit = _coerce_str_to_enum(element.attrib.get("unit"), UNIT, False)
    phase_name = element.attrib.get("phase-name")
    return Count(count=count_, count_type=count_type, unit=unit, phase_name=phase_name)


def export_count(count: Count) -> _Element:
    if not isinstance(count, Count):
        raise TypeError(f"Expected a COunt object but got {type(count)}")
    elem = Element("count")
    if not isinstance(count.count, int):
        raise TypeError(f"Expected an int but got {type(count.count)}")
    elem.text = str(count.count)
    elem.attrib["count-type"] = _export_enum(count.count_type, COUNT_TYPE)
    elem.attrib["unit"] = _export_enum(count.count_type, UNIT)
    if count.phase_name is not None:
        if isinstance(count.phase_name, str):
            elem.attrib["phase-name"] = count.phase_name
        else:
            raise TypeError(f"Expected a string but got {type(count.phase_name)}")
    return elem


def parse_count_group(element: _Element) -> CountGroup:
    if not element.tag == "count-group":
        raise ValueError(f"Expected a count-group element, got {element.tag!r}")
    name = element.attrib["name"]
    counts = [parse_count(c) for c in element.iter("count")]
    return CountGroup(
        name=name,
        counts=counts,
    )


def export_count_group(count_group: CountGroup) -> _Element:
    if not isinstance(count_group, CountGroup):
        raise TypeError(f"Expected a CountGroup object but got {type(count_group)}")
    elem = Element("count-group")
    if not isinstance(count_group.name, str):
        raise TypeError(f"Expected a string but got {type(count_group.name)}")
    elem.attrib["name"] = count_group.name
    elem.extend([export_count(c) for c in count_group.counts])
    return elem


def parse_context(element: _Element) -> Context:
    if not element.tag == "context":
        raise ValueError(f"Expected a context element, got {element.tag!r}")
    if element.text is None:
        raise ValueError("Context element must have a text value")
    context_type = _coerce_str_to_enum(
        element.attrib.get("context-type"), CONTEXT_TYPE, True
    )
    match_mandatory = _coerce_str_to_bool(element.attrib.get("match-mandatory"), False)
    crc = element.get("crc")
    return Context(
        content=element.text,
        context_type=context_type,
        match_mandatory=match_mandatory,
        crc=crc,
    )


def export_context(context: Context) -> _Element:
    if not isinstance(context, Context):
        raise TypeError(f"Expected a Context object but got {type(context)}")
    elem = Element("context")
    if not isinstance(context.content, str):
        raise TypeError(f"Expected a string but got {type(context.content)}")
    elem.text = context.content
    elem.attrib["context-type"] = _export_enum(context.context_type, CONTEXT_TYPE)
    if context.match_mandatory is not None:
        elem.attrib["match-mandatory"] = _export_bool(context.match_mandatory)
    if context.crc is not None:
        if not isinstance(context.crc, str):
            raise TypeError(f"Expected a string but got {type(context.crc)}")
        elem.attrib["crc"] = context.crc
    return elem


def parse_context_group(element: _Element) -> ContextGroup:
    if not element.tag == "context-group":
        raise ValueError(f"Expected a context-group element, got {element.tag!r}")
    crc = element.get("crc")
    purpose = _coerce_str_to_enum(element.get("purpose"), PURPOSE, False)
    contexts = [parse_context(c) for c in element.iter("context")]
    name = element.attrib["name"]
    return ContextGroup(name=name, purpose=purpose, crc=crc, contexts=contexts)


def export_context_group(context_group: ContextGroup) -> _Element:
    if not isinstance(context_group, ContextGroup):
        raise TypeError(f"Expected a ContextGroup object but got {type(context_group)}")
    elem = Element("context-group")
    if context_group.crc is not None:
        if not isinstance(context_group.crc, str):
            raise TypeError(f"Expected a string but got {type(context_group.crc)}")
        elem.attrib["crc"] = context_group.crc
    if context_group.name is not None:
        if not isinstance(context_group.name, str):
            raise TypeError(f"Expected a string but got {type(context_group.name)}")
        elem.attrib["name"] = context_group.name
    if context_group.purpose is not None:
        elem.attrib["purpose"] = _export_enum(context_group.purpose, PURPOSE)
    elem.extend([export_context(c) for c in context_group.contexts])
    return elem


def parse_prop(element: _Element) -> Prop:
    if not element.tag == "prop":
        raise ValueError(f"Expected a prop element, got {element.tag!r}")
    if not element.text:
        raise ValueError("Prop element must have a text value")
    prop_type = element.attrib["prop-type"]
    lang = element.get(f"{__xml__}lang")
    return Prop(prop_type=prop_type, lang=lang, content=element.text)


def export_prop(prop: Prop) -> _Element:
    if not isinstance(prop, Prop):
        raise TypeError(f"Expected a Prop object but got {type(prop)}")
    elem = Element("prop")
    if not isinstance(prop.prop_type, str):
        raise TypeError(f"Expected a string but got {type(prop.prop_type)}")
    elem.attrib["prop-type"] = prop.prop_type
    if prop.lang is not None:
        if not isinstance(prop.lang, str):
            raise TypeError(f"Expected a string but got {type(prop.lang)}")
        elem.attrib[f"{__xml__}lang"] = prop.lang
    elem.text = prop.content
    return elem


def parse_prop_group(element: _Element) -> PropGroup:
    if not element.tag == "prop-group":
        raise ValueError(f"Expected a prop-group element, got {element.tag!r}")
    name = element.get("name")
    props = [parse_prop(c) for c in element.iter("prop")]
    return PropGroup(name=name, props=props)


def export_prop_group(prop_group: PropGroup) -> _Element:
    if not isinstance(prop_group, PropGroup):
        raise TypeError(f"Expected a PropGroup object but got {type(prop_group)}")
    elem = Element("prop-group")
    if prop_group.name is not None:
        if not isinstance(prop_group.name, str):
            raise TypeError(f"Expected a string but got {type(prop_group.name)}")
        elem.attrib["name"] = prop_group.name
    elem.extend([export_prop(p) for p in prop_group.props])
    return elem
