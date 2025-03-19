from __future__ import annotations

from collections.abc import MutableSequence
from dataclasses import dataclass, field
from datetime import datetime

from lxml.etree import _Element

from python_xliff.Extras import ANNOTATES, DATATYPE, PRIORITY, VERSION
from python_xliff.NamedGroups.NamedGroups import CountGroup, PropGroup
from python_xliff.Structural import BinUnit, Group, TransUnit

__all__ = [
    "Xliff",
    "File",
    "Header",
    "Glossary",
    "Reference",
    "InternalFile",
    "ExternalFile",
    "Note",
    "PhaseGroup",
    "Phase",
    "Tool",
]


@dataclass(slots=True, kw_only=True)
class Xliff:
    """
    *XLIFF document* – Encloses all the other elements of the document.
    """

    version: VERSION
    files: MutableSequence[File] = field(default_factory=list)
    lang: str | None = field(default=None)
    """
    *Language* - Specifies the language variant of the text of a given element.
    """


@dataclass(slots=True, kw_only=True)
class File:
    """
    *File* – Corresponds to a single extracted original document.
    """

    header: Header
    original: str
    """
    *Original file* – Specifies the name of the original file from which the
    contents has been extracted.
    """
    source_language: str
    """
    *Source language* – The language for the :class:`Source` elements in the
    given :class:`File` element.
    """
    datatype: DATATYPE | str
    """
    *Data type* – Specifies the kind of text contained in the element.
    """
    tool: str | None = field(default=None)
    """
    *Creation tool* – Specify the signature and version of the tool that created
    or modified the document.
    
    .. warning::
        DEPRECATED in version 1.1. Instead, use the :class:`Tool` element and
        a :attr:`Tool.tool_id` attribute.
    """
    tool_id: str | None = field(default=None)
    """
    *Tool identifier* – Used to refer to the given :class:`Tool` element.
    """
    date: datetime | None = field(default=None)
    """
    *Date* – Indicates when a given element was created or modified
    """
    space: str | None = field(default=None)
    """
    *White spaces* – Specifies how white spaces (ASCII spaces, tabs and line-breaks)
    should be treated.
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
    category: str | None = field(default=None)
    """
    *Category* – Provides information on the subject of what is being
    translated.
    """
    target_language: str | None = field(default=None)
    """
    *Target language* – The language for the :class:`Target` elements in the
    given :class:`File` element.
    """
    product_name: str | None = field(default=None)
    """
    *Product name* – The name of the product which uses this file.
    """
    product_version: str | None = field(default=None)
    """
    *Product version* – The version of the product which uses this file.
    """
    build_num: str | None = field(default=None)
    """
    *Build number* – The build number of the version of the product or
    application the localizable material is for.
    """
    groups: MutableSequence[Group] = field(default_factory=list)
    trans_units: MutableSequence[TransUnit] = field(default_factory=list)
    bin_units: MutableSequence[BinUnit] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class Header:
    """
    *File header* – Contains metadata relating to the
    :class:'File' element.
    """

    skl: InternalFile | ExternalFile | None = field(default=None)
    phase_group: PhaseGroup | None = field(default=None)
    glossaries: MutableSequence[Glossary] = field(default_factory=list)
    references: MutableSequence[Reference] = field(default_factory=list)
    count_groups: MutableSequence[CountGroup] = field(default_factory=list)
    prop_groups: MutableSequence[PropGroup] = field(default_factory=list)
    notes: MutableSequence[Note] = field(default_factory=list)
    tools: MutableSequence[Tool] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class Glossary:
    """
    *Glossary* – Points to or contains a glossary, which can be used in the
    localization of the file.
    """

    description: str
    """
    *Description* – Provides a description of the glossary.
    """
    content: InternalFile | ExternalFile


@dataclass(slots=True, kw_only=True)
class Reference:
    """
    *Reference* – Points to or contains reference material, which can aid in the
    localization of the file.
    """

    description: str
    """
    *Description* – Provides a description of the Reference.
    """
    content: InternalFile | ExternalFile


@dataclass(slots=True, kw_only=True)
class InternalFile:
    """
    *Internal file* – Contains the actual file being referenced.
    """

    content: str
    form: str | None = field(default=None)
    """
    *Format* – Describes the type of format used.
    """
    crc: str | None = field(default=None)
    """
    *Cyclic redundancy checking* – Used to verify data as it is returned to
    the producer.
    """


@dataclass(slots=True, kw_only=True)
class ExternalFile:
    """
    *External file* – Specifies the location of theactual file being referenced.
    """

    href: str
    """
    *Hypertext reference* – The location of the file or the URL.
    """
    uid: str | None = field(default=None)
    """
    *Unique ID* – Used to provide a unique ID to identify the skeleton file.
    """
    crc: int | None = field(default=None)


@dataclass(slots=True, kw_only=True)
class Note:
    """
    *Note* – Used to add localization-related comments to the XLIFF document.
    """

    text: str
    lang: str | None = field(default=None)
    """
    *Language* - Specifies the language variant of the text of a given element.
    """
    from_: str | None = field(default=None)
    """
    *From* – Indicates the author of a :class:`Note` element.
    """
    priority: PRIORITY | None = field(default=None)
    annotates: ANNOTATES | None = field(default=None)
    """
    *Annotates* – Indicates if a :class:`Note` element pertains to the
    :class:`Source` or the :class:`Target`, or neither in particular.
    """


@dataclass(slots=True, kw_only=True)
class PhaseGroup:
    """
    *Phase group* – Contains information about the task that has been performed
    on the file.
    """

    phases: MutableSequence[Phase]


@dataclass(slots=True, kw_only=True)
class Phase:
    """
    *Phase information* – Contains metadata about the tasks performed in a
    particular process.
    """

    phase_name: str
    """
    *Phase Name* – Provides a unique name for a :class:`Phase` element.
    """
    process_name: str
    """
    *Process name* – The name specifying the type of process a given
    :class:`Phase` corresponds to.
    """
    company_name: str | None = field(default=None)
    """
    *Company name* – The name of the company that has performed a task.
    """
    tool: str | None = field(default=None)
    """
    *Creation tool* – Used to specify the signature and version of the tool that
    created or modified the document.
    
    .. warning::
        DEPRECATED in version 1.1. Instead, use the :class:`Tool` element and
        a :attr:`Tool.tool_id` attribute.
    """
    tool_id: str | None = field(default=None)
    """
    *Tool identifier* – Allows unique identification of a :class:`Tool` element.
    """
    date: datetime | None = field(default=None)
    """
    *Date* – The date attribute indicates when a given element was created or modified
    """
    job_id: str | None = field(default=None)
    """
    *Job ID* – The identifier given to the localization job.
    """
    contact_name: str | None = field(default=None)
    """
    *Contact name* – The name of the person that has performed a task in a phase.
    """
    contact_email: str | None = field(default=None)
    """
    *Contact email* – The contact email of the contact-name person
    """
    contact_phone: str | None = field(default=None)
    """
    *Contact phone* – The phone number of the contact-name person.
    """
    notes: MutableSequence[Note] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class Tool:
    """
    *Tool* – Describes the tool that has been used to execute a given task in
    the document.
    """

    tool_id: str
    """
    *Tool identifier* – Allows unique identification of a :class:`Tool` element.
    """
    tool_name: str
    """
    *Tool name* – Specifies the name of a given tool.
    """
    content: MutableSequence[_Element]
    tool_version: str | None = field(default=None)
    """
    *Tool version* – Specifies the version of agiven tool.
    """
    tool_company: str | None = field(default=None)
    """
    *Tool company* – Specifies the company from which a tool originates.
    """
