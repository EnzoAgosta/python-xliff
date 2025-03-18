from collections.abc import MutableSequence
from dataclasses import dataclass, field
from typing import Literal, Self

from python_xliff.Objects.extras import (
    DATATYPE,
    RESTYPE,
    SIZEUNIT,
    STATE,
    STATEQUALIFIER,
    Coord,
    Font,
)
from python_xliff.Objects.Inline import Bpt, Bx, Ept, Ex, G, It, Mrk, Ph, X
from python_xliff.Objects.NamedGroups import ContextGroup, CountGroup, PropGroup
from python_xliff.Objects.TopLevel import ExternalFile, InternalFile, Note


@dataclass(slots=True, kw_only=True)
class Source:
    """
    *Source text* - The :class:`Source` element is used to delimit a unit of text that
    could be a paragraph, a title, a menu item, a caption, etc.
    The content of the :class:`Source` is generally the translatable text,
    depending upon the translate attribute of the parent <trans-unit>.
    The optional :attr:lang attribute is used to specify the content language
    of the :class:`Source`; this should always match source-language as a child of
    <trans-unit> but can vary as a child of <alt-trans>.
    The optional ts attribute was DEPRECATED in XLIFF 1.1.
    """

    lang: str | None = field(default=None)
    """
    *Language* - The xml:lang attribute specifies the language variant of the
    text of a given element. For example: xml:lang="fr-FR" indicates the French
    language as spoken in France.
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
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = field(
        default_factory=list
    )


@dataclass(slots=True, kw_only=True)
class Target:
    """
    *Target* - The :class:`Target` element contains the translation of the content of
    the sibling :class:`Source` element. The optional state and state-qualifier attributes
    indicate in which state the :class:`Target` is. The optional phase-name attribute
    references the <phase> in which the :class:`Target` was last modified. The optional
    xml:lang attribute is used to specify the content language of the :class:`Target`;
    this should always match target-language as a child of <trans-unit> but can
    vary as a child of <alt-trans> . The optional coord, font, css-style, style,
    and exstyle attributes describe the resource contained within the :class:`Target`;
    these are the modifiable attributes for the <trans-unit> depending upon the
    reformat attribute of the parent <trans-unit>. The optional equiv-trans
    describes if the target language translation is a direct equivalent of the
    source text. The optional ts attribute was DEPRECATED in XLIFF 1.1.
    The restype attribute is DEPRECATED in XLIFF 1.2, since :class:`Target` will always
    be of the same restype as its parent <trans-unit> or <alt-trans>.
    A list of preferred values for the restype, state, and state-qualifier
    attributes are provided by this specification.
    """

    state: STATE | str | None = field(default=None)
    """
    *State* - The status of a particular translation in a :class:`Target` or
    :class:`BinTarget` element.
    """
    state_qualifier: STATEQUALIFIER | str | None = field(default=None)
    """
    *State-qualifier* - Describes the state of a particular translation in a
    :class:`Target` or :class:`BinTarget` element.
    """
    phase_name: str | None = field(default=None)
    """
    *Phase Name* - The phase-name attribute provides a unique name for a
    :class:`Phase` element. It is used in other elements in the file to refer to
    the given :class:`Phase` element.
    """
    lang: str | None = field(default=None)
    """
    *Language* - The xml:lang attribute specifies the language variant of the
    text of a given element. For example: xml:lang="fr-FR" indicates the French
    language as spoken in France.
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
    restype: RESTYPE | str | None = field(default=None)
    """
    *Resource type* - Indicates the resource type of the container element.
    """
    resname: str | None = field(default=None)
    """
    Resource name - Resource name or identifier of a item. For example: the key
    in the key/value pair in a Java properties file, the ID of a string in a
    Windows string table, the index value of an entry in a database table, etc.
    """
    coord: Coord | None = field(default=None)
    """
    *Coordinates* - The coord attribute specifies the x, y, cx and cy coordinates
    of the text for a given element. The cx and cy values must represent the
    width and the height (as in Windows resources).
    The extraction and merging tools must make the right conversion if the
    original format uses a top-left/bottom-right coordinate system.
    """
    font: Font | None = field(default=None)
    """
    *Font* - The font attribute specifies the font name, size, and weight of the
    text for a given element. The font attribute would generally be used for
    resource-type data: change of font in document-type data can be marked with
    the :class:`G` element.
    """
    css_style: str | None = field(default=None)
    """
    *Cascading style-sheet style* - The css-style attribute allows any valid CSS
    statement to be specified.
    """
    style: str | None = field(default=None)
    """
    *Style* - The resource style of a control. For example, in Windows resources
    it corresponds to the STYLE statement.
    """
    exstyle: str | None = field(default=None)
    """
    *Extended style* - The exstyle attribute stores the extended style of a
    control. For example, in Windows resources it corresponds to the EXSTYLE
    statement.
    """
    equiv_trans: bool | None = field(default=None)
    """
    *equiv-trans* - Indicates if the target language translation is a direct
    equivalent of the source text.
    """
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = field(
        default_factory=list
    )


@dataclass(slots=True, kw_only=True)
class BinSource:
    content: InternalFile | ExternalFile
    ts: str | None = field(default=None)
    """
    *Tool-specific data* - The ts attribute allows you to include short data
    understood by a specific toolset. You can also use the :class:`Prop`
    element to define large properties at the element level.
    Important: The ts attribute was DEPRECATED in version 1.1. Instead, use
    attributes defined in a namespace different from XLIFF.
    See the Extensibility section for more information.
    """


@dataclass(slots=True, kw_only=True)
class BinTarget:
    content: InternalFile | ExternalFile
    mime_type: str | None = field(default=None)
    """
    *Mime type* - Indicates the type of a binary object. These roughly correspond
    to the content-type of RFC 1341 , the MIME specification; e.g.
    mime-type="image/jpeg" indicates the binary object is an image file of JPEG
    format. This is important in determining how to edit the binary object.
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
    state: STATE | str | None = field(default=None)
    """
    *State* - The status of a particular translation in a :class:`Target` or
    :class:`BinTarget` element.
    """
    phase_name: str | None = field(default=None)
    """
    *Phase Name* - The phase-name attribute provides a unique name for a
    :class:`Phase` element. It is used in other elements in the file to refer to
    the given :class:`Phase` element.
    """
    restype: RESTYPE | str | None = field(default=None)
    """
    *Resource type* - Indicates the resource type of the container element.
    """
    resname: str | None = field(default=None)
    """
    Resource name - Resource name or identifier of a item. For example: the key
    in the key/value pair in a Java properties file, the ID of a string in a
    Windows string table, the index value of an entry in a database table, etc.
    """
    state_qualifier: STATEQUALIFIER | str | None = field(default=None)
    """
    *State-qualifier* - Describes the state of a particular translation in a
    :class:`Target` or :class:`BinTarget` element.
    """


@dataclass(slots=True, kw_only=True)
class SegSource:
    lang: str | None = field(default=None)
    """
    *Language* - The xml:lang attribute specifies the language variant of the
    text of a given element. For example: xml:lang="fr-FR" indicates the French
    language as spoken in France.
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
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = field(
        default_factory=list
    )


@dataclass(slots=True, kw_only=True)
class AltTrans:
    source: Source
    target: Target
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
    match_quality: str | None = field(default=None)
    """
    *Match quality* - The match quality of the :class:`AltTrans` element is tool
    specific and can be a score expressed in percentage or an arbitrary value
    (e.g. match-quality="high").
    """
    tool: str | None = field(default=None)
    """
    *Creation tool* - The tool attribute is used to specify the signature and
    version of the tool that created or modified the document.
    Important: The tool attribute was DEPRECATED in version 1.1. Instead,
    use the :class:`Tool` element and a tool-id attribute.
    """
    tool_id: str | None = field(default=None)
    """
    *Tool identifier* - The tool-id attribute allows unique identification of a
    :class:`Tool` element. It is also used in other elements in the file to
    refer to the given :class:`Tool` element.
    """
    crc: float | None = field(default=None)
    """
    *Cyclic redundancy checking* - A private value used to verify data as it is
    returned to the producer. The generation and verification of this number is
    tool-specific.
    """
    lang: str | None = field(default=None)
    """
    *Language* - The xml:lang attribute specifies the language variant of the
    text of a given element. For example: xml:lang="fr-FR" indicates the French
    language as spoken in France.
    """
    datatype: DATATYPE | str | None = field(default=None)
    """
    *Data type* - The datatype attribute specifies the kind of text contained in
    the element. Depending on that type, you may apply different processes
    to the data. For example: datatype="winres" specifies that the content is
    Windows resources which would allow using the Win32 API in rendering the content.
    """
    space: str | None = field(default=None)
    """
    *White spaces* - The xml:space attribute specifies how white spaces
    (ASCII spaces, tabs and line-breaks) should be treated.
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
    restype: RESTYPE | str | None = field(default=None)
    """
    *Resource type* - Indicates the resource type of the container element.
    """
    resname: str | None = field(default=None)
    """
    Resource name - Resource name or identifier of a item. For example: the key
    in the key/value pair in a Java properties file, the ID of a string in a
    Windows string table, the index value of an entry in a database table, etc.
    """
    extradata: str | None = field(default=None)
    """
    *Extra data* - The extradata attribute stores the extra data properties
    of an item.
    """
    help_id: int | None = field(default=None)
    """
    *Help ID* - The help-id attribute stores the help identifier of an item.
    For example, in Windows resources it corresponds to the Help ID parameter
    of a control.
    """
    menu: str | None = field(default=None)
    """
    *Menu* - The menu attribute stores the menu property of an item.
    """
    menu_option: str | None = field(default=None)
    """
    *Menu option* - The menu-option attribute stores the option data of a control.
    """
    menu_name: str | None = field(default=None)
    """
    *Menu name* - The menu-name attribute stores the menu name of a control.
    """
    coord: Coord | None = field(default=None)
    """
    *Coordinates* - The coord attribute specifies the x, y, cx and cy coordinates
    of the text for a given element. The cx and cy values must represent the
    width and the height (as in Windows resources).
    The extraction and merging tools must make the right conversion if the
    original format uses a top-left/bottom-right coordinate system.
    """
    font: Font | None = field(default=None)
    """
    *Font* - The font attribute specifies the font name, size, and weight of the
    text for a given element. The font attribute would generally be used for
    resource-type data: change of font in document-type data can be marked with
    the :class:`G` element.
    """
    css_style: str | None = field(default=None)
    """
    *Cascading style-sheet style* - The css-style attribute allows any valid CSS
    statement to be specified.
    """
    style: str | None = field(default=None)
    """
    *Style* - The resource style of a control. For example, in Windows resources
    it corresponds to the STYLE statement.
    """
    exstyle: str | None = field(default=None)
    """
    *Extended style* - The exstyle attribute stores the extended style of a
    control. For example, in Windows resources it corresponds to the EXSTYLE
    statement.
    """
    extype: str | None = field(default=None)
    """
    *Extended type* -The extype attribute stores the extra type properties of
    an item.
    """
    origin: str | None = field(default=None)
    """
    *Translation Match Origin* - The origin attribute specifies where a
    translation match came from; for example, from a previous version of the
    same product, a different product, a shared translation memory, etc.
    """
    phase_name: str | None = field(default=None)
    """
    *Phase Name* - The phase-name attribute provides a unique name for a
    :class:`Phase` element. It is used in other elements in the file to refer to
    the given :class:`Phase` element.
    """
    alttranstype: (
        str
        | Literal["proposal", "previous-version", "rejected", "reference", "accepted"]
        | None
    ) = field(default=None)
    """
    *Resource type* - Indicates the type of translation within the containing alt-trans element.
    """
    seg_sources: MutableSequence[SegSource] = field(default_factory=list)
    context_groups: MutableSequence[ContextGroup] = field(default_factory=list)
    count_groups: MutableSequence[CountGroup] = field(default_factory=list)
    prop_groups: MutableSequence[PropGroup] = field(default_factory=list)
    notes: MutableSequence[Note] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class TransUnit:
    """
    *Translation unit* - The <trans-unit> elements contains a :class:`Source`, :class:`Target`
    and associated elements.

    The required :attr:`id` attribute is used to uniquely identify the <trans-unit>
    within all <trans-unit> and <bin-unit> elements within the same :class:`File`.
    The optional :attr:`approved` attribute indicates whether the translation
    has been approved by a reviewer.
    The optional :attr:`translate` attribute indicates whether the <trans-unit>
    is to be translated.
    The optional :attr:`reformat` attribute specifies whether and which
    attributes can be modified for the :class:`Target` element of the <trans-unit>.
    The optional :attr:`space` attribute is used to specify how white-spaces are
    to be treated within the <trans-unit>.
    The optional :attr:`datatype` attribute specifies the data type of the
    content of the <trans-unit>; e.g. "winres" for Windows resources.
    The optional :attr:`ts` attribute was DEPRECATED in XLIFF 1.1.
    The optional :attr:`phase_name` attribute references the phase that the
    <trans-unit> is in.
    The optional :attr:`restype`, :attr:`resname`, :attr:`extradata`,
    :attr:`help_id`, :attr:`menu`, :attr:`menu_option`, :attr:`menu_name`,
    :attr:`coord`, :attr:`font`, :attr:`css_style`, :attr:`style`, :attr:`exstyle`,
    and :attr:`extype` attributes describe the resource contained within the
    <trans-unit>.
    The optional :attr:`maxbytes` and :attr:`minbytes` attributes specify the
    required maximum and minimum number of bytes for the text inside the
    :class:`Source` and :class:`Target` elements of the <trans-unit>.
    The optional :attr:`size_unit` attribute determines the unit for the optional
    :attr:`maxheight`, :attr:`minheight`, :attr:`maxwidth`, and :attr:`minwidth`
    attributes, which limit the size of the resource described by the <trans-unit>.
    The optional :attr:`charclass` attribute restricts all :class:`Source` and :class:`Target`
    text in the scope of the <trans-unit> to a subset of characters.
    Lists of values for the :attr:`datatype`, :attr:`restype`, and
    :attr:`size_unit` attributes are provided by the official specification.
    During translation the content of the :class:`Source` element may be duplicated into
    a <seg-source> element, in which additional segmentation related markup is
    introduced. See the Segmentation section of the oficial spec for more information.
    """

    source: Source
    target: Target
    id: str
    """
    *Identifier* - The id attribute is used in many elements as a reference to
    the original corresponding code data or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document. It may or may not be a resource identifier. The identifier of a
    resource should, at least, be stored in the resname attribute.
    """
    approved: bool | None = field(default=None)
    """
    *Approved* - Indicates whether a translation is final or has passed its final review.
    """
    translate: bool | None = field(default=None)
    """
    *Translate* - The translate attribute indicates whether or not the text
    referred to should be translated.
    """
    reformat: bool | MutableSequence[str] | None = field(default=None)
    """
    Reformat - Indicates whether some properties (size, font, etc.) of the target
    can be formatted differently from the source.
    """
    space: str | None = field(default=None)
    """
    *White spaces* - The xml:space attribute specifies how white spaces
    (ASCII spaces, tabs and line-breaks) should be treated.
    """
    datatype: DATATYPE | str | None = field(default=None)
    """
    *Data type* - The datatype attribute specifies the kind of text contained in
    the element. Depending on that type, you may apply different processes
    to the data. For example: datatype="winres" specifies that the content is
    Windows resources which would allow using the Win32 API in rendering the content.
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
    phase_name: str | None = field(default=None)
    """
    *Phase Name* - The phase-name attribute provides a unique name for a
    :class:`Phase` element. It is used in other elements in the file to refer to
    the given :class:`Phase` element.
    """
    restype: RESTYPE | str | None = field(default=None)
    """
    *Resource type* - Indicates the resource type of the container element.
    """
    resname: str | None = field(default=None)
    """
    Resource name - Resource name or identifier of a item. For example: the key
    in the key/value pair in a Java properties file, the ID of a string in a
    Windows string table, the index value of an entry in a database table, etc.
    """
    extradata: str | None = field(default=None)
    """
    *Extra data* - The extradata attribute stores the extra data properties
    of an item.
    """
    help_id: int | None = field(default=None)
    """
    *Help ID* - The help-id attribute stores the help identifier of an item.
    For example, in Windows resources it corresponds to the Help ID parameter
    of a control.
    """
    menu: str | None = field(default=None)
    """
    *Menu* - The menu attribute stores the menu property of an item.
    """
    menu_option: str | None = field(default=None)
    """
    *Menu option* - The menu-option attribute stores the option data of a control.
    """
    menu_name: str | None = field(default=None)
    """
    *Menu name* - The menu-name attribute stores the menu name of a control.
    """
    coord: Coord | None = field(default=None)
    """
    *Coordinates* - The coord attribute specifies the x, y, cx and cy coordinates
    of the text for a given element. The cx and cy values must represent the
    width and the height (as in Windows resources).
    The extraction and merging tools must make the right conversion if the
    original format uses a top-left/bottom-right coordinate system.
    """
    font: Font | None = field(default=None)
    """
    *Font* - The font attribute specifies the font name, size, and weight of the
    text for a given element. The font attribute would generally be used for
    resource-type data: change of font in document-type data can be marked with
    the :class:`G` element.
    """
    css_style: str | None = field(default=None)
    """
    *Cascading style-sheet style* - The css-style attribute allows any valid CSS
    statement to be specified.
    """
    style: str | None = field(default=None)
    """
    *Style* - The resource style of a control. For example, in Windows resources
    it corresponds to the STYLE statement.
    """
    exstyle: str | None = field(default=None)
    """
    *Extended style* - The exstyle attribute stores the extended style of a
    control. For example, in Windows resources it corresponds to the EXSTYLE
    statement.
    """
    extype: str | None = field(default=None)
    """
    *Extended type* -The extype attribute stores the extra type properties of
    an item.
    """
    maxbytes: int | None = field(default=None)
    """
    *Maximum bytes* - The maximum number of bytes for the :class:è Target` of a
    :class:`TransUnit`. The verification of whether the relevant text respects
    this requirement must be done using the encoding and line-break type of the
    final target environment.
    """
    minbytes: int | None = field(default=None)
    """
    *Minimum bytes* - The minimum number of bytes for the :class:`Target` of a
    :class:`TransUnit`. The verification of whether the relevant text respects
    this requirement must be done using the encoding and line-break type of the
    final target environment.
    """
    size_unit: SIZEUNIT | str | None = field(default=None)
    """
    *Unit of size attributes* - The size-unit attribute specifies the units of
    measure used in the maxheight, minheight, maxwidth, and minwidth attributes.
    The size-unit attribute is not related to the coord attribute.
    """
    maxheight: int | None = field(default=None)
    """
    *Maximum height* - The maximum height for the :class:`Target` of a
    :class:`TransUnit`. This could be interpreted as lines, pixels, or any
    other relevant unit. The unit is determined by the size-unit attribute,
    which defaults to pixel.
    """
    minheight: int | None = field(default=None)
    """
    *Minimum height* - The minimum height for the :class:`Target` of a <trans-unit>. This could be interpreted as lines, pixels, or any other relevant unit. The unit is determined by the size-unit attribute, which defaults to pixel.
    """
    maxwidth: int | None = field(default=None)
    """
    *Maximum width* - The maximum width for the :class:`Target` of a 
    :class:`TransUnit`. This could be interpreted as lines, pixels, or any other
    relevant unit. The unit is determined by the size-unit attribute, which
    defaults to pixel. 
    """
    minwidth: int | None = field(default=None)
    """
    *Minimum width* - The minimum width for the :class:`Target` of a :class:`TransUnit`.
    This could be interpreted as lines, pixels, or any other relevant unit.
    The unit is determined by the size-unit attribute, which defaults to pixel.
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
    bin_source: BinSource
    id: str
    """
    *Identifier* - The id attribute is used in many elements as a reference to
    the original corresponding code data or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document. It may or may not be a resource identifier. The identifier of a
    resource should, at least, be stored in the resname attribute.
    """
    mime_type: str
    """
    *Mime type* - Indicates the type of a binary object. These roughly correspond
    to the content-type of RFC 1341 , the MIME specification; e.g.
    mime-type="image/jpeg" indicates the binary object is an image file of JPEG
    format. This is important in determining how to edit the binary object.
    """
    approved: bool | None = field(default=None)
    translate: bool | None = field(default=None)
    """
    *Translate* - The translate attribute indicates whether or not the text
    referred to should be translated.
    """
    reformat: bool | MutableSequence[str] | None = field(default=None)
    """
    Reformat - Indicates whether some properties (size, font, etc.) of the target
    can be formatted differently from the source.
    """
    space: str | None = field(default=None)
    """
    *White spaces* - The xml:space attribute specifies how white spaces
    (ASCII spaces, tabs and line-breaks) should be treated.
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
    phase_name: str | None = field(default=None)
    """
    *Phase Name* - The phase-name attribute provides a unique name for a
    :class:`Phase` element. It is used in other elements in the file to refer to
    the given :class:`Phase` element.
    """
    restype: RESTYPE | str | None = field(default=None)
    """
    *Resource type* - Indicates the resource type of the container element.
    """
    resname: str | None = field(default=None)
    """
    Resource name - Resource name or identifier of a item. For example: the key
    in the key/value pair in a Java properties file, the ID of a string in a
    Windows string table, the index value of an entry in a database table, etc.
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
    *Group* - The <group> element specifies a set of elements that should be
    processed together. For example: all the items of a menu, etc. Note that a
    :class:`Group` element can contain other :class:`Group` elements.
    The :class:`Group` element can be used to describe the hierarchy of the file.

    The optional :attr:`id` attribute is used to uniquely identify the :class:`Group`
    within the same :class:`File`.
    The optional :attr:`datatype` attribute specifies the data type of the
    content of the :class:`Group`; e.g. "winres" for Windows resources.
    The optional :attr:`space` attribute is used to specify how white-spaces are
    to be treated within the :class:`Group`.
    The optional :attr:`restype`, :attr:`resname`, :attr:`extradata`,
    :attr:`help_id`, :attr:`menu`, :attr:`menu_option`, :attr:`menu_name`,
    :attr:`coord`, :attr:`font`, :attr:`css_style`, :attr:`style`, :attr:`exstyle`,
    and :attr:`extype` attributes describe the resources contained within the
    :class:`Group`.
    The optional :attr:`translate` attribute provides a default value for all
    :class:`TransUnit` elements contained within the :class:`Group`.
    The optional :attr:`reformat` attribute specifies whether and which attributes
    can be modified for the :class:`Target` elements of the :class:`Group`. The optional
    :attr:`maxbytes` and :attr:`minbytes` attributes specify the required maximum
    and minimum number of bytes for the translation units within the :class:`Group`.
    The optional :attr:`size_unit` attribute determines the unit for the optional
    :attr:`maxheight`, :attr:`minheight`, :attr:`maxwidth`, and :attr:`minwidth`
    attributes, which limit the size of the resource described by the :class:`Group`.
    The optional :attr:`charclass` attribute restricts all translation units in
    the scope of the :class:`Group` to a subset of characters.
    The optional :attr:`merged_trans` attribute indicates if the group element
    contains merged :class:`TransUnit` elements.

    The optional :attr:`ts` attribute was DEPRECATED in XLIFF 1.1.
    Lists of values for the :attr:`datatype`, :attr:`restype`, and :attr:`size_unit`
    attributes are provided by the official specification.
    """

    id: str | None = field(default=None)
    """
    *Identifier* - The id attribute is used in many elements as a reference to
    the original corresponding code data or format for the given element.
    The value of the id element is determined by the tool creating the XLIFF
    document. It may or may not be a resource identifier. The identifier of a
    resource should, at least, be stored in the resname attribute.
    """
    datatype: DATATYPE | str | None = field(default=None)
    """
    *Data type* - The datatype attribute specifies the kind of text contained in
    the element. Depending on that type, you may apply different processes
    to the data. For example: datatype="winres" specifies that the content is
    Windows resources which would allow using the Win32 API in rendering the content.
   """
    space: str | None = field(default=None)
    """
    *White spaces* - The xml:space attribute specifies how white spaces
    (ASCII spaces, tabs and line-breaks) should be treated.
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
    restype: RESTYPE | str | None = field(default=None)
    """
    *Resource type* - Indicates the resource type of the container element.
    """
    resname: str | None = field(default=None)
    """
    Resource name - Resource name or identifier of a item. For example: the key
    in the key/value pair in a Java properties file, the ID of a string in a
    Windows string table, the index value of an entry in a database table, etc.
    """
    extradata: str | None = field(default=None)
    """
    *Extra data* - The extradata attribute stores the extra data properties
    of an item.
    """
    help_id: int | None = field(default=None)
    """
    *Help ID* - The help-id attribute stores the help identifier of an item.
    For example, in Windows resources it corresponds to the Help ID parameter
    of a control.
    """
    menu: str | None = field(default=None)
    """
    *Menu* - The menu attribute stores the menu property of an item.
    """
    menu_option: str | None = field(default=None)
    """
    *Menu option* - The menu-option attribute stores the option data of a control.
    """
    menu_name: str | None = field(default=None)
    """
    *Menu name* - The menu-name attribute stores the menu name of a control.
    """
    coord: Coord | None = field(default=None)
    """
    *Coordinates* - The coord attribute specifies the x, y, cx and cy coordinates
    of the text for a given element. The cx and cy values must represent the
    width and the height (as in Windows resources).
    The extraction and merging tools must make the right conversion if the
    original format uses a top-left/bottom-right coordinate system.
    """
    font: Font | None = field(default=None)
    """
    *Font* - The font attribute specifies the font name, size, and weight of the
    text for a given element. The font attribute would generally be used for
    resource-type data: change of font in document-type data can be marked with
    the :class:`G` element.
    """
    css_style: str | None = field(default=None)
    """
    *Cascading style-sheet style* - The css-style attribute allows any valid CSS
    statement to be specified.
    """
    style: str | None = field(default=None)
    """
    *Style* - The resource style of a control. For example, in Windows resources
    it corresponds to the STYLE statement.
    """
    exstyle: str | None = field(default=None)
    """
    *Extended style* - The exstyle attribute stores the extended style of a
    control. For example, in Windows resources it corresponds to the EXSTYLE
    statement.
    """
    extype: str | None = field(default=None)
    """
    *Extended type* -The extype attribute stores the extra type properties of
    an item.
    """
    translate: bool | None = field(default=None)
    """
    *Translate* - The translate attribute indicates whether or not the text
    referred to should be translated.
    """
    reformat: bool | MutableSequence[str] | None = field(default=None)
    """
    Reformat - Indicates whether some properties (size, font, etc.) of the target
    can be formatted differently from the source.
    """
    maxbytes: int | None = field(default=None)
    """
    *Maximum bytes* - The maximum number of bytes for the :class:è Target` of a
    :class:`TransUnit`. The verification of whether the relevant text respects
    this requirement must be done using the encoding and line-break type of the
    final target environment.
    """
    minbytes: int | None = field(default=None)
    """
    *Minimum bytes* - The minimum number of bytes for the :class:`Target` of a
    :class:`TransUnit`. The verification of whether the relevant text respects
    this requirement must be done using the encoding and line-break type of the
    final target environment.
    """
    size_unit: SIZEUNIT | str | None = field(default=None)
    """
    *Unit of size attributes* - The size-unit attribute specifies the units of
    measure used in the maxheight, minheight, maxwidth, and minwidth attributes.
    The size-unit attribute is not related to the coord attribute.
    """
    maxheight: int | None = field(default=None)
    """
    *Maximum height* - The maximum height for the :class:`Target` of a
    :class:`TransUnit`. This could be interpreted as lines, pixels, or any
    other relevant unit. The unit is determined by the size-unit attribute,
    which defaults to pixel.
    """
    minheight: int | None = field(default=None)
    """
    *Minimum height* - The minimum height for the :class:`Target` of a <trans-unit>. This could be interpreted as lines, pixels, or any other relevant unit. The unit is determined by the size-unit attribute, which defaults to pixel.
    """
    maxwidth: int | None = field(default=None)
    """
    *Maximum width* - The maximum width for the :class:`Target` of a 
    :class:`TransUnit`. This could be interpreted as lines, pixels, or any other
    relevant unit. The unit is determined by the size-unit attribute, which
    defaults to pixel. 
    """
    minwidth: int | None = field(default=None)
    """
    *Minimum width* - The minimum width for the :class:`Target` of a :class:`TransUnit`.
    This could be interpreted as lines, pixels, or any other relevant unit.
    The unit is determined by the size-unit attribute, which defaults to pixel.
    """
    charclass: str | None = field(default=None)
    """
    *Character class* - This indicates that a translation is restricted to a
    subset of characters (i.e. ASCII only, Katakana only, uppercase only, etc.).
    A blank value indicates there is no limitation.
    """
    merged_trans: bool | None = field(default=None)
    """
    *merged-trans* - Indicates if the group element contains merged 
    :class:`TransUnit` elements.
    """
    context_groups: MutableSequence[ContextGroup] = field(default_factory=list)
    count_groups: MutableSequence[CountGroup] = field(default_factory=list)
    prop_groups: MutableSequence[PropGroup] = field(default_factory=list)
    notes: MutableSequence[Note] = field(default_factory=list)
    groups: MutableSequence[Self] = field(default_factory=list)
    trans_units: MutableSequence[TransUnit] = field(default_factory=list)
    bin_units: MutableSequence[BinUnit] = field(default_factory=list)
