from __future__ import annotations

from collections.abc import MutableSequence
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import ClassVar

from lxml.etree import _Element


@dataclass(slots=True)
class HasNonXliff:
    non_xliff: MutableSequence[_Element] = field(default_factory=list)


@dataclass(slots=True)
class Xliff(HasNonXliff):
    """
    *XLIFF document* - The <xliff> element encloses all the other elements of
    the document. The required version attribute specifies the version of XLIFF.

    The optional :attr:`lang` attribute is used to specify the language of the
    content of the document.
    """

    # Required Attributes
    version: ClassVar[str] = "1.2"
    # Optional Attributes
    lang: str | None = field(default=None)
    # Content
    files: MutableSequence[File] = field(default_factory=list)


@dataclass(slots=True)
class File(HasNonXliff):
    """
    *File* - The <file> element corresponds to a single extracted original
    document.

    The required :attr:`original` attribute specifies the name of the file from
    which this file content is derived.
    The required :attr:`datatype` attribute specifies the format of the original
    file; e.g. "html".
    The required :attr:`source_language` attribute specifies the language of the
    <source> content.

    The optional :attr:`target_language` attribute is used to specify the
    language of the <target> content. The optional :attr:`tool_id` attribute
    accepts the id of the <tool> used to generate this XLIFF document.
    The optional :attr:`date` attribute is used to specify the creation date of
    this XLIFF file. The optional :attr:`space` attribute is used to specify how
    white-spaces are to be treated.
    The optional :attr:`category` attribute is used to specify a general category
    of the  content of the file; e.g. "medical".
    The optional :attr:`product_name` attribute is used to specify the name of
    the product which uses this file.
    The optional :attr:`product_version` and :attr:`build_num` attributes are
    used to specify the revision of the product from which this file comes.
    The :attr:`tool` and :attr:`ts` attributes have been deprecated in XLIFF 1.1.
    """

    # Required Attributes
    original: str
    source_language: str
    datatype: str
    # Optional Attributes
    tool: str | None = field(default=None)
    tool_id: str | None = field(default=None)
    date: datetime | None = field(default=None)
    space: str | None = field(default=None)
    ts: str | None = field(default=None)
    category: str | None = field(default=None)
    target_language: str | None = field(default=None)
    product_name: str | None = field(default=None)
    product_version: str | None = field(default=None)
    build_num: str | None = field(default=None)
    # Content
    header: Header
    notes: MutableSequence[Note] = field(default_factory=list)


@dataclass(slots=True)
class Header:
    """
    *File header* - The <header> element contains metadata relating to the
    :class:'File' element.
    """

    # Content
    skl: InternalFile | ExternalFile | None = field(default=None)
    phase_group: PhaseGroup | None = field(default=None)
    glossaries: MutableSequence[InternalFile | ExternalFile] = field(
        default_factory=list
    )
    references: MutableSequence[Reference] = field(default_factory=list)
    count_groups: MutableSequence[CountGroup] = field(default_factory=list)
    prop_groups: MutableSequence[PropGroup] = field(default_factory=list)
    notes: MutableSequence[Note] = field(default_factory=list)
    tools: MutableSequence[Tool] = field(default_factory=list)


@dataclass(slots=True)
class InternalFile:
    """
    *Internal file* - The <internal-file> element contains the actual file
    being referenced.

    The format of the file is specified by the optional :attr:`form` attribute,
    which accepts mime-type values.
    The :attr:`crc` attribute accepts a value that can be used to precisely
    identify and assure the authenticity of the file.
    """

    # Optional Attributes
    form: str | None = field(default=None)
    crc: str | None = field(default=None)
    # Content
    content: str


@dataclass(slots=True)
class ExternalFile:
    """
    *External file* - The <external-file> element specifies the location of the
    actual file being referenced.

    The required :attr:`href` attribute provides a URI to the file.

    The :attr:`crc` attribute accepts a value that can be used to precisely
    identify and assure the authenticity of the file.
    The :attr:`uid` attribute allows a unique ID to be assigned to the file.
    """

    # Required Attributes
    href: str
    # Optional Attributes
    uid: str | None = field(default=None)
    crc: int | None = field(default=None)
    # Content
    content: str


class PRIORITY(Enum):
    Critical = 1
    Urgent = 2
    High = 3
    Elevated = 4
    Medium = 5
    Important = 6
    LowMedium = 7
    Low = 8
    VeryLow = 9
    NoPriority = 10


@dataclass(slots=True)
class Note:
    """
    *Note* - The <note> element is used to add localization-related comments to
    the XLIFF document.

    The content of Note may be instructions from developers about how to handle
    the <source>, comments from the translator about the translation, or any
    comment from anyone involved in processing the XLIFF file.

    The optional :attr:`lang` attribute specifies the language of the note
    content.

    The optional :attr:`from` attribute indicates who entered the note.
    The optional :attr:`priority` attribute allows a priority from 1 (high) to
    10 (low) to be assigned to the note.
    """

    # Optional Attributes
    lang: str | None = field(default=None)
    from_: str | None = field(default=None)
    priority: PRIORITY | None = field(default=None)
    annotates: str | None = field(default=None)
    # Content
    text: str


Note(lang="en-us", priority=12)


@dataclass(slots=True)
class PhaseGroup:
    """
    *Phase group* - The <phase-group> element contains information about the
    task that has been performed on the file.

    This phase information is specific to the tools and workflow used in
    processing the file.
    """

    # Content
    phases: MutableSequence[Phase]


@dataclass(slots=True)
class Phase:
    """
    *Phase information* - The <phase> element contains metadata about the tasks
    performed in a particular process.

    The required :attr:`phase_name` attribute uniquely identifies the phase for
    reference within the :class:`File` element.
    The required :attr:`process_name` attribute identifies the kind of process
    the phase corresponds to; e.g. "proofreading".

    The optional :attr:`company_name` attribute identifies the company
    performing the task.
    The optional :attr:`tool_id` attribute references the :class:`Tool` element
    used in performing the task.
    The optional :attr:`date` attribute provides a timestamp indicating when the
    task was performed.
    The optional :attr:`job_id` attribute allows an ID to be assigned to the job.
    The optional :attr:`contact_name`, :attr:`contact_email`, and
    :attr:`contact_phone` attributes all refer to the person performing the task.
    """

    # Required Attributes
    phase_name: str
    process_name: str
    # Optional Attributes
    company_name: str | None = field(default=None)
    tool: str | None = field(default=None)
    tool_id: str | None = field(default=None)
    date: datetime | None = field(default=None)
    job_id: str | None = field(default=None)
    contact_name: str | None = field(default=None)
    contact_email: str | None = field(default=None)
    contact_phone: str | None = field(default=None)
    # Content
    notes: MutableSequence[Note] = field(default_factory=list)


@dataclass(slots=True)
class Tool:
    """
    *Tool* - The <tool> element describes the tool that has been used to execute
    a given task in the document.

    The required :attr:`tool_id` attribute uniquely identifies the tool for
    reference within the :class:`File` element.
    The required :attr:`tool_name` attribute specifies the actual tool name.
    The optional :attr:`tool_version` attribute provides the version of the tool.
    The optional :attr:`tool_company` attribute provides the name of the company
    that produced the tool.
    """

    # Required Attributes
    tool_id: str
    tool_name: str
    # Optional Attributes
    tool_version: str | None = field(default=None)
    tool_company: str | None = field(default=None)
    # Content
    content: MutableSequence[_Element]
