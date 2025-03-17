from __future__ import annotations

from collections.abc import MutableSequence
from dataclasses import dataclass, field
from warnings import deprecated


@dataclass
class CountGroup:
    """
    *Count group* - The <count-group> element holds count elements relating to
    the level in the tree in which it occurs.

    Each group for :class:`Count` elements must be named, allowing different
    uses for each group. The required :attr:`name` attribute uniquely identifies
    the :class:`CountGroup` for reference within the :class:`File` element.
    """

    # Required Attributes
    name: str
    # Content
    counts: MutableSequence[Count]


@dataclass
class Count:
    """
    *Count* - The <count> element contains information about counts.

    For each :class:`Count` element the required :attr:`count_type` attribute
    indicates what kind of count the element represents, and the optional
    :attr:`unit` attribute indicates the unit of the count (by default: word).
    A list of values for :attr:`count_type` and unit is provided. The optional
    :attr:`phase_name` attribute references the :class:`Phase` in which the count
    was produced.
    """

    # Required Attributes
    count_type: str
    # Optional Attributes
    phase_name: str | None = field(default=None)
    unit: str | None = field(default=None)
    # Content
    value: int


@dataclass
class ContextGroup:
    """
    *Context group* - The <context-group> element holds context elements
    relating to the level in the tree in which it occurs. Thus context can be
    set at a :class:`Group` level, a :class:`TransUnit` level, or a
    :class:`AltTrans` level.

    Each :class:`ContextGroup` element may be named, allowing different uses
    for each group. When the :class:`ContextGroup` is named, these uses can be
    controlled through the use of XML processing instructions.
    Because the :class:`ContextGroup` element may occur at a very high level,
    a default context can be established for all :class:`TransUnit` elements
    within a file. This default can be overridden at many subsequent levels.

    The optional :attr:`name` attribute may uniquely identify the
    :class:`ContextGroup` within the :class:`File` element.
    The optional :attr:`crc` attribute allows a verification of the data.
    The optional :attr:`purpose`purpose attribute indicates to what use this
    context information is used; e.g. "match" indicates the context information
    is for memory lookups.
    """

    # Optional Attributes
    crc: str | None = field(default=None)
    name: str | None = field(default=None)
    purpose: str | None = field(default=None)
    # Content
    contexts: MutableSequence[Context]


@dataclass
class Context:
    """
    *Context* - The <context> element describes the context of a <source> within
    a :class:`TransUnit` or a :class:`AltTrans`. The purpose of this context
    information is to allow certain pieces of text to have different translations
    depending on where they came from. The translation of a piece of text may
    differ if it is a web form or a dialog or an Oracle form or a Lotus form for
    example. This information is thus required by a translator when working on
    the file. Likewise, the information may be used by any tool proposing to
    automatically leverage the text successfully.

    The required :attr:`context_type` attribute indicates what the context
    information is; e.g. "recordtitle" indicates the name of a record in a database.
    The optional :attr:`match_mandatory` attribute indicates that translations
    of the <source> elements within the scope of this context must have the same
    context. The optional :attr:`crc` attribute allows a verification of the data.
    """

    # Required Attributes
    context_type: str
    # Optional Attributes
    match_mandatory: str | None = field(default=None)
    crc: str | None = field(default=None)
    # Content
    content: str


@deprecated("DEPRECATED in version 1.1")
@dataclass
class PropGroup:
    """ "
    *Property group* - The <prop-group> element contains :class:`Prop` elements.
    Each :class:`PropGroup` element may be named, allowing different uses for
    each group. These uses can be controlled through the use of XML processing
    instructions.

    .. warning::
      Important: The :class:`PropGroup` element was DEPRECATED in version 1.1.
      Instead, use attributes defined in a namespace different from XLIFF.
      See the Extensibility section of the official Spec for more information."""

    # Optional Attributes
    name: str | None = field(default=None)
    # Content
    props: MutableSequence[Prop]


@deprecated("DEPRECATED in version 1.1")
@dataclass
class Prop:
    """
    *Property* - The :class:`Prop` element allows the tools to specify
    non-standard information in the XLIFF document. This information can be used
    by the tools that have produced the file or that translate the file or that
    do any other amount of processing specific to the producer.

    .. warning::
      Important: The :class:`Prop` element was DEPRECATED in version 1.1.
      Instead, use attributes defined in a namespace different from XLIFF.
      See the Extensibility section of the official Spec for more information."""

    # Required Attributes
    prop_type: str
    # Optional Attributes
    lang: str | None = field(default=None)
    # Content
    content: str
