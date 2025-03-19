from __future__ import annotations

from collections.abc import MutableSequence
from dataclasses import dataclass, field

from typing_extensions import deprecated

from python_xliff.Extras import CONTEXT_TYPE, COUNT_TYPE, PURPOSE, UNIT

__all__ = ["CountGroup", "Count", "ContextGroup", "Context", "PropGroup", "Prop"]


@dataclass(slots=True, kw_only=True)
class CountGroup:
    """
    *Count group* – Holds :class:`Count` elements relating to the level in the
    tree in which it occurs.
    """

    name: str
    """
    *Name* – Specifies the user-defined name of the element.
    
    .. note::
        used for identification purposes only and is not referenced with the file,
        unless by a processing instruction.
    """
    counts: MutableSequence[Count] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class Count:
    """
    *Count* – Contains information about counts.
    """

    count: int
    count_type: COUNT_TYPE | str
    """
    *Count type* – Specifies the purpose of the :class:`Count` element.
    """
    phase_name: str | None = field(default=None)
    """
    *Phase Name* – Used to refer to the given class:`Phase` element.
    """
    unit: UNIT | str | None = field(default=None)
    """
    *Unit* – Specifies the units counted in a :class:`Count` element.
    """


@dataclass(slots=True, kw_only=True)
class ContextGroup:
    """
    *Context group* – Holds context elements relating to the level in the tree
    in which it occurs.
    """

    contexts: MutableSequence[Context] = field(default_factory=list)
    crc: str | None = field(default=None)
    """
    *Cyclic redundancy checking* – Used to verify data as it is returned to the
    producer. The generation and verification of this number is tool-specific.
    """
    name: str | None = field(default=None)
    """
    *Name* – Specifies the user-defined name of the element.
    
    .. note::
        used for identification purposes only and is not referenced with the file,
        unless by a processing instruction.
    """
    purpose: PURPOSE | str | None = field(default=None)
    """
    *Purpose* – Specifies the purpose of a :class:`ContextGroup` element.
    """


@dataclass(slots=True, kw_only=True)
class Context:
    """
    *Context* – Describes the context of a
    :class:`python_xliff.Objects.Structural.Source` within a
    :class:`python_xliff.Objects.Structural.TransUnit` or a
    :class:`python_xliff.Objects.Structural.AltTrans`.
    """

    content: str
    context_type: CONTEXT_TYPE | str
    """
    *Context type* – Specifies the context and the type of resource or style of
    the data.
    """
    match_mandatory: bool | None = field(default=None)
    """
    *Match mandatory* – Indicates that any
    :class:`python_xliff.Objects.Structural.AltTrans` element of the parent
    :class:`python_xliff.Objects.Structural.TransUnit` must have the same
    :class:`Context` as the :class:`python_xliff.Objects.Structural.TransUnit`.
    """
    crc: str | None = field(default=None)
    """
    *Cyclic redundancy checking* – Used to verify data as it is returned to the
    producer. The generation and verification of this number is tool-specific.
    """


@deprecated("DEPRECATED in version 1.1")
@dataclass(slots=True, kw_only=True)
class PropGroup:
    """ "
    *Property group* – Contains :class:`Prop` elements.

    .. warning::
      Important: The :class:`PropGroup` element was DEPRECATED in version 1.1.
      Instead, use attributes defined in a namespace different from XLIFF.
      See the Extensibility section of the official Spec for more information."""

    props: MutableSequence[Prop]
    name: str | None = field(default=None)
    """
    *Name* – Specifies the user-defined name of the element.
    
    .. note::
        used for identification purposes only and is not referenced with the file,
        unless by a processing instruction.
    """


@deprecated("DEPRECATED in version 1.1")
@dataclass(slots=True, kw_only=True)
class Prop:
    """
    *Property* – Allows the tools to specify non-standard information in the
    XLIFF document.

    .. warning::
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """

    prop_type: str
    """
    *Property type* – Specifies the type of a :class:`Prop` element.
    
    ..warning::
        Because the :class:`Prop` element was DEPRECATED in version
        1.1 and this attribute is only a member of that element, this attribute
        is also deprecated. Instead, use attributes defined in a namespace
        different from XLIFF.
    """
    content: str
    lang: str | None = field(default=None)
    """
    *Language* – Specifies the language variant of the text of a given element.
    """
