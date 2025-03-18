from collections.abc import MutableSequence
from dataclasses import dataclass, field
from typing import Self

from python_xliff.Objects.extras import (
    ALT_TRANS_TYPE,
    DATATYPE,
    REFORMAT,
    RESTYPE,
    SIZE_UNIT,
    STATE,
    STATE_QUALIFIER,
    Coord,
    Font,
)
from python_xliff.Objects.Inline import Bpt, Bx, Ept, Ex, G, It, Mrk, Ph, X
from python_xliff.Objects.NamedGroups import ContextGroup, CountGroup, PropGroup
from python_xliff.Objects.TopLevel import ExternalFile, InternalFile, Note


@dataclass(slots=True, kw_only=True)
class Source:
    """
    *Source text* – Used to delimit a unit of text that could be a paragraph,
    a title, a menu item, a caption, etc.
    The content of the :class:`Source` is generally the translatable text,
    depending upon the translate attribute of the parent :class:`TransUnit`.
    """

    lang: str | None = field(default=None)
    """
    *Language* - Specifies the language variant of the text of a given element.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* – Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = field(
        default_factory=list
    )


@dataclass(slots=True, kw_only=True)
class Target:
    """
    *Target* – Contains the translation of the content of the sibling
    :class:`Source` element.
    """

    state: STATE | str | None = field(default=None)
    """
    *State* – Indicates the status of a particular translation in a
    :class:`Target` or s:class:`BinTarget` element.
    """
    state_qualifier: STATE_QUALIFIER | str | None = field(default=None)
    """
    *State-qualifier* – Describes the state of a particular translation in a
    :class:`Target` or :class:`BinTarget` element.
    """
    phase_name: str | None = field(default=None)
    """
    *Phase Name* – Used to refer to the given class:`Phase` element.
    """
    lang: str | None = field(default=None)
    """
    *Language* - Specifies the language variant of the text of a given element.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* – Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    restype: RESTYPE | str | None = field(default=None)
    """
    *Resource type* – Indicates the resource type of the container element.
    """
    resname: str | None = field(default=None)
    """
    *Resource name* – Resource name or identifier of a item.
    """
    coord: Coord | None = field(default=None)
    """
    *Coordinates* – Specifies the x, y, cx and cy coordinates of the text for a
    given element. The cx and cy values must represent the width and the height
    (as in Windows resources).
    """
    font: Font | None = field(default=None)
    """
    *Font* – Specifies the font name, size, and weight of the text for a given
    element.
    """
    css_style: str | None = field(default=None)
    """
    *Cascading style-sheet style* – Allows any valid CSS statement to be specified.
    """
    style: str | None = field(default=None)
    """
    *Style* – The resource style of a control.
    """
    exstyle: str | None = field(default=None)
    """
    *Extended style* – Stores the extended style of a control.
    """
    equiv_trans: bool | None = field(default=None)
    """
    *equiv-trans* – Indicates if the target language translation is a direct
    equivalent of the source text.
    """
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = field(
        default_factory=list
    )


@dataclass(slots=True, kw_only=True)
class BinSource:
    """
    *Binary source* – Container for the binary source data.
    """

    content: InternalFile | ExternalFile
    ts: str | None = field(default=None)
    """
    *Tool-specific data* – Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """


@dataclass(slots=True, kw_only=True)
class BinTarget:
    """
    *Binary target* – Container for the translated version of the binary data.
    """

    content: InternalFile | ExternalFile
    mime_type: str | None = field(default=None)
    """
    *Mime type* – Indicates the type of a binary object. These roughly correspond
    to the content-type of RFC 1341 , the MIME specification.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* – Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    state: STATE | str | None = field(default=None)
    """
    *State* – The status of a particular translation in a :class:`Target` or
    :class:`BinTarget` element.
    """
    phase_name: str | None = field(default=None)
    """
    *Phase Name* – Used to refer to the given class:`Phase` element.
    """
    restype: RESTYPE | str | None = field(default=None)
    """
    *Resource type* – Indicates the resource type of the container element.
    """
    resname: str | None = field(default=None)
    """
    *Resource name* – Resource name or identifier of a item.
    """
    state_qualifier: STATE_QUALIFIER | str | None = field(default=None)
    """
    *State-qualifier* – Describes the state of a particular translation in a
    :class:`Target` or :class:`BinTarget` element.
    """


@dataclass(slots=True, kw_only=True)
class SegSource:
    """
    *Source text* - Used to maintain a working copy of the :class:`Source`
    element, where markup such as segmentation can be introduced without
    affecting the actual :class:`Source` element content.
    """

    lang: str | None = field(default=None)
    """
    *Language* - Specifies the language variant of the text of a given element.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* – Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = field(
        default_factory=list
    )


@dataclass(slots=True, kw_only=True)
class AltTrans:
    """
    *Translation match* - Contains possible translations in :class:`Target` and
    along with optional context, notes, etc.
    """

    source: Source
    target: Target
    mid: str | None = field(default=None)
    """
    *Marker ID* – Indicates that the entire :class:`AltTrans` element
    references a particular :class:`python_xliff.Objects.Inline.Mrk` segment
    (with the :attr:`python_xliff.Objects.Inline.Mrk.mtype` attribute set to "seg")
    in the the :class:`SegSource` and :class:`Target` elements.
    """
    match_quality: str | None = field(default=None)
    """
    *Match quality* – tool specific and can be a score expressed in percentage
    or an arbitrary value (e.g. match-quality="high").
    """
    tool: str | None = field(default=None)
    """
    *Creation tool* – Specify the signature and version of the tool that
    created or modified the document.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use the :class:`Tool` element and
        a :attr:`tool_id` attribute.
    """
    tool_id: str | None = field(default=None)
    """
    *Tool identifier* – Used to refer to the given :class:`Tool` element.
    """
    crc: float | None = field(default=None)
    """
    *Cyclic redundancy checking* – Used to verify data as it is returned to the
    producer. The generation and verification of this number is tool-specific.
    """
    lang: str | None = field(default=None)
    """
    *Language* - Specifies the language variant of the text of a given element.
    """
    datatype: DATATYPE | str | None = field(default=None)
    """
    *Data type* – Specifies the kind of text contained in the element.
    """
    space: str | None = field(default=None)
    """
    *White spaces* – Specifies how white spaces (ASCII spaces, tabs and
    line-breaks) should be treated.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* – Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    restype: RESTYPE | str | None = field(default=None)
    """
    *Resource type* – Indicates the resource type of the container element.
    """
    resname: str | None = field(default=None)
    """
    *Resource name* – Resource name or identifier of a item.
    """
    extradata: str | None = field(default=None)
    """
    *Extra data* – Stores the extra data properties of an item.
    """
    help_id: int | None = field(default=None)
    """
    *Help ID* – Stores the help identifier of an item.
    """
    menu: str | None = field(default=None)
    """
    *Menu* – Stores the menu property of an item.
    """
    menu_option: str | None = field(default=None)
    """
    *Menu option* – Stores the option data of a control.
    """
    menu_name: str | None = field(default=None)
    """
    *Menu name* – Stores the menu name of a control.
    """
    coord: Coord | None = field(default=None)
    """
    *Coordinates* – Specifies the x, y, cx and cy coordinates of the text.
    The cx and cy values must represent the width and the height (as in Windows
    resources).
    """
    font: Font | None = field(default=None)
    """
    *Font* – Specifies the font name, size, and weight of the text.
    """
    css_style: str | None = field(default=None)
    """
    *Cascading style-sheet style* – Allows any valid CSS statement to be specified.
    """
    style: str | None = field(default=None)
    """
    *Style* – The resource style of a control.
    """
    exstyle: str | None = field(default=None)
    """
    *Extended style* – Stores the extended style of a control.
    """
    extype: str | None = field(default=None)
    """
    *Extended type* – Stores the extra type properties of an item.
    """
    origin: str | None = field(default=None)
    """
    *Translation Match Origin* – Specifies where a translation match came from.
    """
    phase_name: str | None = field(default=None)
    """
    *Phase Name* – Used to refer to the given :class:`Phase` element.
    """
    alttranstype: str | ALT_TRANS_TYPE | None = field(default=None)
    """
    *Resource type* – Indicates the type of translation within the containing
    :class:`AltTrans` element.
    """
    seg_sources: MutableSequence[SegSource] = field(default_factory=list)
    context_groups: MutableSequence[ContextGroup] = field(default_factory=list)
    count_groups: MutableSequence[CountGroup] = field(default_factory=list)
    prop_groups: MutableSequence[PropGroup] = field(default_factory=list)
    notes: MutableSequence[Note] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class TransUnit:
    """
    *Translation unit* – The :class:`TransUnit` elements contains a :class:`Source`,
    :class:`Target` and associated elements.
    """

    source: Source
    target: Target
    id: str
    """
    *Identifier* – Used as a reference to the original corresponding code data
    or format. The value of the id element is determined by the tool creating
    the XLIFF document. It may or may not be a resource identifier.
    The identifier of a resource should, at least, be stored in the
    resname attribute.
    """
    approved: bool | None = field(default=None)
    """
    *Approved* – Indicates whether a translation is final or has passed its final
    review.
    """
    translate: bool | None = field(default=None)
    """
    *Translate* – Indicates whether or not the text referred to should be
    translated.
    """
    reformat: bool | MutableSequence[REFORMAT] | None = field(default=None)
    """
    Reformat – Indicates whether some properties (size, font, etc.) of the target
    can be formatted differently from the source.
    """
    space: str | None = field(default=None)
    """
    *White spaces* – Specifies how white spaces (ASCII spaces, tabs and
    line-breaks) should be treated.
    """
    datatype: DATATYPE | str | None = field(default=None)
    """
    *Data type* – Specifies the kind of text contained in the element.
   """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* – Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    phase_name: str | None = field(default=None)
    """
    *Phase Name* – Used to refer to the given class:`Phase` element.
    """
    restype: RESTYPE | str | None = field(default=None)
    """
    *Resource type* – Indicates the resource type of the container element.
    """
    resname: str | None = field(default=None)
    """
    *Resource name* – Resource name or identifier of a item.
    """
    extradata: str | None = field(default=None)
    """
    *Extra data* – Stores the extra data properties of an item.
    """
    help_id: int | None = field(default=None)
    """
    *Help ID* – Stores the help identifier of an item.
    """
    menu: str | None = field(default=None)
    """
    *Menu* – Stores the menu property of an item.
    """
    menu_option: str | None = field(default=None)
    """
    *Menu option* – Stores the option data of a control.
    """
    menu_name: str | None = field(default=None)
    """
    *Menu name* – Stores the menu name of a control.
    """
    coord: Coord | None = field(default=None)
    """
    *Coordinates* – Specifies the x, y, cx and cy coordinates of the text.
    The cx and cy values must represent the width and the height (as in Windows
    resources).
    """
    font: Font | None = field(default=None)
    """
    *Font* – Specifies the font name, size, and weight of the text.
    """
    css_style: str | None = field(default=None)
    """
    *Cascading style-sheet style* – Allows any valid CSS statement to be specified.
    """
    style: str | None = field(default=None)
    """
    *Style* – The resource style of a control.
    """
    exstyle: str | None = field(default=None)
    """
    *Extended style* – Stores the extended style of a control. 
    """
    extype: str | None = field(default=None)
    """
    *Extended type* – Stores the extra type properties of an item.
    """
    maxbytes: int | None = field(default=None)
    """
    *Maximum bytes* – The maximum number of bytes for the :class:`Target` of a
    :class:`TransUnit`.
    """
    minbytes: int | None = field(default=None)
    """
    *Minimum bytes* – The minimum number of bytes for the :class:`Target` of a
    :class:`TransUnit`.
    """
    size_unit: SIZE_UNIT | str | None = field(default=None)
    """
    *Unit of size attributes* – Specifies the units of measure used in the
    maxheight, minheight, maxwidth, and minwidth attributes.
    """
    maxheight: int | None = field(default=None)
    """
    *Maximum height* – The maximum height for the :class:`Target` of a
    :class:`TransUnit`.
    """
    minheight: int | None = field(default=None)
    """
    *Minimum height* – The minimum height for the :class:`Target` of a
    :class:`TransUnit`.
    """
    maxwidth: int | None = field(default=None)
    """
    *Maximum width* – The maximum width for the :class:`Target` of a 
    :class:`TransUnit`.
    """
    minwidth: int | None = field(default=None)
    """
    *Minimum width* – The minimum width for the :class:`Target` of a
    :class:`TransUnit`.
    """
    charclass: str | None = field(default=None)
    seg_sources: MutableSequence[SegSource] = field(default_factory=list)
    context_groups: MutableSequence[ContextGroup] = field(default_factory=list)
    count_groups: MutableSequence[CountGroup] = field(default_factory=list)
    prop_groups: MutableSequence[PropGroup] = field(default_factory=list)
    notes: MutableSequence[Note] = field(default_factory=list)
    alt_trans: MutableSequence[AltTrans] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class BinUnit:
    """
    Binary unit – Contains a binary object that may or may not be translatable.
    """

    bin_source: BinSource
    id: str
    """
    *Identifier* – Used as a reference to the original corresponding code data
    or format. The value of the id element is determined by the tool creating
    the XLIFF document. It may or may not be a resource identifier.
    The identifier of a resource should, at least, be stored in the
    resname attribute.
    """
    mime_type: str
    """
    *Mime type* – Indicates the type of a binary object. These roughly correspond
    to the content-type of RFC 1341 , the MIME specification.
    """
    approved: bool | None = field(default=None)
    """
    *Approved* – Indicates whether a translation is final or has passed its final
    review.
    """
    translate: bool | None = field(default=None)
    """
    *Translate* – Indicates whether or not the text referred to should be translated.
    """
    reformat: bool | MutableSequence[str] | None = field(default=None)
    """
    Reformat – Indicates whether some properties (size, font, etc.) of the target
    can be formatted differently from the source.
    """
    space: str | None = field(default=None)
    """
    *White spaces* – Specifies how white spaces (ASCII spaces, tabs and
    line-breaks) should be treated.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* – Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    phase_name: str | None = field(default=None)
    """
    *Phase Name* – Used to refer to the given class:`Phase` element.
    """
    restype: RESTYPE | str | None = field(default=None)
    """
    *Resource type* – Indicates the resource type of the container element.
    """
    resname: str | None = field(default=None)
    """
    *Resource name* – Resource name or identifier of a item.
    """
    bin_targets: MutableSequence[BinTarget] = field(default_factory=list)
    context_groups: MutableSequence[ContextGroup] = field(default_factory=list)
    count_groups: MutableSequence[CountGroup] = field(default_factory=list)
    prop_groups: MutableSequence[PropGroup] = field(default_factory=list)
    notes: MutableSequence[Note] = field(default_factory=list)
    trans_units: MutableSequence[TransUnit] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class Group:
    """
    *Group* – Specifies a set of elements that should be processed together.
    """

    id: str | None = field(default=None)
    """
    *Identifier* – Used as a reference to the original corresponding code data
    or format. The value of the id element is determined by the tool creating
    the XLIFF document. It may or may not be a resource identifier.
    The identifier of a resource should, at least, be stored in the
    resname attribute.
    """
    datatype: DATATYPE | str | None = field(default=None)
    """
    *Data type* – Specifies the kind of text contained in the element.
   """
    space: str | None = field(default=None)
    """
    *White spaces* – Specifies how white spaces (ASCII spaces, tabs and
    line-breaks) should be treated.
    """
    ts: str | None = field(default=None)
    """
    *Tool-specific data* – Used to include short data understood by a specific
    toolset. You can also use the :class:`python_xliff.Objects.NamedGroups.Prop`
    element to define large properties at the element level.
    
    .. warning:: 
        DEPRECATED in version 1.1. Instead, use attributes defined in a
        namespace different from XLIFF.
    """
    restype: RESTYPE | str | None = field(default=None)
    """
    *Resource type* – Indicates the resource type of the container element.
    """
    resname: str | None = field(default=None)
    """
    *Resource name* – Resource name or identifier of a item.
    """
    extradata: str | None = field(default=None)
    """
    *Extra data* – Stores the extra data properties of an item.
    """
    help_id: int | None = field(default=None)
    """
    *Help ID* – Stores the help identifier of an item.
    """
    menu: str | None = field(default=None)
    """
    *Menu* – Stores the menu property of an item.
    """
    menu_option: str | None = field(default=None)
    """
    *Menu option* – Stores the option data of a control.
    """
    menu_name: str | None = field(default=None)
    """
    *Menu name* – Stores the menu name of a control.
    """
    coord: Coord | None = field(default=None)
    """
    *Coordinates* – Specifies the x, y, cx and cy coordinates of the text.
    The cx and cy values must represent the width and the height (as in Windows
    resources).
    """
    font: Font | None = field(default=None)
    """
    *Font* – Specifies the font name, size, and weight of the text.
    """
    css_style: str | None = field(default=None)
    """
    *Cascading style-sheet style* – Allows any valid CSS statement to be specified.
    """
    style: str | None = field(default=None)
    """
    *Style* – The resource style of a control.
    """
    exstyle: str | None = field(default=None)
    """
    *Extended style* – Stores the extended style of a control.
    """
    extype: str | None = field(default=None)
    """
    *Extended type* – Stores the extra type properties of an item.
    """
    translate: bool | None = field(default=None)
    """
    *Translate* – Indicates whether or not the text referred to should be translated.
    """
    reformat: bool | MutableSequence[str] | None = field(default=None)
    """
    Reformat – Indicates whether some properties (size, font, etc.) of the target
    can be formatted differently from the source.
    """
    maxbytes: int | None = field(default=None)
    """
    *Maximum bytes* – The maximum number of bytes for the :class:`Target` of a
    :class:`TransUnit`.
    """
    minbytes: int | None = field(default=None)
    """
    *Minimum bytes* – The minimum number of bytes for the :class:`Target` of a
    :class:`TransUnit`.
    """
    size_unit: SIZE_UNIT | str | None = field(default=None)
    """
    *Unit of size attributes* – Specifies the units of measure used in the
    maxheight, minheight, maxwidth, and minwidth attributes.
    """
    maxheight: int | None = field(default=None)
    """
    *Maximum height* – The maximum height for the :class:`Target` of a
    :class:`TransUnit`.
    """
    minheight: int | None = field(default=None)
    """
    *Minimum height* – The minimum height for the :class:`Target` of a
    :class:`TransUnit`.
    """
    maxwidth: int | None = field(default=None)
    """
    *Maximum width* – The maximum width for the :class:`Target` of a 
    :class:`TransUnit`.
    """
    minwidth: int | None = field(default=None)
    """
    *Minimum width* – The minimum width for the :class:`Target` of a
    :class:`TransUnit`.
    """
    charclass: str | None = field(default=None)
    """
    *Character class* – Indicates that a translation is restricted to a
    subset of characters (i.e. ASCII only, Katakana only, uppercase only, etc.).
    """
    merged_trans: bool | None = field(default=None)
    """
    *merged-trans* – Indicates if the group element contains merged 
    :class:`TransUnit` elements.
    """
    context_groups: MutableSequence[ContextGroup] = field(default_factory=list)
    count_groups: MutableSequence[CountGroup] = field(default_factory=list)
    prop_groups: MutableSequence[PropGroup] = field(default_factory=list)
    notes: MutableSequence[Note] = field(default_factory=list)
    groups: MutableSequence[Self] = field(default_factory=list)
    trans_units: MutableSequence[TransUnit] = field(default_factory=list)
    bin_units: MutableSequence[BinUnit] = field(default_factory=list)
