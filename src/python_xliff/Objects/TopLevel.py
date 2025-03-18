from __future__ import annotations

from collections.abc import MutableSequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from lxml.etree import _Element

from python_xliff.Objects.extras import DATATYPE, PRIORITY
from python_xliff.Objects.NamedGroups import CountGroup, PropGroup
from python_xliff.Objects.Structural import BinUnit, Group, TransUnit


@dataclass(slots=True, kw_only=True)
class Xliff:
    """
    *XLIFF document* - The <xliff> element encloses all the other elements of
    the document. The required version attribute specifies the version of XLIFF.

    The optional :attr:`lang` attribute is used to specify the language of the
    content of the document.
    """

    files: MutableSequence[File] = field(default_factory=list)
    lang: str | None = field(default=None)
    """
    *Language* - The xml:lang attribute specifies the language variant of the
    text of a given element. For example: xml:lang="fr-FR" indicates the French
    language as spoken in France.
    """


@dataclass(slots=True, kw_only=True)
class File:
    """
    *File* - The :class:`File` element corresponds to a single extracted original
    document.

    The required :attr:`original` attribute specifies the name of the file from
    which this file content is derived.
    The required :attr:`datatype` attribute specifies the format of the original
    file; e.g. "html".
    The required :attr:`source_language` attribute specifies the language of the
    :class:`Source` content.

    The optional :attr:`target_language` attribute is used to specify the
    language of the :class:`Target` content. The optional :attr:`tool_id` attribute
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

    header: Header
    original: str
    """
    *Original file* - The original attribute specifies the name of the original
    file from which the contents of a :class:`File` element has been extracted.
    """
    source_language: str
    """
    *Source language* - The language for the :class:`Source` elements in the given
    :class:`File` element.
    """
    datatype: DATATYPE | str
    """
    *Data type* - The datatype attribute specifies the kind of text contained in
    the element. Depending on that type, you may apply different processes
    to the data. For example: datatype="winres" specifies that the content is
    Windows resources which would allow using the Win32 API in rendering the content.
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
    date: datetime | None = field(default=None)
    """
    *Date* - The date attribute indicates when a given element was created or modified
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
    category: str | None = field(default=None)
    """
    *Category* - This provides information on the subject of what is being
    translated. For example: category="medical" for files from a medical related
    product.
    """
    target_language: str | None = field(default=None)
    """
    *Target language* - The language for the :class:`Target` elements in the
    given :class:`File` element.
    """
    product_name: str | None = field(default=None)
    """
    *Product name* - The name of the product which uses this file.
    """
    product_version: str | None = field(default=None)
    """
    *Product version* - The version of the product which uses this file.
    """
    build_num: str | None = field(default=None)
    """
    *Build number* - The build number of the version of the product or
    application the localizable material is for.
    For example: build-num="12" for the 12th build of the new version of a product. 
    """
    notes: MutableSequence[Note] = field(default_factory=list)
    body: MutableSequence[Group | TransUnit | BinUnit] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class Header:
    """
    *File header* - The <header> element contains metadata relating to the
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
    *Glossary* - The <glossary> element points to or contains a glossary,
    which can be used in the localization of the file.
    """

    description: str
    """
    *Description* - The description attribute provides a description of the
    glossary.
    """
    content: InternalFile | ExternalFile


@dataclass(slots=True, kw_only=True)
class Reference:
    """
    *Reference* - The <reference> element points to or contains reference
    material, which can aid in the localization of the file.
    """

    description: str
    """
    *Description* - The description attribute provides a description of the
    glossary.
    """
    content: InternalFile | ExternalFile


@dataclass(slots=True, kw_only=True)
class InternalFile:
    """
    *Internal file* - The <internal-file> element contains the actual file
    being referenced.

    The format of the file is specified by the optional :attr:`form` attribute,
    which accepts mime-type values.
    The :attr:`crc` attribute accepts a value that can be used to precisely
    identify and assure the authenticity of the file.
    """

    content: str
    form: str | None = field(default=None)
    """
    *Format* - Describes the type of format used in an :class:`InternalFile`
    element. For example: form="text" indicates a plain text format internal file.
    """
    crc: float | None = field(default=None)
    """
    *Cyclic redundancy checking* - A private value used to verify data as it is
    returned to the producer. The generation and verification of this number is
    tool-specific.
    """


@dataclass(slots=True, kw_only=True)
class ExternalFile:
    """
    *External file* - The <external-file> element specifies the location of the
    actual file being referenced.

    The required :attr:`href` attribute provides a URI to the file.

    The :attr:`crc` attribute accepts a value that can be used to precisely
    identify and assure the authenticity of the file.
    The :attr:`uid` attribute allows a unique ID to be assigned to the file.
    """

    href: str
    """
    *Hypertext reference* - The location of the file or the URL for an
    :class:`ExternalFile` element. For example:
    href="file:///C:/MyFolder/MyProject/MyFile.htm" indicates a file on a
    local drive.
    """
    uid: str | None = field(default=None)
    """
    *Unique ID* - The uid attribute is used to provide a unique ID to identify
    the skeleton file.
    """
    crc: int | None = field(default=None)


@dataclass(slots=True, kw_only=True)
class Note:
    """
    *Note* - The <note> element is used to add localization-related comments to
    the XLIFF document.

    The content of Note may be instructions from developers about how to handle
    the :class:`Source`, comments from the translator about the translation, or any
    comment from anyone involved in processing the XLIFF file.

    The optional :attr:`lang` attribute specifies the language of the note
    content.

    The optional :attr:`from` attribute indicates who entered the note.
    The optional :attr:`priority` attribute allows a priority from 1 (high) to
    10 (low) to be assigned to the note.
    """

    text: str
    lang: str | None = field(default=None)
    """
    *Language* - The xml:lang attribute specifies the language variant of the
    text of a given element. For example: xml:lang="fr-FR" indicates the French
    language as spoken in France.
    """
    from_: str | None = field(default=None)
    """
    *From* - Indicates the author of a :class:`Note` element. For example:
    from="reviewer" indicates a note from a reviewer.
    """
    priority: PRIORITY | None = field(default=None)
    annotates: Literal["source", "target", " general"] | None = field(default=None)
    """
    *Annotates* - Indicates if a :class:`Note` element pertains to the
    :class:`Source` or the :class:`Target`, or neither in particular.
    """


@dataclass(slots=True, kw_only=True)
class PhaseGroup:
    """
    *Phase group* - The <phase-group> element contains information about the
    task that has been performed on the file.

    This phase information is specific to the tools and workflow used in
    processing the file.
    """

    phases: MutableSequence[Phase]


@dataclass(slots=True, kw_only=True)
class Phase:
    """
    *Phase information* - The :class:`Phase` element contains metadata about the tasks
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

    phase_name: str
    """
    *Phase Name* - The phase-name attribute provides a unique name for a
    :class:`Phase` element. It is used in other elements in the file to refer to
    the given :class:`Phase` element.
    """
    process_name: str
    """
    *Process name* - The name specifying the type of process a given
    :class:`Phase` corresponds to (e.g. Translation, Proofreading, Sizing, etc.).
    """
    company_name: str | None = field(default=None)
    """
    *Company name* - The name of the company that has performed a task.
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
    date: datetime | None = field(default=None)
    """
    *Date* - The date attribute indicates when a given element was created or modified
    """
    job_id: str | None = field(default=None)
    """
    *Job ID* - The identifier given to the localization job.
    This is determined by the entity creating the phase element at the time of
    processing the file.
    """
    contact_name: str | None = field(default=None)
    """
    *Contact name* - The name of the person that has performed a task in a phase.
    """
    contact_email: str | None = field(default=None)
    """
    *Contact email* - The contact email of the contact-name person
    """
    contact_phone: str | None = field(default=None)
    """
    *Contact phone* - The phone number of the contact-name person.
    """
    notes: MutableSequence[Note] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
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

    tool_id: str
    """
    *Tool identifier* - The tool-id attribute allows unique identification of a
    :class:`Tool` element. It is also used in other elements in the file to
    refer to the given :class:`Tool` element.
    """
    tool_name: str
    """
    *Tool name* - The tool-name attribute specifies the name of a given tool.
    """
    content: MutableSequence[_Element]
    tool_version: str | None = field(default=None)
    """
    *Tool version* - The tool-version attribute specifies the version of a
    given tool.
    """
    tool_company: str | None = field(default=None)
    """
    *Tool company* - The tool-company attribute specifies the company from
    which a tool originates.
    """
