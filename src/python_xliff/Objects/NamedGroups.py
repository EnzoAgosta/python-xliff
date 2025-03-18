from __future__ import annotations

from collections.abc import MutableSequence
from dataclasses import dataclass, field
from warnings import deprecated

from python_xliff.Objects.extras import CONTEXT_TYPE, PURPOSE, UNIT, CountType


@dataclass(slots=True, kw_only=True)
class CountGroup:
    """
    *Count group* - The <count-group> element holds count elements relating to
    the level in the tree in which it occurs.

    Each group for :class:`Count` elements must be named, allowing different
    uses for each group. The required :attr:`name` attribute uniquely identifies
    the :class:`CountGroup` for reference within the :class:`File` element.
    """

    name: str
    """
    Name - The name attribute specifies the user-defined name of a named group
    element. This is used for identification purposes only and is not referenced
    with the file, unless by a processing instruction.
    """
    counts: MutableSequence[Count]


@dataclass(slots=True, kw_only=True)
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

    value: int
    count_type: CountType | str
    """
    *Count type* - The count-type attribute specifies the purpose of the
    :class:`Count` element. For example: count-type="total" for the total count
    of words in the current scope.
    """
    phase_name: str | None = field(default=None)
    """
    *Phase Name* - The phase-name attribute provides a unique name for a
    :class:`Phase` element. It is used in other elements in the file to refer to
    the given :class:`Phase` element.
    """
    unit: UNIT | str | None = field(default=None)
    """
    *Unit* - The unit attribute specifies the units counted in a :class:`Count`
    element.
    """


@dataclass(slots=True, kw_only=True)
class ContextGroup:
    """
    *Context group* - The :class:`ContextGroup` element holds context elements
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

    contexts: MutableSequence[Context] = field(default_factory=list)
    crc: float | None = field(default=None)
    """
    *Cyclic redundancy checking* - A private value used to verify data as it is
    returned to the producer. The generation and verification of this number is
    tool-specific.
    """
    name: str | None = field(default=None)
    """
    Name - The name attribute specifies the user-defined name of a named group
    element. This is used for identification purposes only and is not referenced
    with the file, unless by a processing instruction.
    """
    purpose: PURPOSE | str | None = field(default=None)
    """
    *Purpose* - The purpose attribute specifies the purpose of a
    :class:`ContextGroup` element. For example: purpose="information"
    indicates the content is informational only and not used for specific
    processing.
    """


@dataclass(slots=True, kw_only=True)
class Context:
    """
    *Context* - The <context> element describes the context of a :class:`Source` within
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
    of the :class:`Source` elements within the scope of this context must have the same
    context. The optional :attr:`crc` attribute allows a verification of the data.
    """

    content: str
    context_type: CONTEXT_TYPE | str
    """
    *Context type* - The context-type attribute specifies the context and the
    type of resource or style of the data of a given element.
    For example, to define if it is a label, or a menu item in the case of
    resource-type data, or the style in the case of document-related data.
    """
    match_mandatory: bool | None = field(default=None)
    """
    *Match mandatory* - Indicates that any :class:`AltTrans` element of the
    parent :class:`TransUnit` must have the same :class:`Context` as the
    :class:`TransUnit`.
    """
    crc: float | None = field(default=None)
    """
    *Cyclic redundancy checking* - A private value used to verify data as it is
    returned to the producer. The generation and verification of this number is
    tool-specific.
    """


@deprecated("DEPRECATED in version 1.1")
@dataclass(slots=True, kw_only=True)
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

    props: MutableSequence[Prop]
    name: str | None = field(default=None)
    """
    Name - The name attribute specifies the user-defined name of a named group
    element. This is used for identification purposes only and is not referenced
    with the file, unless by a processing instruction.
    """


@deprecated("DEPRECATED in version 1.1")
@dataclass(slots=True, kw_only=True)
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

    prop_type: str
    """
    *Property type* - The prop-type attribute specifies the type of a
    :class:`Prop` element.
    
    ..warning::
        Important: Because the :class:`Prop` element was DEPRECATED in version
        1.1 and this attribute is only a member of that element, this attribute
        is also deprecated. Instead, use attributes defined in a namespace
        different from XLIFF. See the Extensibility section for more information.
    """
    content: str
    lang: str | None = field(default=None)
    """
    *Language* - The xml:lang attribute specifies the language variant of the
    text of a given element. For example: xml:lang="fr-FR" indicates the French
    language as spoken in France.
    """
