from collections.abc import MutableSequence
from dataclasses import dataclass, field
from typing import Self

from python_xliff.Objects.NamedGroups import ContextGroup, CountGroup, PropGroup
from python_xliff.Objects.TopLevel import ExternalFile, InternalFile, Note


@dataclass
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
    can be modified for the <target> elements of the :class:`Group`. The optional
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

    # Optional Attributes
    id: str | None = field(default=None)
    datatype: str | None = field(default=None)
    space: str | None = field(default=None)
    ts: str | None = field(default=None)
    restype: str | None = field(default=None)
    resname: str | None = field(default=None)
    extradata: str | None = field(default=None)
    help_id: str | None = field(default=None)
    menu: str | None = field(default=None)
    menu_option: str | None = field(default=None)
    menu_name: str | None = field(default=None)
    coord: str | None = field(default=None)
    font: str | None = field(default=None)
    css_style: str | None = field(default=None)
    style: str | None = field(default=None)
    exstyle: str | None = field(default=None)
    extype: str | None = field(default=None)
    translate: str | None = field(default=None)
    reformat: str | None = field(default=None)
    maxbytes: str | None = field(default=None)
    minbytes: str | None = field(default=None)
    size_unit: str | None = field(default=None)
    maxheight: str | None = field(default=None)
    minheight: str | None = field(default=None)
    maxwidth: str | None = field(default=None)
    minwidth: str | None = field(default=None)
    charclass: str | None = field(default=None)
    merged_trans: str | None = field(default=None)
    # Content
    context_groups: MutableSequence[ContextGroup] = field(default_factory=list)
    count_groups: MutableSequence[CountGroup] = field(default_factory=list)
    prop_groups: MutableSequence[PropGroup] = field(default_factory=list)
    notes: MutableSequence[Note] = field(default_factory=list)
    groups: MutableSequence[Self] = field(default_factory=list)
    trans_units: MutableSequence[TransUnit] = field(default_factory=list)
    bin_units: MutableSequence[BinUnit] = field(default_factory=list)


@dataclass
class TransUnit:
    """
    *Translation unit* - The <trans-unit> elements contains a <source>, <target>
    and associated elements.

    The required :attr:`id` attribute is used to uniquely identify the <trans-unit>
    within all <trans-unit> and <bin-unit> elements within the same <file>.
    The optional :attr:`approved` attribute indicates whether the translation
    has been approved by a reviewer.
    The optional :attr:`translate` attribute indicates whether the <trans-unit>
    is to be translated.
    The optional :attr:`reformat` attribute specifies whether and which
    attributes can be modified for the <target> element of the <trans-unit>.
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
    <source> and <target> elements of the <trans-unit>.
    The optional :attr:`size_unit` attribute determines the unit for the optional
    :attr:`maxheight`, :attr:`minheight`, :attr:`maxwidth`, and :attr:`minwidth`
    attributes, which limit the size of the resource described by the <trans-unit>.
    The optional :attr:`charclass` attribute restricts all <source> and <target>
    text in the scope of the <trans-unit> to a subset of characters.
    Lists of values for the :attr:`datatype`, :attr:`restype`, and
    :attr:`size_unit` attributes are provided by the official specification.
    During translation the content of the <source> element may be duplicated into
    a <seg-source> element, in which additional segmentation related markup is
    introduced. See the Segmentation section of the oficial spec for more information.
    """

    # Required Attributes
    id: str
    # Optional Attributes
    approved: str | None = field(default=None)
    translate: str | None = field(default=None)
    reformat: str | None = field(default=None)
    space: str | None = field(default=None)
    datatype: str | None = field(default=None)
    ts: str | None = field(default=None)
    phase_name: str | None = field(default=None)
    restype: str | None = field(default=None)
    resname: str | None = field(default=None)
    extradata: str | None = field(default=None)
    help_id: str | None = field(default=None)
    menu: str | None = field(default=None)
    menu_option: str | None = field(default=None)
    menu_name: str | None = field(default=None)
    coord: str | None = field(default=None)
    font: str | None = field(default=None)
    css_style: str | None = field(default=None)
    style: str | None = field(default=None)
    exstyle: str | None = field(default=None)
    extype: str | None = field(default=None)
    maxbytes: str | None = field(default=None)
    minbytes: str | None = field(default=None)
    size_unit: str | None = field(default=None)
    maxheight: str | None = field(default=None)
    minheight: str | None = field(default=None)
    maxwidth: str | None = field(default=None)
    minwidth: str | None = field(default=None)
    charclass: str | None = field(default=None)
    # Content
    source: Source
    seg_sources: MutableSequence[SegSource] = field(default_factory=list)
    target: Target
    context_groups: MutableSequence[ContextGroup] = field(default_factory=list)
    count_groups: MutableSequence[CountGroup] = field(default_factory=list)
    prop_groups: MutableSequence[PropGroup] = field(default_factory=list)
    notes: MutableSequence[Note] = field(default_factory=list)
    alt_trans: MutableSequence[AltTrans] = field(default_factory=list)


@dataclass
class Source:
    """
    *Source text* - The <source> element is used to delimit a unit of text that
    could be a paragraph, a title, a menu item, a caption, etc.
    The content of the <source> is generally the translatable text,
    depending upon the translate attribute of the parent <trans-unit>.
    The optional :attr:lang attribute is used to specify the content language
    of the <source>; this should always match source-language as a child of
    <trans-unit> but can vary as a child of <alt-trans>.
    The optional ts attribute was DEPRECATED in XLIFF 1.1.
    """

    # Optional Attributes
    lang: str | None = field(default=None)
    ts: str | None = field(default=None)
    # Content
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = field(
        default_factory=list
    )


@dataclass
class Target:
    """
    *Target* - The <target> element contains the translation of the content of
    the sibling <source> element. The optional state and state-qualifier attributes
    indicate in which state the <target> is. The optional phase-name attribute
    references the <phase> in which the <target> was last modified. The optional
    xml:lang attribute is used to specify the content language of the <target>;
    this should always match target-language as a child of <trans-unit> but can
    vary as a child of <alt-trans> . The optional coord, font, css-style, style,
    and exstyle attributes describe the resource contained within the <target>;
    these are the modifiable attributes for the <trans-unit> depending upon the
    reformat attribute of the parent <trans-unit>. The optional equiv-trans
    describes if the target language translation is a direct equivalent of the
    source text. The optional ts attribute was DEPRECATED in XLIFF 1.1.
    The restype attribute is DEPRECATED in XLIFF 1.2, since <target> will always
    be of the same restype as its parent <trans-unit> or <alt-trans>.
    A list of preferred values for the restype, state, and state-qualifier
    attributes are provided by this specification.
    """

    # Optional Attributes
    state: str | None = field(default=None)
    state_qualifier: str | None = field(default=None)
    phase_name: str | None = field(default=None)
    lang: str | None = field(default=None)
    ts: str | None = field(default=None)
    restype: str | None = field(default=None)
    resname: str | None = field(default=None)
    coord: str | None = field(default=None)
    font: str | None = field(default=None)
    css_style: str | None = field(default=None)
    style: str | None = field(default=None)
    exstyle: str | None = field(default=None)
    equiv_trans: str | None = field(default=None)
    # Content
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = field(
        default_factory=list
    )


@dataclass
class AltTrans:
    # Optional Attributes
    mid: str | None = field(default=None)
    match_quality: str | None = field(default=None)
    tool: str | None = field(default=None)
    tool_id: str | None = field(default=None)
    crc: str | None = field(default=None)
    lang: str | None = field(default=None)
    datatype: str | None = field(default=None)
    space: str | None = field(default=None)
    ts: str | None = field(default=None)
    restype: str | None = field(default=None)
    resname: str | None = field(default=None)
    extradata: str | None = field(default=None)
    help_id: str | None = field(default=None)
    menu: str | None = field(default=None)
    menu_option: str | None = field(default=None)
    menu_name: str | None = field(default=None)
    coord: str | None = field(default=None)
    font: str | None = field(default=None)
    css_style: str | None = field(default=None)
    style: str | None = field(default=None)
    exstyle: str | None = field(default=None)
    extype: str | None = field(default=None)
    origin: str | None = field(default=None)
    phase_name: str | None = field(default=None)
    alttranstype: str | None = field(default=None)
    # Content
    source: Source
    seg_sources: MutableSequence[SegSource] = field(default_factory=list)
    target: Target
    context_groups: MutableSequence[ContextGroup] = field(default_factory=list)
    count_groups: MutableSequence[CountGroup] = field(default_factory=list)
    prop_groups: MutableSequence[PropGroup] = field(default_factory=list)
    notes: MutableSequence[Note] = field(default_factory=list)


@dataclass
class BinUnit:
    # Required Attributes
    id: str
    mime_type: str
    # Optional Attributes
    approved: str | None = field(default=None)
    translate: str | None = field(default=None)
    reformat: str | None = field(default=None)
    space: str | None = field(default=None)
    ts: str | None = field(default=None)
    phase_name: str | None = field(default=None)
    restype: str | None = field(default=None)
    resname: str | None = field(default=None)
    # Content
    bin_source: BinSource
    bin_targets: MutableSequence[BinTarget] = field(default_factory=list)
    context_groups: MutableSequence[ContextGroup] = field(default_factory=list)
    count_groups: MutableSequence[CountGroup] = field(default_factory=list)
    prop_groups: MutableSequence[PropGroup] = field(default_factory=list)
    notes: MutableSequence[Note] = field(default_factory=list)
    trans_units: MutableSequence[TransUnit] = field(default_factory=list)


@dataclass
class BinSource:
    # Optional Attributes
    ts: str | None = field(default=None)
    # Content
    content: InternalFile | ExternalFile


@dataclass
class BinTarget:
    # Optional Attributes
    mime_type: str | None = field(default=None)
    ts: str | None = field(default=None)
    state: str | None = field(default=None)
    phase_name: str | None = field(default=None)
    restype: str | None = field(default=None)
    resname: str | None = field(default=None)
    state_qualifier: str | None = field(default=None)
    # Content
    content: InternalFile | ExternalFile


@dataclass
class SegSource:
    # Optional Attributes
    lang: str | None = field(default=None)
    ts: str | None = field(default=None)
    # Content
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = field(
        default_factory=list
    )
