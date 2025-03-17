from collections.abc import MutableSequence
from dataclasses import dataclass, field
from typing import Self


@dataclass
class G:
    # Required Attributes
    id: str
    # Optional Attributes
    ctype: str | None = field(default=None)
    ts: str | None = field(default=None)
    clone: str | None = field(default=None)
    xid: str | None = field(default=None)
    equiv_text: str | None = field(default=None)
    # Content
    content: MutableSequence[str | Self | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = (
        field(default_factory=list)
    )


@dataclass
class X:
    # Required Attributes
    id: str
    # Optional Attributes
    ctype: str | None = field(default=None)
    ts: str | None = field(default=None)
    clone: str | None = field(default=None)
    xid: str | None = field(default=None)
    equiv_text: str | None = field(default=None)


@dataclass
class Bx:
    # Required Attributes
    id: str
    # Optional Attributes
    ctype: str | None = field(default=None)
    ts: str | None = field(default=None)
    clone: str | None = field(default=None)
    xid: str | None = field(default=None)
    equiv_text: str | None = field(default=None)


@dataclass
class Ex:
    # Required Attributes
    id: str
    # Optional Attributes
    ctype: str | None = field(default=None)
    ts: str | None = field(default=None)
    clone: str | None = field(default=None)
    xid: str | None = field(default=None)
    equiv_text: str | None = field(default=None)


@dataclass
class Ph:
    # Required Attributes
    id: str
    # Optional Attributes
    ctype: str | None = field(default=None)
    ts: str | None = field(default=None)
    crc: str | None = field(default=None)
    assoc: str | None = field(default=None)
    xid: str | None = field(default=None)
    equiv_text: str | None = field(default=None)
    # Content
    content: MutableSequence[str | Sub] = field(default_factory=list)


@dataclass
class Bpt:
    # Required Attributes
    id: str
    # Optional Attributes
    rid: str | None = field(default=None)
    ctype: str | None = field(default=None)
    ts: str | None = field(default=None)
    crc: str | None = field(default=None)
    equiv_text: str | None = field(default=None)
    # Content
    content: MutableSequence[str | Sub] = field(default_factory=list)


@dataclass
class Ept:
    # Required Attributes
    id: str
    # Optional Attributes
    rid: str | None = field(default=None)
    ctype: str | None = field(default=None)
    ts: str | None = field(default=None)
    crc: str | None = field(default=None)
    equiv_text: str | None = field(default=None)
    # Content
    content: MutableSequence[str | Sub] = field(default_factory=list)


@dataclass
class It:
    # Required Attributes
    id: str
    pos: str
    # Optional Attributes
    rid: str | None = field(default=None)
    ctype: str | None = field(default=None)
    ts: str | None = field(default=None)
    crc: str | None = field(default=None)
    xid: str | None = field(default=None)
    equiv_text: str | None = field(default=None)
    # Content
    content: MutableSequence[str | Sub] = field(default_factory=list)


@dataclass
class Sub:
    # Optional Attributes
    datatype: str | None = field(default=None)
    ctype: str | None = field(default=None)
    xid: str | None = field(default=None)
    # Content
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Mrk] = field(
        default_factory=list
    )


@dataclass
class Mrk:
    # Required Attributes
    mtype: str
    # Optional Attributes
    mid: str | None = field(default=None)
    ts: str | None = field(default=None)
    comment: str | None = field(default=None)
    # Content
    content: MutableSequence[str | G | X | Bx | Ex | Bpt | Ept | Ph | It | Self] = (
        field(default_factory=list)
    )
