from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


class PRIORITY(Enum):
    """
    *Priority* - The priority of a :class:`Note` element.
    """

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


class CountType(Enum):
    """
    *Count type* - The count-type attribute specifies the purpose of the
    :class:`Count` element. For example: count-type="total" for the total count
    of words in the current scope.
    """

    NUMUSAGE = "num-usages"
    """
    Indicates the count units are items that are used X times in a certain
    context; example: this is a reusable text unit which is used 42 times in
    other texts.
    """
    REPETITION = "repetition"
    """
    Indicates the count units are translation units existing already in the
    same document.
    """
    TOTAL = "total"
    """
    Indicates a total count.
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
    Indicates the line number from the sourcefile (see context-type="sourcefile")
    where the :class:`Source` is found.
    """
    NUMPARAMS = "numparams"
    """
    Indicates a the number of parameters contained within the :class:`Source`.
    """
    PARAMNOTES = "paramnotes"
    """
    Indicates notes pertaining to the parameters in the :class:`Source`.
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
    Indicates the original source file in the case that multiple files are
    merged to form the original file from which the XLIFF file is created.
    This differs from the original :class:`File` attribute in that this sourcefile is
    one of many that make up that file.
    """


class X_PH_CTYPE(Enum):
    IMAGE = "image"
    """
    Indicates a inline image.
    """
    PB = "pb"
    """
    Indicates a page break.
    """
    LB = "lb"
    """
    Indicates a line break.
    """


class CTYPE(Enum):
    BOLD = "bold"
    """
    Indicates a run of bolded text.
    """
    ITALIC = "italic"
    """
    Indicates a run of text in italics.
    """
    UNDERLINED = "underlined"
    """
    Indicates a run of underlined text.
    """
    LINK = "link"
    """
    Indicates a run of hyper-text.
    """


class DATATYPE(Enum):
    """
    *Data type* - The datatype attribute specifies the kind of text contained
    in the element. Depending on that type, you may apply different processes
    to the data. For example: datatype="winres" specifies that the content is
    Windows resources which would allow using the Win32 API in rendering the
    content.
    """

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
    Indicates data from standard UI file operations dialogs (e.g., Open, Save,
    Save As, Export, Import).
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
    Indicates that the datatype attribute value is a MIME Type value and is
    defined in the mime-type attribute.
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
    Indicates a list of property values (e.g., settings within INI files or
    preferences dialog).
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
    Indicates dynamically generated user defined document. e.g. Oracle Report,
    Crystal Report, etc.
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
    Indicates Standard Generalized Markup Language (SGML) data - Document Type
    Definition (DTD).
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
    Indicates Windows (Win32) resources (i.e. resources extracted from an RC
    script, a message file, or a compiled file).
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


@dataclass(slots=True, kw_only=True)
class Coord:
    """
    *Coordinates* - The coord attribute specifies the x, y, cx and cy coordinates
    of the text for a given element. The cx and cy values must represent the
    width and the height (as in Windows resources).
    The extraction and merging tools must make the right conversion if the
    original format uses a top-left/bottom-right coordinate system.
    """

    x: float | Literal["#"]
    y: float | Literal["#"]
    cx: float | Literal["#"]
    cy: float | Literal["#"]


@dataclass(slots=True, kw_only=True)
class Font:
    """
    *Font* - The font attribute specifies the font name, size, and weight of the
    text for a given element. The font attribute would generally be used for
    resource-type data: change of font in document-type data can be marked with
    the :class:`G` element.
    """

    name: str
    size: str | None = field(default=None)
    weight: str | None = field(default=None)
    encoding: str | None = field(default=None)


class MTYPE(Enum):
    """
    *Marker type* - The mtype attribute specifies what a :class:`Mrk` element is
    defining within the content of a :class:`Source` or :class:`Target` element.
    """

    ABBREV = "abbrev"
    """
    Indicates the marked text is an abbreviation.
    """
    ABBREVIATEDFORM = "abbreviatedform"
    """
    ISO-12620 2.1.8: A term resulting from the omission of any part of the full
    term while designating the same concept.
    """
    ABBREVIATION = "abbreviation"
    """
    ISO-12620 2.1.8.1: An abbreviated form of a simple term resulting from the
    omission of some of its letters (e.g. 'adj.' for 'adjective').
    """
    ACRONYM = "acronym"
    """
    ISO-12620 2.1.8.4: An abbreviated form of a term made up of letters from the
    full form of a multiword term strung together into a sequence pronounced only
    syllabically (e.g. 'radar' for 'radio detecting and ranging').
    """
    APPELLATION = "appellation"
    """
    ISO-12620: A proper-name term, such as the name of an agency or other proper
    entity.
    """
    COLLOCATION = "collocation"
    """
    ISO-12620 2.1.18.1: A recurrent word combination characterized by cohesion
    in that the components of the collocation must co-occur within an utterance
    or series of utterances, even though they do not necessarily have to maintain
    immediate proximity to one another.
    """
    COMMONNAME = "commonname"
    """
    ISO-12620 2.1.5: A synonym for an international scientific term that is used
    in general discourse in a given language.
    """
    DATETIME = "datetime"
    """
    Indicates the marked text is a date and/or time.
    """
    EQUATION = "equation"
    """
    ISO-12620 2.1.15: An expression used to represent a concept based on a
    statement that two mathematical expressions are, for instance, equal as
    identified by the equal sign (=), or assigned to one another by a similar sign.
    """
    EXPANDEDFORM = "expandedform"
    """
    ISO-12620 2.1.7: The complete representation of a term for which there is
    an abbreviated form.
    """
    FORMULA = "formula"
    """
    ISO-12620 2.1.14: Figures, symbols or the like used to express a concept
    briefly, such as a mathematical or chemical formula.
    """
    HEADTERM = "headterm"
    """
    ISO-12620 2.1.1: The concept designation that has been chosen to head a
    terminological record.
    """
    INITIALISM = "initialism"
    """
    ISO-12620 2.1.8.3: An abbreviated form of a term consisting of some of the
    initial letters of the words making up a multiword term or the term elements
    making up a compound term when these letters are pronounced individually
    (e.g. 'BSE' for 'bovine spongiform encephalopathy').
    """
    INTERNATIONAL = "international"
    """
    scientific-term 	ISO-12620 2.1.4: A term that is part of an international
    scientific nomenclature as adopted by an appropriate scientific body.
    """
    INTERNATIONALISM = "internationalism"
    """
    ISO-12620 2.1.6: A term that has the same or nearly identical orthographic
    or phonemic form in many languages.
    """
    LOGICALEXPRESSION = "logicalexpression"
    """
    ISO-12620 2.1.16: An expression used to represent a concept based on
    mathematical or logical relations, such as statements of inequality, set
    relationships, Boolean operations, and the like.
    """
    MATERIALSMANAGEMENTUNIT = "materialsmanagementunit"
    """
    ISO-12620 2.1.17: A unit to track object.
    """
    NAME = "name"
    """
    Indicates the marked text is a name.
    """
    NEARSYNONYM = "nearsynonym"
    """
    ISO-12620 2.1.3: A term that represents the same or a very similar concept
    as another term in the same language, but for which interchangeability is
    limited to some contexts and inapplicable in others.
    """
    PARTNUMBER = "partnumber"
    """
    ISO-12620 2.1.17.2: A unique alphanumeric designation assigned to an object
    in a manufacturing system.
    """
    PHRASE = "phrase"
    """
    Indicates the marked text is a phrase.
    """
    PHRASEOLOGICALUNIT = "phraseologicalunit"
    """
    ISO-12620 2.1.18: Any group of two or more words that form a unit, the
    meaning of which frequently cannot be deduced based on the combined sense of
    the words making up the phrase.
    """
    PROTECTED = "protected"
    """
    Indicates the marked text should not be translated.
    """
    ROMANIZEDFORM = "romanizedform"
    """
    ISO-12620 2.1.12: A form of a term resulting from an operation whereby
    non-Latin writing systems are converted to the Latin alphabet.
    """
    SEG = "seg"
    """
    Indicates that the marked text represents a segment.
    """
    SETPHRASE = "setphrase"
    """
    ISO-12620 2.1.18.2: A fixed, lexicalized phrase.
    """
    SHORTFORM = "shortform"
    """
    ISO-12620 2.1.8.2: A variant of a multiword term that includes fewer words
    than the full form of the term (e.g. 'Group of Twenty-four' for
    'Intergovernmental Group of Twenty-four on International Monetary Affairs').
    """
    SKU = "sku"
    """
    ISO-12620 2.1.17.1: Stock keeping unit, an inventory item identified by a
    unique alphanumeric designation assigned to an object in an inventory control
    system.
    """
    STANDARD = "standard"
    """
    text 	ISO-12620 2.1.19: A fixed chunk of recurring text.
    """
    SYMBOL = "symbol"
    """
    ISO-12620 2.1.13: A designation of a concept by letters, numerals,
    pictograms or any combination thereof.
    """
    SYNONYM = "synonym"
    """
    ISO-12620 2.1.2: Any term that represents the same or a very similar concept
    as the main entry term in a term entry.
    """
    SYNONYMOUSPHRASE = "synonymousphrase"
    """
    ISO-12620 2.1.18.3: Phraseological unit in a language that expresses the same
    semantic content as another phrase in that same language.
    """
    TERM = "term"
    """
    Indicates the marked text is a term.
    """
    TRANSCRIBEDFORM = "transcribedform"
    """
    ISO-12620 2.1.11: A form of a term resulting from an operation whereby the
    characters of one writing system are represented by characters from another
    writing system, taking into account the pronunciation of the characters converted.
    """
    TRANSLITERATEDFORM = "transliteratedform"
    """
    ISO-12620 2.1.10: A form of a term resulting from an operation whereby the
    characters of an alphabetic writing system are represented by characters from
    another alphabetic writing system.
    """
    TRUNCATEDTERM = "truncatedterm"
    """
    ISO-12620 2.1.8.5: An abbreviated form of a term resulting from the omission
    of one or more term elements or syllables (e.g. 'flu' for 'influenza').
    """
    VARIANT = "variant"
    """
    ISO-12620 2.1.9: One of the alternate forms of a term.
    """


class POS(Enum):
    """
    *Position* - Indicates whether an isolated tag :class:`It` is a beginning or an
    ending tag."
    """

    OPEN = "open"
    CLOSE = "close"


class PURPOSE(Enum):
    """
    *Purpose* - The purpose attribute specifies the purpose of a
    :class:`ContextGroup` element. For example: purpose="information"
    indicates the content is informational only and not used for specific
    processing.
    """

    INFORMATION = "information"
    """
    Indicates that the context is informational in nature, specifying for example, how a term should be translated. Thus, should be displayed to anyone editing the XLIFF document.
    """
    LOCATION = "location"
    """
    Indicates that the context-group is used to specify where the term was found in the translatable source. Thus, it is not displayed.
    """
    MATCH = "match"
    """
    Indicates that the context information should be used during translation memory lookups. Thus, it is not displayed.
    """


class RESTYPE(Enum):
    """
    *Resource type* - Indicates the resource type of the container element.
    """

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


class SIZEUNIT(Enum):
    """
    *Unit of size attributes* - The size-unit attribute specifies the units of
    measure used in the maxheight, minheight, maxwidth, and minwidth attributes.
    The size-unit attribute is not related to the coord attribute.
    """

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
    Indicates a size in glyphs. A glyph is considered to be one or more combined
    Unicode characters that represent a single displayable text character.
    Sometimes referred to as a 'grapheme cluster'
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


class STATE(Enum):
    """
    *State* - The status of a particular translation in a :class:`Target` or
    :class:`BinTarget` element.
    """

    FINAL = "final"
    """
    Indicates the terminating state.
    """
    NEEDSADAPTATION = "needsadaptation"
    """
    Indicates only non-textual information needs adaptation.
    """
    NEEDSL10N = "needsl10n"
    """
    Indicates both text and non-textual information needs adaptation.
    """
    NEEDSREVIEWADAPTATION = "needsreviewadaptation"
    """
    Indicates only non-textual information needs review.
    """
    NEEDSREVIEWL10N = "needsreviewl10n"
    """
    Indicates both text and non-textual information needs review.
    """
    NEEDSREVIEWTRANSLATION = "needsreviewtranslation"
    """
    Indicates that only the text of the item needs to be reviewed.
    """
    NEEDSTRANSLATION = "needstranslation"
    """
    Indicates that the item needs to be translated.
    """
    NEW = "new"
    """
    Indicates that the item is new. For example, translation units that were not
    in a previous version of the document.
    """
    SIGNEDOFF = "signedoff"
    """
    Indicates that changes are reviewed and approved.
    """
    TRANSLATED = "translated"
    """
    Indicates that the item has been translated.
    """


class STATEQUALIFIER(Enum):
    """
    *State-qualifier* - Describes the state of a particular translation in a
    :class:`Target` or :class:`BinTarget` element.
    """

    EXACTMATCH = "exactmatch"
    """
    Indicates an exact match. An exact match occurs when a source text of a
    segment is exactly the same as the source text of a segment that was
    translated previously.
    """
    FUZZYMATCH = "fuzzymatch"
    """
    Indicates a fuzzy match. A fuzzy match occurs when a source text of a
    segment is very similar to the source text of a segment that was translated
    previously (e.g. when the difference is casing, a few changed words,
    white-space discripancy, etc.).
    """
    IDMATCH = "idmatch"
    """
    Indicates a match based on matching IDs (in addition to matching text).
    """
    LEVERAGEDGLOSSARY = "leveragedglossary"
    """
    Indicates a translation derived from a glossary.
    """
    LEVERAGEDINHERITED = "leveragedinherited"
    """
    Indicates a translation derived from existing translation.
    """
    LEVERAGEDMT = "leveragedmt"
    """
    Indicates a translation derived from machine translation.
    """
    LEVERAGEDREPOSITORY = "leveragedrepository"
    """
    Indicates a translation derived from a translation repository.
    """
    LEVERAGEDTM = "leveragedtm"
    """
    Indicates a translation derived from a translation memory.
    """
    MTSUGGESTION = "mtsuggestion"
    """
    Indicates the translation is suggested by machine translation.
    """
    REJECTEDGRAMMAR = "rejectedgrammar"
    """
    Indicates that the item has been rejected because of incorrect grammar.
    """
    REJECTEDINACCURATE = "rejectedinaccurate"
    """
    Indicates that the item has been rejected because it is incorrect.
    """
    REJECTEDLENGTH = "rejectedlength"
    """
    Indicates that the item has been rejected because it is too long or too short.
    """
    REJECTEDSPELLING = "rejectedspelling"
    """
    Indicates that the item has been rejected because of incorrect spelling.
    """
    TMSUGGESTION = "tmsuggestion"
    """
    Indicates the translation is suggested by translation memory.
    """


class UNIT(Enum):
    """
    *Unit* - The unit attribute specifies the units counted in a :class:`Count`
    element.
    """

    WORD = "word"
    """
    Refers to words.
    """
    PAGE = "page"
    """
    Refers to pages.
    """
    TRANSUNIT = "transunit"
    """
    Refers to <trans-unit> elements.
    """
    BINUNIT = "binunit"
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
