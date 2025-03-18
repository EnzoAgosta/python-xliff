from __future__ import annotations

from collections.abc import MutableSequence
from dataclasses import dataclass, field
from typing import Self

from python_xliff.Objects.extras import (
    ASSOC,
    CTYPE,
    DATATYPE,
    MTYPE,
    POS,
    X_PH_CTYPE,
)


@dataclass(slots=True, kw_only=True)
class G:
    """
    *Generic group placeholder* - Used to replace any inline code of the original
    document that has a beginning and an end, does not overlap other paired
    inline codes, and can be moved within its parent structural element.
    """

    id: str
    """
    *Identifier* - Used as a reference to the original corresponding code data
    or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document.
    It may or may not be a resource identifier.
    The identifier of a resource should, at least, be stored in the
    resname attribute.
    """
    ctype: CTYPE | str | None = field(default=None)
    """
    *Content type* - Specifies the type of code that is represented by the
    inline element.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    clone: bool | None = field(default=None)
    """
    *Clone* - Indicates that a copy of the given inline element can be made and
    placed multiple times in the :class:`python_xliff.Objects.Structural.Target`.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - Used to link an inline element to a different
    :class:`python_xliff.Objects.Structural.TransUnit` or
    :class:`python_xliff.Objects.Structural.BinUnit` element.
    """
    equiv_text: str | None = field(default=None)
    """
    *equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag.
    """
    content: MutableSequence[str | Self | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = (
        field(default_factory=list)
    )


@dataclass(slots=True, kw_only=True)
class X:
    """
    *Generic placeholder* - Used to replace any code of the original document.
    """

    id: str
    """
    *Identifier* - Used as a reference to the original corresponding code data
    or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document.
    It may or may not be a resource identifier.
    The identifier of a resource should, at least, be stored in the
    resname attribute.
    """
    ctype: X_PH_CTYPE | str | None = field(default=None)
    """
    *Content type* - Specifies the type of code that is represented by the
    inline element
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    clone: bool | None = field(default=None)
    """
    *Clone* - Indicates that a copy of the given inline element can be made and
    placed multiple times in the :class:`python_xliff.Objects.Structural.Target`.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - Used to link an inline element to a different
    :class:`python_xliff.Objects.Structural.TransUnit` or
    :class:`python_xliff.Objects.Structural.BinUnit` element.
    """
    equiv_text: str | None = field(default=None)
    """
    *equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag.
    """


@dataclass(slots=True, kw_only=True)
class Bx:
    """
    *Begin paired placeholder* - Used to replace a beginning paired code of the
    original document.
    It should be used for paired codes that do not follow XML well-formedness
    rules (i.e. no overlapping elements).
    If the paired codes follow that rule, it is strongly recommended that the
    :class:`G` element is used because it simplifies processing.
    The :class:`Bx` element should be followed by a matching :class:`Ex` element.
    These paired elements are related via their :attr:`rid` attributes.
    If the :attr:`rid` attribute is not present (in a 1.0 document for example),
    the attribute :attr:`id` is used to match both tags.
    """

    id: str
    """
    *Identifier* - Used as a reference to the original corresponding code data
    or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document.
    It may or may not be a resource identifier.
    The identifier of a resource should, at least, be stored in the
    resname attribute.
    """
    rid: str | None = field(default=None)
    """
    *Reference identifier* - Used to link paired inline elements.
    The rid attribute of a begin-paired-code element should have the
    same value as the close-paired-code element.
    """
    ctype: CTYPE | str | None = field(default=None)
    """
    *Content type* - Specifies the type of code that is represented by the
    inline element.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    clone: bool | None = field(default=None)
    """
    *Clone* - Indicates that a copy of the given inline element can be made and
    placed multiple times in the :class:`python_xliff.Objects.Structural.Target`.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - Used to link an inline element to a different
    :class:`python_xliff.Objects.Structural.TransUnit` or
    :class:`python_xliff.Objects.Structural.BinUnit` element.
    """
    equiv_text: str | None = field(default=None)
    """
    *equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag.
    """


@dataclass(slots=True, kw_only=True)
class Ex:
    """
    *End paired placeholder* - Used to replace an ending paired code of the
    original document.
    It should be used for paired codes that do not follow XML well-formedness
    rules (i.e. no overlapping elements).
    If the paired codes follow that rule, it is strongly recommended that the
    :class:`G` element is used because it simplifies processing.
    The :class:`Ex` element should be preceded by a matching :class:`Bx` element.
    These paired elements are related via their :attr:`rid` attributes.
    If the :attr:`rid` attribute is not present (in a 1.0 document for example),
    the attribute :attr:`id` is used to match both tags.
    """

    id: str
    """
    *Identifier* - Used as a reference to the original corresponding code data
    or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document.
    It may or may not be a resource identifier.
    The identifier of a resource should, at least, be stored in the
    resname attribute.
    """
    rid: str | None = field(default=None)
    """
    *Reference identifier* - Used to link paired inline elements.
    The rid attribute of a begin-paired-code element should have the
    same value as the close-paired-code element.
    """
    ctype: CTYPE | str | None = field(default=None)
    """
    *Content type* - Specifies the type of code that is represented by the
    inline element.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    clone: bool | None = field(default=None)
    """
    *Clone* - Indicates that a copy of the given inline element can be made and
    placed multiple times in the :class:`python_xliff.Objects.Structural.Target`.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - Used to link an inline element to a different
    :class:`python_xliff.Objects.Structural.TransUnit` or
    :class:`python_xliff.Objects.Structural.BinUnit` element.
    """
    equiv_text: str | None = field(default=None)
    """
    *equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag.
    """


@dataclass(slots=True, kw_only=True)
class Ph:
    """
    *Placeholder* - Used to delimit a sequence of native stand-alone codes in
    the translation unit.
    """

    crc: float | None = field(default=None)
    """
    *Cyclic redundancy checking* - Used to verify data as it is returned to the
    producer. The generation and verification of this number is tool-specific.
    """
    assoc: ASSOC | None = field(default=None)
    """
    *Association* - Indicates the association of a :class:`Ph` with the text
    prior or after the inline element.
    """
    id: str
    """
    *Identifier* - Used as a reference to the original corresponding code data
    or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document.
    It may or may not be a resource identifier.
    The identifier of a resource should, at least, be stored in the
    resname attribute.
    """
    rid: str | None = field(default=None)
    """
    *Reference identifier* - Used to link paired inline elements.
    The rid attribute of a begin-paired-code element should have the
    same value as the close-paired-code element.
    """
    ctype: CTYPE | str | None = field(default=None)
    """
    *Content type* - Specifies the type of code that is represented by the
    inline element.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    clone: bool | None = field(default=None)
    """
    *Clone* - Indicates that a copy of the given inline element can be made and
    placed multiple times in the :class:`python_xliff.Objects.Structural.Target`.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - Used to link an inline element to a different
    :class:`python_xliff.Objects.Structural.TransUnit` or
    :class:`python_xliff.Objects.Structural.BinUnit` element.
    """
    equiv_text: str | None = field(default=None)
    """
    *equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag.
    """
    content: MutableSequence[str | Sub] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class Bpt:
    """
    *Begin paired tag* - Used to delimit the beginning of a paired sequence of
    native codes. Each :class:`Bpt` has a corresponding :class:`Ept` element
    within the translation unit.
    These paired elements are related via their :attr:`rid` attributes.
    If the :attr:`rid` attribute is not present (in a 1.0 document for example),
    the attribute :attr:`id` is used to match both tags.
    """

    crc: float | None = field(default=None)
    """
    *Cyclic redundancy checking* - Used to verify data as it is returned to the
    producer. The generation and verification of this number is tool-specific.
    """
    id: str
    """
    *Identifier* - Used as a reference to the original corresponding code data
    or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document.
    It may or may not be a resource identifier.
    The identifier of a resource should, at least, be stored in the
    resname attribute.
    """
    rid: str | None = field(default=None)
    """
    *Reference identifier* - Used to link paired inline elements.
    The rid attribute of a begin-paired-code element should have the
    same value as the close-paired-code element.
    """
    ctype: CTYPE | str | None = field(default=None)
    """
    *Content type* - Specifies the type of code that is represented by the
    inline element.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    clone: bool | None = field(default=None)
    """
    *Clone* - Indicates that a copy of the given inline element can be made and
    placed multiple times in the :class:`python_xliff.Objects.Structural.Target`.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - Used to link an inline element to a different
    :class:`python_xliff.Objects.Structural.TransUnit` or
    :class:`python_xliff.Objects.Structural.BinUnit` element.
    """
    equiv_text: str | None = field(default=None)
    """
    *equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag.
    """
    content: MutableSequence[str | Sub] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class Ept:
    """
    *End paired tag* - Used to delimit the end of a paired sequence of native
    codes. Each :class:`Ept` has a corresponding :class:`Bpt` element
    within the translation unit.
    These paired elements are related via their :attr:`rid` attributes.
    If the :attr:`rid` attribute is not present (in a 1.0 document for example),
    the attribute :attr:`id` is used to match both tags.
    """

    crc: float | None = field(default=None)
    """
    *Cyclic redundancy checking* - Used to verify data as it is returned to the
    producer. The generation and verification of this number is tool-specific.
    """
    id: str
    """
    *Identifier* - Used as a reference to the original corresponding code data
    or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document.
    It may or may not be a resource identifier.
    The identifier of a resource should, at least, be stored in the
    resname attribute.
    """
    rid: str | None = field(default=None)
    """
    *Reference identifier* - Used to link paired inline elements.
    The rid attribute of a begin-paired-code element should have the
    same value as the close-paired-code element.
    """
    ctype: CTYPE | str | None = field(default=None)
    """
    *Content type* - Specifies the type of code that is represented by the
    inline element.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    clone: bool | None = field(default=None)
    """
    *Clone* - Indicates that a copy of the given inline element can be made and
    placed multiple times in the :class:`python_xliff.Objects.Structural.Target`.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - Used to link an inline element to a different
    :class:`python_xliff.Objects.Structural.TransUnit` or
    :class:`python_xliff.Objects.Structural.BinUnit` element.
    """
    equiv_text: str | None = field(default=None)
    """
    *equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag.
    """
    content: MutableSequence[str | Sub] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class It:
    """
    *Isolated tag* - Used to delimit a beginning/ending sequence of native codes
    that does not have its corresponding ending/beginning within the translation
    unit.
    """

    pos: POS
    """
    *Position* - Indicates whether an isolated tag :class:`It` is a beginning or
    an ending tag.
    """
    crc: float | None = field(default=None)
    """
    *Cyclic redundancy checking* - Used to verify data as it is returned to the
    producer. The generation and verification of this number is tool-specific.
    """
    id: str
    """
    *Identifier* - Used as a reference to the original corresponding code data
    or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document.
    It may or may not be a resource identifier.
    The identifier of a resource should, at least, be stored in the
    resname attribute.
    """
    rid: str | None = field(default=None)
    """
    *Reference identifier* - Used to link paired inline elements.
    The rid attribute of a begin-paired-code element should have the
    same value as the close-paired-code element.
    """
    ctype: CTYPE | str | None = field(default=None)
    """
    *Content type* - Specifies the type of code that is represented by the
    inline element.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    clone: bool | None = field(default=None)
    """
    *Clone* - Indicates that a copy of the given inline element can be made and
    placed multiple times in the :class:`python_xliff.Objects.Structural.Target`.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - Used to link an inline element to a different
    :class:`python_xliff.Objects.Structural.TransUnit` or
    :class:`python_xliff.Objects.Structural.BinUnit` element.
    """
    equiv_text: str | None = field(default=None)
    """
    *equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag.
    """
    content: MutableSequence[str | Sub] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class Sub:
    """
    *Sub-flow* - Used to delimit sub-flow text inside a sequence of native code,
    """

    datatype: DATATYPE | str | None = field(default=None)
    """
    *Data type* - Specifies the kind of text contained in the element.
    """
    ctype: CTYPE | str | None = field(default=None)
    """
    *Content type* - Specifies the type of code that is represented by the
    inline element.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - Used to link an inline element to a different
    :class:`python_xliff.Objects.Structural.TransUnit` or
    :class:`python_xliff.Objects.Structural.BinUnit` element.
    """
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = field(
        default_factory=list
    )


@dataclass(slots=True, kw_only=True)
class Mrk:
    """
    *Marker* - Delimits a section of text that has special meaning, such as a
    terminological unit, a proper name, an item that should not be modified, etc.
    """

    mtype: MTYPE | str
    """
    *Marker type* - Specifies what a :class:`Mrk` element is defining within the
    content of a :class:`python_xliff.Objects.Structural.Source` or
    :class:`python_xliff.Objects.Structural.Target` element.
    """
    mid: str | None = field(default=None)
    """
    *Marker ID* - Used to reference segments between the
    :class:`python_xliff.Objects.Structural.SegSource` and
    :class:`python_xliff.Objects.Structural.Target` of a 
    :class:`python_xliff.Objects.Structural.TransUnit`.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    comment: str | None = field(default=None)
    """
    *Comment* - A comment in a tag.
    """
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Self] = (
        field(default_factory=list)
    )
