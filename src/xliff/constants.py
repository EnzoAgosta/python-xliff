from enum import Enum
from collections.abc import Callable, Generator, Mapping
from typing import Any, Optional, Protocol, Self, TypeAlias
import lxml.etree as et
import xml.etree.ElementTree as ET

__FAKE__ELEMENT__ = et.Element("fake")


class ElementLikeProtocol(Protocol):
  """
  A protocol defining the minimal interface expected of XML element-like objects.

  Any object that supports this protocol can be used as a replacement for lxml and the
  standard library XML Element objects.

  Only recommended for advanced users, if possible, stick to using lxml.
  """

  tag: str | bytes
  text: Optional[str]
  tail: Optional[str]
  attrib: Mapping[str, str]

  def append(self, other: Self) -> None: ...
  def __len__(self) -> int: ...
  def __iter__(self) -> Generator[Self, None, None]: ...


type ElementLike = ElementLikeProtocol | et._Element | ET.Element
Python_ElementFactory: TypeAlias = Callable[[Any, dict[Any, Any]], ET.Element]


class COUNT_TYPE(Enum):
  NUM_USAGE = "num-usage"
  """
  Indicates the count units are items that are used X times in a certain context
  """
  REPETITION = "repetition"
  """
  Indicates the count units are translation units existing already in the same document.
  """
  TOTAL = "total"
  """
  Indicates a total count.
  """


class UNIT(Enum):
  WORD = "word"
  """
  Refers to words.
  """
  PAGE = "page"
  """
  Refers to pages.
  """
  TRANS_UNIT = "trans-unit"
  """
  Refers to <trans-unit> elements.
  """
  BIN_UNIT = "bin-unit"
  """
  Refers to <bin-unit> elements.
  """
  GLYPH = "glyph"
  """
  Refers to glyphs.
  """
  ITEM = "item"
  """
  Refers to <trans-unit> and/or <bin-unit> elements.
  """
  INSTANCE = "instance"
  """
  Refers to the occurrences of instances defined by the count-type value.
  """
  CHARACTER = "character"
  """
  Refers to characters.
  """
  LINE = "line"
  """
  Refers to lines.
  """
  SENTENCE = "sentence"
  """
  Refers to sentences.
  """
  PARAGRAPH = "paragraph"
  """
  Refers to paragraphs.
  """
  SEGMENT = "segment"
  """
  Refers to segments.
  """
  PLACEABLE = "placeable"
  """
  Refers to placeables (inline elements).
  """


class CONTEXT_TYPE(Enum):
  DATABASE = "database"
  """
  Indicates a database content.
  """
  ELEMENT = "element"
  """
  Indicates the content of an element within an XML document.
  """
  ELEMENTTITLE = "elementtitle"
  """
  Indicates the name of an element within an XML document.
  """
  LINENUMBER = "linenumber"
  """
  Indicates the line number from the sourcefile (see context-type="sourcefile") where
  the <source> is found.
  """
  NUMPARAMS = "numparams"
  """
  Indicates a the number of parameters contained within the <source>.
  """
  PARAMNOTES = "paramnotes"
  """
  Indicates notes pertaining to the parameters in the <source>.
  """
  RECORD = "record"
  """
  Indicates the content of a record within a database.
  """
  RECORDTITLE = "recordtitle"
  """
  Indicates the name of a record within a database.
  """
  SOURCEFILE = "sourcefile"
  """
  Indicates the original source file in the case that multiple files are merged to form
  the original file from which the XLIFF file is created. This differs from the original
  <file> attribute in that this sourcefile is one of many that make up that file.
  """


class PURPOSE(Enum):
  INFORMATION = "information"
  """
  Indicates that the context is informational in nature, specifying for example, how a
  term should be translated. Thus, should be displayed to anyone editing the XLIFF
  document.
  """
  LOCATION = "location"
  """
  Indicates that the context-group is used to specify where the term was found in the
  translatable source. Thus, it is not displayed.
  """
  MATCH = "match"
  """
  Indicates that the context information should be used during translation memory lookups.
  Thus, it is not displayed.
  """


class DATATYPE(Enum):
  ASP = "asp"
  """
  Indicates Active Server Page data.
  """
  C = "c"
  """
  Indicates C source file data.
  """
  CDF = "cdf"
  """
  Indicates Channel Definition Format (CDF) data.
  """
  CFM = "cfm"
  """
  Indicates ColdFusion data.
  """
  CPP = "cpp"
  """
  Indicates C++ source file data.
  """
  CSHARP = "csharp"
  """
  Indicates C-Sharp data.
  """
  CSTRING = "cstring"
  """
  Indicates strings from C, ASM, and driver files data.
  """
  CSV = "csv"
  """
  Indicates comma-separated values data.
  """
  DATABASE = "database"
  """
  Indicates database data.
  """
  DOCUMENTFOOTER = "documentfooter"
  """
  Indicates portions of document that follows data and contains metadata.
  """
  DOCUMENTHEADER = "documentheader"
  """
  Indicates portions of document that precedes data and contains metadata.
  """
  FILEDIALOG = "filedialog"
  """
  Indicates data from standard UI file operations dialogs (e.g., Open, Save, Save As, Export, Import).
  """
  FORM = "form"
  """
  Indicates standard user input screen data.
  """
  HTML = "html"
  """
  Indicates HyperText Markup Language (HTML) data - document instance.
  """
  HTMLBODY = "htmlbody"
  """
  Indicates content within an HTML document's <body> element.
  """
  INI = "ini"
  """
  Indicates Windows INI file data.
  """
  INTERLEAF = "interleaf"
  """
  Indicates Interleaf data.
  """
  JAVACLASS = "javaclass"
  """
  Indicates Java source file data (extension '.java').
  """
  JAVAPROPERTYRESOURCEBUNDLE = "javapropertyresourcebundle"
  """
  Indicates Java property resource bundle data.
  """
  JAVALISTRESOURCEBUNDLE = "javalistresourcebundle"
  """
  Indicates Java list resource bundle data.
  """
  JAVASCRIPT = "javascript"
  """
  Indicates JavaScript source file data.
  """
  JSCRIPT = "jscript"
  """
  Indicates JScript source file data.
  """
  LAYOUT = "layout"
  """
  Indicates information relating to formatting.
  """
  LISP = "lisp"
  """
  Indicates LISP source file data.
  """
  MARGIN = "margin"
  """
  Indicates information relating to margin formats.
  """
  MENUFILE = "menufile"
  """
  Indicates a file containing menu.
  """
  MESSAGEFILE = "messagefile"
  """
  Indicates numerically identified string table.
  """
  MIF = "mif"
  """
  Indicates Maker Interchange Format (MIF) data.
  """
  MIMETYPE = "mimetype"
  """
  Indicates that the datatype attribute value is a MIME Type value and is defined in the mime-type attribute.
  """
  MO = "mo"
  """
  Indicates GNU Machine Object data.
  """
  MSGLIB = "msglib"
  """
  Indicates Message Librarian strings created by Novell's Message Librarian Tool.
  """
  PAGEFOOTER = "pagefooter"
  """
  Indicates information to be displayed at the bottom of each page of a document.
  """
  PAGEHEADER = "pageheader"
  """
  Indicates information to be displayed at the top of each page of a document.
  """
  PARAMETERS = "parameters"
  """
  Indicates a list of property values (e.g., settings within INI files or preferences dialog).
  """
  PASCAL = "pascal"
  """
  Indicates Pascal source file data.
  """
  PHP = "php"
  """
  Indicates Hypertext Preprocessor data.
  """
  PLAINTEXT = "plaintext"
  """
  Indicates plain text file (no formatting other than, possibly, wrapping).
  """
  PO = "po"
  """
  Indicates GNU Portable Object file.
  """
  REPORT = "report"
  """
  Indicates dynamically generated user defined document. e.g. Oracle Report, Crystal Report, etc.
  """
  RESOURCES = "resources"
  """
  Indicates Windows .NET binary resources.
  """
  RESX = "resx"
  """
  Indicates Windows .NET Resources.
  """
  RTF = "rtf"
  """
  Indicates Rich Text Format (RTF) data.
  """
  SGML = "sgml"
  """
  Indicates Standard Generalized Markup Language (SGML) data - document instance.
  """
  SGMLDTD = "sgmldtd"
  """
  Indicates Standard Generalized Markup Language (SGML) data - Document Type Definition (DTD).
  """
  SVG = "svg"
  """
  Indicates Scalable Vector Graphic (SVG) data.
  """
  VBSCRIPT = "vbscript"
  """
  Indicates VisualBasic Script source file.
  """
  WARNING = "warning"
  """
  Indicates warning message.
  """
  WINRES = "winres"
  """
  Indicates Windows (Win32) resources (i.e. resources extracted from an RC script, a message file, or a compiled file).
  """
  XHTML = "xhtml"
  """
  Indicates Extensible HyperText Markup Language (XHTML) data - document instance.
  """
  XML = "xml"
  """
  Indicates Extensible Markup Language (XML) data - document instance.
  """
  XMLDTD = "xmldtd"
  """
  Indicates Extensible Markup Language (XML) data - Document Type Definition (DTD).
  """
  XSL = "xsl"
  """
  Indicates Extensible Stylesheet Language (XSL) data.
  """
  XUL = "xul"
  """
  Indicates XUL elements.
  """


class RESTYPE(Enum):
  AUTO3STATE = "auto3state"
  """
  Indicates a Windows RC AUTO3STATE control.
  """
  AUTOCHECKBOX = "autocheckbox"
  """
  Indicates a Windows RC AUTOCHECKBOX control.
  """
  AUTORADIOBUTTON = "autoradiobutton"
  """
  Indicates a Windows RC AUTORADIOBUTTON control.
  """
  BEDIT = "bedit"
  """
  Indicates a Windows RC BEDIT control.
  """
  BITMAP = "bitmap"
  """
  Indicates a bitmap, for example a BITMAP resource in Windows.
  """
  BUTTON = "button"
  """
  Indicates a button object, for example a BUTTON control Windows.
  """
  CAPTION = "caption"
  """
  Indicates a caption, such as the caption of a dialog box.
  """
  CELL = "cell"
  """
  Indicates the cell in a table, for example the content of the <td> element in HTML.
  """
  CHECKBOX = "checkbox"
  """
  Indicates check box object, for example a CHECKBOX control in Windows.
  """
  CHECKBOXMENUITEM = "checkboxmenuitem"
  """
  Indicates a menu item with an associated checkbox.
  """
  CHECKEDLISTBOX = "checkedlistbox"
  """
  Indicates a list box, but with a check-box for each item.
  """
  COLORCHOOSER = "colorchooser"
  """
  Indicates a color selection dialog.
  """
  COMBOBOX = "combobox"
  """
  Indicates a combination of edit box and listbox object, for example a COMBOBOX control in Windows.
  """
  COMBOBOXEXITEM = "comboboxexitem"
  """
  Indicates an initialization entry of an extended combobox DLGINIT resource block. (code 0x1234).
  """
  COMBOBOXITEM = "comboboxitem"
  """
  Indicates an initialization entry of a combobox DLGINIT resource block (code 0x0403).
  """
  COMPONENT = "component"
  """
  Indicates a UI base class element that cannot be represented by any other element.
  """
  CONTEXTMENU = "contextmenu"
  """
  Indicates a context menu.
  """
  CTEXT = "ctext"
  """
  Indicates a Windows RC CTEXT control.
  """
  CURSOR = "cursor"
  """
  Indicates a cursor, for example a CURSOR resource in Windows.
  """
  DATETIMEPICKER = "datetimepicker"
  """
  Indicates a date/time picker.
  """
  DEFPUSHBUTTON = "defpushbutton"
  """
  Indicates a Windows RC DEFPUSHBUTTON control.
  """
  DIALOG = "dialog"
  """
  Indicates a dialog box.
  """
  DLGINIT = "dlginit"
  """
  Indicates a Windows RC DLGINIT resource block.
  """
  EDIT = "edit"
  """
  Indicates an edit box object, for example an EDIT control in Windows.
  """
  FILE = "file"
  """
  Indicates a filename.
  """
  FILECHOOSER = "filechooser"
  """
  Indicates a file dialog.
  """
  FN = "fn"
  """
  Indicates a footnote.
  """
  FONT = "font"
  """
  Indicates a font name.
  """
  FOOTER = "footer"
  """
  Indicates a footer.
  """
  FRAME = "frame"
  """
  Indicates a frame object.
  """
  GRID = "grid"
  """
  Indicates a XUL grid element.
  """
  GROUPBOX = "groupbox"
  """
  Indicates a groupbox object, for example a GROUPBOX control in Windows.
  """
  HEADER = "header"
  """
  Indicates a header item.
  """
  HEADING = "heading"
  """
  Indicates a heading, such has the content of <h1>, <h2>, etc. in HTML.
  """
  HEDIT = "hedit"
  """
  Indicates a Windows RC HEDIT control.
  """
  HSCROLLBAR = "hscrollbar"
  """
  Indicates a horizontal scrollbar.
  """
  ICON = "icon"
  """
  Indicates an icon, for example an ICON resource in Windows.
  """
  IEDIT = "iedit"
  """
  Indicates a Windows RC IEDIT control.
  """
  KEYWORDS = "keywords"
  """
  Indicates keyword list, such as the content of the Keywords meta-data in HTML, or a K footnote in WinHelp RTF.
  """
  LABEL = "label"
  """
  Indicates a label object.
  """
  LINKLABEL = "linklabel"
  """
  Indicates a label that is also a HTML link (not necessarily a URL).
  """
  LIST = "list"
  """
  Indicates a list (a group of list-items, for example an <ol> or <ul> element in HTML).
  """
  LISTBOX = "listbox"
  """
  Indicates a listbox object, for example an LISTBOX control in Windows.
  """
  LISTITEM = "listitem"
  """
  Indicates an list item (an entry in a list).
  """
  LTEXT = "ltext"
  """
  Indicates a Windows RC LTEXT control.
  """
  MENU = "menu"
  """
  Indicates a menu (a group of menu-items).
  """
  MENUBAR = "menubar"
  """
  Indicates a toolbar containing one or more tope level menus.
  """
  MENUITEM = "menuitem"
  """
  Indicates a menu item (an entry in a menu).
  """
  MENUSEPARATOR = "menuseparator"
  """
  Indicates a XUL menuseparator element.
  """
  MESSAGE = "message"
  """
  Indicates a message, for example an entry in a MESSAGETABLE resource in Windows.
  """
  MONTHCALENDAR = "monthcalendar"
  """
  Indicates a calendar control.
  """
  NUMERICUPDOWN = "numericupdown"
  """
  Indicates an edit box beside a spin control.
  """
  PANEL = "panel"
  """
  Indicates a catch all for rectangular areas.
  """
  POPUPMENU = "popupmenu"
  """
  Indicates a standalone menu not necessarily associated with a menubar.
  """
  PUSHBOX = "pushbox"
  """
  Indicates a pushbox object, for example a PUSHBOX control in Windows.
  """
  PUSHBUTTON = "pushbutton"
  """
  Indicates a Windows RC PUSHBUTTON control.
  """
  RADIO = "radio"
  """
  Indicates a radio button object.
  """
  RADIOBUTTONMENUITEM = "radiobuttonmenuitem"
  """
  Indicates a menuitem with associated radio button.
  """
  RCDATA = "rcdata"
  """
  Indicates raw data resources for an application.
  """
  ROW = "row"
  """
  Indicates a row in a table.
  """
  RTEXT = "rtext"
  """
  Indicates a Windows RC RTEXT control.
  """
  SCROLLPANE = "scrollpane"
  """
  Indicates a user navigable container used to show a portion of a document.
  """
  SEPARATOR = "separator"
  """
  Indicates a generic divider object (e.g. menu group separator).
  """
  SHORTCUT = "shortcut"
  """
  Windows accelerators, shortcuts in resource or property files.
  """
  SPINNER = "spinner"
  """
  Indicates a UI control to indicate process activity but not progress.
  """
  SPLITTER = "splitter"
  """
  Indicates a splitter bar.
  """
  STATE3 = "state3"
  """
  Indicates a Windows RC STATE3 control.
  """
  STATUSBAR = "statusbar"
  """
  Indicates a window for providing feedback to the users, like 'read-only', etc.
  """
  STRING = "string"
  """
  Indicates a string, for example an entry in a STRINGTABLE resource in Windows.
  """
  TABCONTROL = "tabcontrol"
  """
  Indicates a layers of controls with a tab to select layers.
  """
  TABLE = "table"
  """
  Indicates a display and edits regular two-dimensional tables of cells.
  """
  TEXTBOX = "textbox"
  """
  Indicates a XUL textbox element.
  """
  TOGGLEBUTTON = "togglebutton"
  """
  Indicates a UI button that can be toggled to on or off state.
  """
  TOOLBAR = "toolbar"
  """
  Indicates an array of controls, usually buttons.
  """
  TOOLTIP = "tooltip"
  """
  Indicates a pop up tool tip text.
  """
  TRACKBAR = "trackbar"
  """
  Indicates a bar with a pointer indicating a position within a certain range.
  """
  TREE = "tree"
  """
  Indicates a control that displays a set of hierarchical data.
  """
  URI = "uri"
  """
  Indicates a URI (URN or URL).
  """
  USERBUTTON = "userbutton"
  """
  Indicates a Windows RC USERBUTTON control.
  """
  USERCONTROL = "usercontrol"
  """
  Indicates a user-defined control like CONTROL control in Windows.
  """
  VAR = "var"
  """
  Indicates the text of a variable.
  """
  VERSIONINFO = "versioninfo"
  """
  Indicates version information about a resource like VERSIONINFO in Windows.
  """
  VSCROLLBAR = "vscrollbar"
  """
  Indicates a vertical scrollbar.
  """
  WINDOW = "window"
  """
  Indicates a graphical window.
  """


class REFORMAT(Enum):
  COORD = "coord"
  """
  This value indicates that all information in the coord attribute can be modified.
  """
  COORD_X = "coord_x"
  """
  This value indicates that the x information in the coord attribute can be modified.
  """
  COORD_Y = "coord_y"
  """
  This value indicates that the y information in the coord attribute can be modified.
  """
  COORD_CX = "coord_cx"
  """
  This value indicates that the cx information in the coord attribute can be modified.
  """
  COORD_CY = "coord_cy"
  """
  This value indicates that the cy information in the coord attribute can be modified.
  """
  FONT = "font"
  """
  This value indicates that all the information in the font attribute can be modified.
  """
  FONT_NAME = "font_name"
  """
  This value indicates that the name information in the font attribute can be modified.
  """
  FONT_SIZE = "font_size"
  """
  This value indicates that the size information in the font attribute can be modified.
  """
  FONT_WEIGHT = "font_weight"
  """
  This value indicates that the weight information in the font attribute can be modified.
  """
  CSS = "css"
  """
  style 	This value indicates that the information in the css-style attribute can be modified.
  """
  STYLE = "style"
  """
  This value indicates that the information in the style attribute can be modified.
  """
  EX_STYLE = "ex_style"
  """
  This value indicates that the information in the exstyle attribute can be modified.
  """


class SIZE_UNIT(Enum):
  BYTE = "byte"
  """
  Indicates a size in 8-bit bytes.
  """
  CHAR = "char"
  """
  Indicates a size in Unicode characters.
  """
  COL = "col"
  """
  Indicates a size in columns. Used for HTML text area.
  """
  CM = "cm"
  """
  Indicates a size in centimeters.
  """
  DLGUNIT = "dlgunit"
  """
  Indicates a size in dialog units, as defined in Windows resources.
  """
  EM = "em"
  """
  Indicates a size in 'font-size' units (as defined in CSS).
  """
  EX = "ex"
  """
  Indicates a size in 'x-height' units (as defined in CSS).
  """
  GLYPH = "glyph"
  """
  Indicates a size in glyphs. A glyph is considered to be one or more combined Unicode characters that represent a single displayable text character. Sometimes referred to as a 'grapheme cluster'
  """
  IN = "in"
  """
  Indicates a size in inches.
  """
  MM = "mm"
  """
  Indicates a size in millimeters.
  """
  PERCENT = "percent"
  """
  Indicates a size in percentage.
  """
  PIXEL = "pixel"
  """
  Indicates a size in pixels.
  """
  POINT = "point"
  """
  Indicates a size in point.
  """
  ROW = "row"
  """
  Indicates a size in rows. Used for HTML text area.
  """
