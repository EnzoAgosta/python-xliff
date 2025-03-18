from __future__ import annotations

from collections.abc import MutableSequence
from dataclasses import dataclass, field
from typing import Literal, Self

from python_xliff.Objects.extras import CTYPE, DATATYPE, MTYPE, POS, X_PH_CTYPE


@dataclass(slots=True, kw_only=True)
class G:
    id: str
    """
    *Identifier* - The id attribute is used in many elements as a reference to
    the original corresponding code data or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document. It may or may not be a resource identifier. The identifier of a
    resource should, at least, be stored in the resname attribute.
    """
    ctype: CTYPE | str | None = field(default=None)
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - The ts attribute allows you to include short data
    understood by a specific toolset. You can also use the :class:`Prop`
    element to define large properties at the element level.
    Important: The ts attribute was DEPRECATED in version 1.1. Instead, use
    attributes defined in a namespace different from XLIFF.
    See the Extensibility section for more information.
    """
    """
    *Tool-specific data* - The ts attribute allows you to include short data
    understood by a specific toolset. You can also use the :class:`Prop`
    element to define large properties at the element level.
    Important: The ts attribute was DEPRECATED in version 1.1. Instead, use
    attributes defined in a namespace different from XLIFF.
    See the Extensibility section for more information.
    """
    clone: bool | None = field(default=None)
    """
    *Clone* - This indicates that a copy of the given inline element can be made
    and placed multiple times in the :class:`Target`. This is useful for codes
    such as bold which may require duplication after localization of a segment.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - The xid attribute is used to link an inline
    element to a different :class:`TransUnit` or :class:`BinUnit` element.
    For example, to link the text within a code to a corresponding translation
    unit.
    """
    equiv_text: str | None = field(default=None)
    """*equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag. It is useful for inserting whitespace or other content in place
    of markup to facilitate consistent word counting. The equiv-text attribute
    is also useful for ensuring consistent round trip conversion between native
    resource formats and XLIFF content, for example the resource string "F&ile"
    converts to the following XLIFF: "F<x id='1' ctype='x-akey' equiv-text=''/>
    ile" to preserve the underlying translatable content.
    """
    content: MutableSequence[str | Self | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = (
        field(default_factory=list)
    )


@dataclass(slots=True, kw_only=True)
class X:
    id: str
    """
    *Identifier* - The id attribute is used in many elements as a reference to
    the original corresponding code data or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document. It may or may not be a resource identifier. The identifier of a
    resource should, at least, be stored in the resname attribute.
    """
    ctype: X_PH_CTYPE | str | None = field(default=None)
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - The ts attribute allows you to include short data
    understood by a specific toolset. You can also use the :class:`Prop`
    element to define large properties at the element level.
    Important: The ts attribute was DEPRECATED in version 1.1. Instead, use
    attributes defined in a namespace different from XLIFF.
    See the Extensibility section for more information.
    """
    clone: bool | None = field(default=None)
    """
    *Clone* - This indicates that a copy of the given inline element can be made
    and placed multiple times in the :class:`Target`. This is useful for codes
    such as bold which may require duplication after localization of a segment.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - The xid attribute is used to link an inline
    element to a different :class:`TransUnit` or :class:`BinUnit` element.
    For example, to link the text within a code to a corresponding translation
    unit.
    """
    equiv_text: str | None = field(default=None)
    """*equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag. It is useful for inserting whitespace or other content in place
    of markup to facilitate consistent word counting. The equiv-text attribute
    is also useful for ensuring consistent round trip conversion between native
    resource formats and XLIFF content, for example the resource string "F&ile"
    converts to the following XLIFF: "F<x id='1' ctype='x-akey' equiv-text=''/>
    ile" to preserve the underlying translatable content.
    """


@dataclass(slots=True, kw_only=True)
class Bx:
    id: str
    """
    *Identifier* - The id attribute is used in many elements as a reference to
    the original corresponding code data or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document. It may or may not be a resource identifier. The identifier of a
    resource should, at least, be stored in the resname attribute.
    """
    rid: str | None = field(default=None)
    """
    *Reference identifier* - The rid attribute is used to link paired inline
    elements. The rid attribute of a begin-paired-code element should have the
    same value as the close-paired-code element.
    For example: <bx id="1" rid="1"/> ... <ex id="3" rid="1"/> indicates these
    elements are paired. If the rid attribute is not present (in a 1.0 document
    for example), the attribute id is used to match both tags. For example:
    <bpt id='5'>xx</bpt> ... <ept id='5'>xx</ept>.
    """
    ctype: CTYPE | str | None = field(default=None)
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - The ts attribute allows you to include short data
    understood by a specific toolset. You can also use the :class:`Prop`
    element to define large properties at the element level.
    Important: The ts attribute was DEPRECATED in version 1.1. Instead, use
    attributes defined in a namespace different from XLIFF.
    See the Extensibility section for more information.
    """
    clone: bool | None = field(default=None)
    """
    *Clone* - This indicates that a copy of the given inline element can be made
    and placed multiple times in the :class:`Target`. This is useful for codes
    such as bold which may require duplication after localization of a segment.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - The xid attribute is used to link an inline
    element to a different :class:`TransUnit` or :class:`BinUnit` element.
    For example, to link the text within a code to a corresponding translation
    unit.
    """
    equiv_text: str | None = field(default=None)
    """*equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag. It is useful for inserting whitespace or other content in place
    of markup to facilitate consistent word counting. The equiv-text attribute
    is also useful for ensuring consistent round trip conversion between native
    resource formats and XLIFF content, for example the resource string "F&ile"
    converts to the following XLIFF: "F<x id='1' ctype='x-akey' equiv-text=''/>
    ile" to preserve the underlying translatable content.
    """


@dataclass(slots=True, kw_only=True)
class Ex:
    id: str
    """
    *Identifier* - The id attribute is used in many elements as a reference to
    the original corresponding code data or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document. It may or may not be a resource identifier. The identifier of a
    resource should, at least, be stored in the resname attribute.
    """
    rid: str | None = field(default=None)
    """
    *Reference identifier* - The rid attribute is used to link paired inline
    elements. The rid attribute of a begin-paired-code element should have the
    same value as the close-paired-code element.
    For example: <bx id="1" rid="1"/> ... <ex id="3" rid="1"/> indicates these
    elements are paired. If the rid attribute is not present (in a 1.0 document
    for example), the attribute id is used to match both tags. For example:
    <bpt id='5'>xx</bpt> ... <ept id='5'>xx</ept>.
    """
    ctype: CTYPE | str | None = field(default=None)
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - The ts attribute allows you to include short data
    understood by a specific toolset. You can also use the :class:`Prop`
    element to define large properties at the element level.
    Important: The ts attribute was DEPRECATED in version 1.1. Instead, use
    attributes defined in a namespace different from XLIFF.
    See the Extensibility section for more information.
    """
    clone: bool | None = field(default=None)
    """
    *Clone* - This indicates that a copy of the given inline element can be made
    and placed multiple times in the :class:`Target`. This is useful for codes
    such as bold which may require duplication after localization of a segment.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - The xid attribute is used to link an inline
    element to a different :class:`TransUnit` or :class:`BinUnit` element.
    For example, to link the text within a code to a corresponding translation
    unit.
    """
    equiv_text: str | None = field(default=None)
    """*equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag. It is useful for inserting whitespace or other content in place
    of markup to facilitate consistent word counting. The equiv-text attribute
    is also useful for ensuring consistent round trip conversion between native
    resource formats and XLIFF content, for example the resource string "F&ile"
    converts to the following XLIFF: "F<x id='1' ctype='x-akey' equiv-text=''/>
    ile" to preserve the underlying translatable content.
    """


@dataclass(slots=True, kw_only=True)
class Ph:
    id: str
    """
    *Identifier* - The id attribute is used in many elements as a reference to
    the original corresponding code data or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document. It may or may not be a resource identifier. The identifier of a
    resource should, at least, be stored in the resname attribute.
    """
    ctype: X_PH_CTYPE | str | None = field(default=None)
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - The ts attribute allows you to include short data
    understood by a specific toolset. You can also use the :class:`Prop`
    element to define large properties at the element level.
    Important: The ts attribute was DEPRECATED in version 1.1. Instead, use
    attributes defined in a namespace different from XLIFF.
    See the Extensibility section for more information.
    """
    crc: float | None = field(default=None)
    """
    *Cyclic redundancy checking* - A private value used to verify data as it is
    returned to the producer. The generation and verification of this number is
    tool-specific.
    """
    assoc: Literal["preceding", "following", "both"] | None = field(default=None)
    """
    *Association* - Indicates the association of a :class:`Ph` with the text
    prior or after the inline element.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - The xid attribute is used to link an inline
    element to a different :class:`TransUnit` or :class:`BinUnit` element.
    For example, to link the text within a code to a corresponding translation
    unit.
    """
    equiv_text: str | None = field(default=None)
    """*equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag. It is useful for inserting whitespace or other content in place
    of markup to facilitate consistent word counting. The equiv-text attribute
    is also useful for ensuring consistent round trip conversion between native
    resource formats and XLIFF content, for example the resource string "F&ile"
    converts to the following XLIFF: "F<x id='1' ctype='x-akey' equiv-text=''/>
    ile" to preserve the underlying translatable content.
    """
    content: MutableSequence[str | Sub] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class Bpt:
    id: str
    """
    *Identifier* - The id attribute is used in many elements as a reference to
    the original corresponding code data or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document. It may or may not be a resource identifier. The identifier of a
    resource should, at least, be stored in the resname attribute.
    """
    rid: str | None = field(default=None)
    """
    *Reference identifier* - The rid attribute is used to link paired inline
    elements. The rid attribute of a begin-paired-code element should have the
    same value as the close-paired-code element.
    For example: <bx id="1" rid="1"/> ... <ex id="3" rid="1"/> indicates these
    elements are paired. If the rid attribute is not present (in a 1.0 document
    for example), the attribute id is used to match both tags. For example:
    <bpt id='5'>xx</bpt> ... <ept id='5'>xx</ept>.
    """
    ctype: CTYPE | str | None = field(default=None)
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - The ts attribute allows you to include short data
    understood by a specific toolset. You can also use the :class:`Prop`
    element to define large properties at the element level.
    Important: The ts attribute was DEPRECATED in version 1.1. Instead, use
    attributes defined in a namespace different from XLIFF.
    See the Extensibility section for more information.
    """
    crc: float | None = field(default=None)
    """
    *Cyclic redundancy checking* - A private value used to verify data as it is
    returned to the producer. The generation and verification of this number is
    tool-specific.
    """
    equiv_text: str | None = field(default=None)
    """*equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag. It is useful for inserting whitespace or other content in place
    of markup to facilitate consistent word counting. The equiv-text attribute
    is also useful for ensuring consistent round trip conversion between native
    resource formats and XLIFF content, for example the resource string "F&ile"
    converts to the following XLIFF: "F<x id='1' ctype='x-akey' equiv-text=''/>
    ile" to preserve the underlying translatable content.
    """

    content: MutableSequence[str | Sub] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class Ept:
    id: str
    """
    *Identifier* - The id attribute is used in many elements as a reference to
    the original corresponding code data or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document. It may or may not be a resource identifier. The identifier of a
    resource should, at least, be stored in the resname attribute.
    """
    rid: str | None = field(default=None)
    """
    *Reference identifier* - The rid attribute is used to link paired inline
    elements. The rid attribute of a begin-paired-code element should have the
    same value as the close-paired-code element.
    For example: <bx id="1" rid="1"/> ... <ex id="3" rid="1"/> indicates these
    elements are paired. If the rid attribute is not present (in a 1.0 document
    for example), the attribute id is used to match both tags. For example:
    <bpt id='5'>xx</bpt> ... <ept id='5'>xx</ept>.
    """
    ctype: CTYPE | str | None = field(default=None)
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - The ts attribute allows you to include short data
    understood by a specific toolset. You can also use the :class:`Prop`
    element to define large properties at the element level.
    Important: The ts attribute was DEPRECATED in version 1.1. Instead, use
    attributes defined in a namespace different from XLIFF.
    See the Extensibility section for more information.
    """
    crc: float | None = field(default=None)
    """
    *Cyclic redundancy checking* - A private value used to verify data as it is
    returned to the producer. The generation and verification of this number is
    tool-specific.
    """
    equiv_text: str | None = field(default=None)
    """*equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag. It is useful for inserting whitespace or other content in place
    of markup to facilitate consistent word counting. The equiv-text attribute
    is also useful for ensuring consistent round trip conversion between native
    resource formats and XLIFF content, for example the resource string "F&ile"
    converts to the following XLIFF: "F<x id='1' ctype='x-akey' equiv-text=''/>
    ile" to preserve the underlying translatable content.
    """
    content: MutableSequence[str | Sub] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class It:
    id: str
    """
    *Identifier* - The id attribute is used in many elements as a reference to
    the original corresponding code data or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document. It may or may not be a resource identifier. The identifier of a
    resource should, at least, be stored in the resname attribute.
    """
    pos: POS
    rid: str | None = field(default=None)
    """
    *Reference identifier* - The rid attribute is used to link paired inline
    elements. The rid attribute of a begin-paired-code element should have the
    same value as the close-paired-code element.
    For example: <bx id="1" rid="1"/> ... <ex id="3" rid="1"/> indicates these
    elements are paired. If the rid attribute is not present (in a 1.0 document
    for example), the attribute id is used to match both tags. For example:
    <bpt id='5'>xx</bpt> ... <ept id='5'>xx</ept>.
    """
    ctype: CTYPE | str | None = field(default=None)
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - The ts attribute allows you to include short data
    understood by a specific toolset. You can also use the :class:`Prop`
    element to define large properties at the element level.
    Important: The ts attribute was DEPRECATED in version 1.1. Instead, use
    attributes defined in a namespace different from XLIFF.
    See the Extensibility section for more information.
    """
    crc: float | None = field(default=None)
    """
    *Cyclic redundancy checking* - A private value used to verify data as it is
    returned to the producer. The generation and verification of this number is
    tool-specific.
    """
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - The xid attribute is used to link an inline
    element to a different :class:`TransUnit` or :class:`BinUnit` element.
    For example, to link the text within a code to a corresponding translation
    unit.
    """
    equiv_text: str | None = field(default=None)
    """*equiv-text* - Indicates the equivalent text to substitute in place of an
    inline tag. It is useful for inserting whitespace or other content in place
    of markup to facilitate consistent word counting. The equiv-text attribute
    is also useful for ensuring consistent round trip conversion between native
    resource formats and XLIFF content, for example the resource string "F&ile"
    converts to the following XLIFF: "F<x id='1' ctype='x-akey' equiv-text=''/>
    ile" to preserve the underlying translatable content.
    """
    content: MutableSequence[str | Sub] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class Sub:
    datatype: DATATYPE | str | None = field(default=None)
    """
    *Data type* - The datatype attribute specifies the kind of text contained in
    the element. Depending on that type, you may apply different processes
    to the data. For example: datatype="winres" specifies that the content is
    Windows resources which would allow using the Win32 API in rendering the content.
   """
    ctype: CTYPE | str | None = field(default=None)
    xid: str | None = field(default=None)
    """
    *Extern Reference identifier* - The xid attribute is used to link an inline
    element to a different :class:`TransUnit` or :class:`BinUnit` element.
    For example, to link the text within a code to a corresponding translation
    unit.
    """
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = field(
        default_factory=list
    )


@dataclass(slots=True, kw_only=True)
class Mrk:
    mtype: MTYPE | str
    """
    *Marker type* -The mtype attribute specifies what a :class:`Mrk` element is
    defining within the content of a :class:`Source` or :class:`Target` element.
    """
    mid: str | None = field(default=None)
    """
    *Marker ID* - Identifier for an :class:`Mrk` element. When used with in
    combination with mtype="seg" the value of this attribute is used to reference
    segments between the :class:`SegSource` and :class:`Target` of a 
    :class:`TransUnit`. When used in :class:`AltTrans` this attribute indicates
    that the entire :class:`AltTrans` element references a particular
    <mrk mtype ="seg"> segment in the :class:`SegSource` (and :class:`Target`)
    element. See the Segmentation section for further details.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - The ts attribute allows you to include short data
    understood by a specific toolset. You can also use the :class:`Prop`
    element to define large properties at the element level.
    Important: The ts attribute was DEPRECATED in version 1.1. Instead, use
    attributes defined in a namespace different from XLIFF.
    See the Extensibility section for more information.
    """
    comment: str | None = field(default=None)
    """
    *Comment* - A comment in a tag.
    """
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Self] = (
        field(default_factory=list)
    )
